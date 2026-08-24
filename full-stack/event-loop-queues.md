# System design: event loop, queues, background jobs, retries

Some work happens now. Some completes later. Some fails. Some must not block the user. Some must survive crashes and be retried safely.

Local JS async (promises, `async`/`await`, event loop) is **not** the same as system async (queues, workers, durable jobs).

> A promise is not a queue. The event loop is not a background worker. A retry is not automatically safe. A background job is not automatically reliable.

## Sync vs async

**Sync:** finish this, then the next line. Slow I/O blocks everything after it.

**Async:** start/schedule work, continue, handle the result later. Coordination over time — **not** always parallel.

```js
console.log("Start");
fetch("/api/user").then((user) => console.log(user));
console.log("End");
// Start, End, then user data
```

## Promises and `async`/`await`

A **Promise** is a handle to a future result: `pending` → `fulfilled` or `rejected`. It is not the value.

`.then()` is a pipeline: returned value feeds the next step; returned promises are awaited. Missing `return response.json()` → next step gets `undefined`. `.then(() => …)` waits but ignores the value. Rejections skip `.then` unless `.catch` exists. `.finally()` is cleanup (loading, locks, timers).

`async`/`await` is syntax over promises. `await` pauses **this async function**, not the runtime. Async functions always return promises; `throw` → rejected promise.

```js
async function run() {
  console.log("A");
  await fetch("/api/user");
  console.log("B");
}
run();
console.log("C");
// A, C, B
```

Forgetting `await`: function returns success before work finishes; `try/catch` does **not** catch later rejections. Catch async errors only if you `await` inside the `try`.

## Event loop

JS runs one piece at a time. The runtime (timers, I/O, network) does work off the call stack; when it finishes, the continuation waits its turn.

Busy stack (`while (true) {}`) blocks timers, clicks, promise callbacks, rendering.

```text
1. synchronous code
2. microtasks  (.then / .catch / .finally, queueMicrotask, after await)
3. macrotasks  (setTimeout, setInterval, many I/O / UI events)
```

`setTimeout(fn, 0)` = enqueue a macrotask, not “run now.”

Microtask scheduled from a microtask still runs **before** timers.

Node extra: `process.nextTick` runs **before** regular promise microtasks.

```text
sync: A, G (async fn before await), I
nextTick: F
microtasks: C, E, H, D (D scheduled from C)
macrotask: B (setTimeout 0)
```

Do not memorize every edge case. Know the categories.

## Layers (what survives a crash?)

| Layer | Answers | Survives app process crash? |
| --- | --- | --- |
| Promise | observe success/failure later | no (in-memory) |
| Event loop | which JS continuation runs next | no (`setTimeout` dies with the process) |
| In-process `await` | wait for I/O without blocking the stack | no |
| External queue | defer work outside this request | **usually yes** if the backend is durable |

Redis stores/coordinates jobs. Redis is **not** the worker. Full system = queue lib + store + workers + retries + idempotency + monitoring.

Ask: is Redis persisted? worker crash mid-job? retries? duplicates?

## Queues and background jobs

`producer → queue → worker`

Use for: decoupling, absorbing spikes, concurrency limits, retries, slow/rate-limited/CPU/scheduled work **outside** the request.

```text
signup → enqueue "send welcome email" → respond
worker sends email later
```

`setTimeout(sendEmail, 5000)` is delay in **this process**, not a job. Crash before 5s → gone.

A queue is durable coordination, not just delay. It also introduces: duplicates, out-of-order, retry-after-partial-success, stuck/poison jobs, backlogs.

**When not to background:** if you cannot honestly tell the user it succeeded yet. Do not enqueue `charge-customer` then return `{ success: true }`. Charge + create order in the request; receipt email can be a job.

**Queued ≠ completed.** Request success ≠ job success.

```text
Signup success: account created, email job queued (email may not be sent)
POST /reports: record exists, job queued — client polls GET /reports/:id
```

Statuses: `queued` → `processing` → `retrying` → `completed` | `failed` | `failed_permanently`.

## Retries

Temporary failures (503, dropped connection, timeout) may be worth retrying. Immediate retry can make outages worse → **backoff** (linear or exponential) + **jitter**.

A timeout means **we stopped waiting**, not “it failed.” The charge may have succeeded.

Safer: reads, idempotent updates, unique job ids, APIs with idempotency keys.

Riskier: payments, creates, emails, shipping, deletes.

Queue `attempts` + backoff is config. Real question: **is the job safe to run more than once?** Unique `jobId`, processed-event ids, persisted progress, DB constraints.

## Failure modes

- **Duplicates:** double enqueue, crash after side effect, redelivery, double-click, webhook replay.
- **Partial success:** charge ok, ship fails, retry charges again → persist progress, skip completed steps.
- **Races:** last writer wins; read-modify-write on balance → atomic increment / locks / versions.
- **Stuck:** crash, hung I/O, no timeout → heartbeats, stall detection, dead-letter.
- **Poison:** always fails (bad payload) → do not retry permanent errors; cap attempts; DLQ.
- **Backlog:** enqueue faster than process. Watch **oldest job age**, not just depth.

## Observability

Jobs run later, often in another process. Reconstruct: `jobId`, `jobName`, `userId`, `resourceId`, `requestId` / **correlationId**, `attemptNumber`.

Log status transitions. Metrics: depth, oldest age, fail/retry/DLQ rates, duration. Alerts on age, DLQ, no workers — not “one error.” Store failure **code/reason**, not secrets or huge payloads.

Job payload: **stable IDs**, worker loads source of truth. Not a giant stale snapshot.

## Mentor bugs

**`forEach(async …)`** does not wait. Returns `{ failed: 0 }` then imports finish. Use `for…of` + `await` (sequential) or `map` + `Promise.all` (parallel).

```text
for…of + await = one at a time
map + Promise.all = start all, wait for all
```

`Promise.all` **fail-fast**: one reject rejects the group. `Promise.allSettled` waits for all, then inspect fulfilled/rejected. Huge arrays still need a concurrency limit.

**Fire-and-forget email:** `sendWelcomeEmail(email)` without await/queue starts in-memory work; `registered` does not mean email sent. `try/catch` without `await` only catches sync throws. Owner of the work owns the failure: controller enqueues; worker sends and **rethrows** so the queue can retry.

**In-memory “queue”:** `maxConcurrent` unused (starts every job), not durable, no status, no retry/DLQ. It is `job()` in process memory. Real flow: persist `queued` → external `queue.add({ fileId })` → worker updates processing/completed/failed → rethrow on failure.

## Corrected misunderstandings

| Wrong | Right |
| --- | --- |
| `await` pauses the whole runtime | Pauses this async function |
| Promise / `setTimeout` = background job | In-process; dies with the process |
| Queue = run it later | Durability + coordination + a new failure contract |
| Move all slow work off the request | Only if the request can honestly succeed first |
| Fail → retry | Retry if safe or idempotent; timeout ≠ failed |
| Job succeeds or fails | Also: twice, halfway, stuck, poison, race, backlog |

**What does the system promise at this point, and what if the work is slow, fails, runs twice, or is interrupted?**
