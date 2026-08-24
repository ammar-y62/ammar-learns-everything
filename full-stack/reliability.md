# Reliability: timeouts, exponential backoff, partial failures

Reliability is **not** “nothing fails.” It is continuing to behave acceptably when dependencies are slow, down, overloaded, **partially** successful, or **ambiguous**.

Junior: “Will this call succeed?”
Senior: “What if it is slow, fails, succeeds remotely but I never see the response, is retried, or only half-completes?”

A timeout / network error means **I did not get confirmation**, not “the remote op failed.” Writes (charge, create order) have an `unknown` outcome — blind retry can duplicate the side effect.

## Timeouts

Turn unbounded wait into a **controlled failure**. Without them: hung users, occupied workers, exhausted sockets/connections, cascades.

A timeout **does not stop the remote work**. Caller left; kitchen may still cook. Design timeouts **with** idempotency.

Choose from real latency (p50/p95/**p99**), caller deadline, importance, retry budget. Too short = healthy work fails; too long = resources and cascades. **p99** = 99% finish by that time.

Work **backward from the whole request budget**. Three sequential deps cannot each get the full 2s. Optional work (recommendations) gets a short timeout + fallback; critical (payment) gets more, still bounded.

| Kind | Meaning |
| --- | --- |
| Connection | Can I reach it? (DNS/TCP/TLS) |
| Request | Once connected, can it answer? |
| Overall | Attempt + retries + backoff + cleanup inside the budget |

`Promise.race([fetch, timeout])` is a **waiting** timeout. `fetch` may keep running. Prefer `AbortController` so cancellation can propagate; still check HTTP status; `clearTimeout` in `finally`.

Do not map every failure to valid domain data (`catch { return 0 }` for prices). Timeout ≠ $0. Use `{ success, cents } | { unavailable, reason }`.

Sequential `for await` over 1,000 SKUs is slow; `Promise.all` of 1,000 can melt the dependency. **Controlled concurrency.**

`Promise.race` = first **settled** (success or fail). `Promise.any` = first **success** (rejects only if all reject). Both **start all** work; leftover ops keep running. Fine for interchangeable **reads**. Never `Promise.any([chargeA(), chargeB()])`.

## Retries

Retry **transient** failures (network blip, 429/502/503/504, deadlock) when the op is **safe to repeat** and time remains.

Retries are not “try harder.” 1,000 requests × 3 retries = **retry storm**. Do not retry 400/401/403/validation/business rules. Status meaning is **contextual** (404 after write to eventual search; 409 may be retryable optimistic lock). Classify: retry / do_not_retry / unknown. Never `catch { retry() }`.

**Exponential backoff:** `base * 2^attempt`, **capped**. **Jitter:** randomize delay so clients do not retry in lockstep (thundering herd). Backoff = less often; jitter = not together.

Policy: max attempts, classified errors, per-attempt timeout, backoff + cap + jitter, **overall deadline**, idempotency, user latency budget.

Idempotency = same **final effect**. HTTP method is a hint, not a proof (`POST …/cancel` can still be idempotent). **Idempotency key** names the **logical operation**, not the network attempt — do not mint a new UUID on every retry.

## Partial failure

Some steps succeed, later ones fail. Do not report “registration failed” if the user already exists — the client will retry and duplicate.

Classify **critical** vs **secondary**. Strategies:

| Strategy | Idea |
| --- | --- |
| Accept + log | Secondary fail does not fail the API (no guaranteed recovery) |
| Retry the failed step | Queue welcome email; do not recreate the user |
| Compensate | `releaseInventory` after charge fails — not a DB rollback; compensation can **fail** too |
| DB transaction | Atomic **only** for writes in that DB — cannot include `paymentProvider.charge()` |

`try/catch` detects errors. A transaction provides **atomicity**. `catch` does not undo `stepA`. Saga: each success may need a compensating action. Reliability is **state**: `pending`, `unknown`, `partially_completed`, `retrying`, `degraded`, `recovery_required`, `compensated` — not just success/fail.

If original fail **and** compensation fail: log both, keep original error, maybe `recovery_required`. **Reconciliation** later asks the provider of truth instead of repeating the write.

## Containment

**Fallback** = acceptable substitute (cache, empty optional UI). Not `balance → 0`. Ask what **correctness** you trade for availability.

**Fail-open** = continue (maintenance check, cosmetic flags). **Fail-closed** = deny (authz, billing, destructive ops). Stale feature-flag defaults can be unsafe for security flags. Observe `live | cache | stale | defaults`.

**Circuit breaker:** closed → open (fail fast) → half-open (probe). Retry = try again. Breaker = stop calling. Fallback = substitute. Degraded = stay useful with less.

## Queues (reliability view)

Move retryable secondary work off the request. Queues do **not** erase failure: enqueue fail, crash, **at-least-once** (handlers must be idempotent), ack lost, poison, backlog, visibility timeout, order.

Standard queue: throughput, order not guaranteed. **FIFO** + group key (`orderId`): order **within** group, groups concurrent. Kafka order is **per partition**.

**DLQ** = exhausted / permanent failures for inspect/replay, not silent drop.

**SQS visibility timeout** = “this worker owns the message.” If processing > timeout and no heartbeat, another worker can start the **same** job. Set from p99; too long delays crash recovery. Safety: visibility + extend/heartbeat + **idempotent** handlers.

Poison = permanent (bad payload) → do not retry forever. Distinguish transient vs permanent; swallowing validation may **ack** instead of DLQ — logs must match behavior.

In-process `.then()` after returning `{ status: processing }` is **not durable**. Persist the job.

## Async vs sequential (Node)

`await A(); await B()` is **async + sequential**: B waits for A; the runtime can run **other** requests while A waits on I/O. It does **not** skip to B. Node is one JS thread + I/O; CPU loops block everyone. `Promise.all` = async + concurrent. Transactions ≠ `await`.

## Codebase patterns (to remember)

- L4 workflow: later fail → invalidate downstream, rethrow; compensation must not hide the original error
- Shared SQS visibility 30s vs long imports → duplicate risk
- Feature flags: cache → live → stale → defaults (availability vs stale config)
- S3 multipart abort: backoff; cleanup fail must not replace upload fail; add jitter
- Redis: command timeout **and** reconnect policy, capped retries
- Clerk on the **request path**: few, short, classified, jittered, overall deadline — not worker-style retries
- Maintenance fail-open: still needs a **short** timeout so a hung check does not stall every page
- Polling: one transient fetch should not kill the whole poll loop

## Corrected misunderstandings

| Wrong | Right |
| --- | --- |
| Timeout = remote failed | Caller stopped waiting; outcome may be unknown |
| Retry always helps | Can amplify outages; classify + bound |
| Retry all 500s | Some are deterministic bugs |
| Logged = handled | Observability ≠ recovery |
| Queue = reliable | Still duplicates, visibility, poison, DLQ |
| Longer timeout = safer | Hold resources, grow queues, worsen cascades |
| `try/catch` = rollback | Need tx, compensation, or cleanup |
| Sequential `await` = sync | Other work can run during I/O wait |

Every dependency needs a **boundary**: timeout, retry class, attempts, jitter, fallback, breaker, metrics, idempotency. Contain blast radius. Prefer a path from unknown → valid (retry, replay, reconcile, compensate, human repair). Observe timeouts, retries, breakers, fallbacks, queue age/DLQ, duplicates, partial fails.

**Make failures bounded, explicit, recoverable, and observable.**
