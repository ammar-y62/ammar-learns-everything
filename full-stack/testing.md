# Testing: unit vs integration tests, mocking, edge cases

Tests are **executable confidence**: if I change this, how fast do I know I broke something that matters? Valuable when that confidence is worth the maintenance cost. Weak tests prove a function exists or a mock was called.

Protect: business rules, integrations, failure paths, transitions, edges, concurrency, persistence.

## Levels

| Kind | Answers | Keep real |
| --- | --- | --- |
| Unit | Does this logic behave? | Isolated; deps controlled |
| Integration | Do these pieces really work together? | DB, ORM, Redis, queue, schema |
| E2E | Does the journey work from outside? | Critical paths only |
| Contract | Do systems still agree on the wire? | Shape, codes, required fields |

“Unit” is a **behavior boundary**, not “one function.” Names matter less than: **which boundaries are real, and what did I replace?**

**Smallest test that still hits the real source of risk.** Logic → unit. SQL / tx / constraints / Redis / queue semantics → integration. Would mocking **remove the thing I’m trying to prove?** (mocked DB cannot prove rollback.) Keep real the dep you need confidence in. Local Postgres/Redis: often real. Stripe/SendGrid/AWS: usually mock/fake.

## Jest and doubles

Jest is the runner, not “a mock.” `it` / `expect` / matchers. `jest.fn()` tracks calls and can `mockResolvedValue` / `mockRejectedValue`.

```ts
await expect(fail()).rejects.toThrow('Something failed');
await expect(getUser()).resolves.toEqual({ id: '123' });
expect(() => parseBadInput()).toThrow('Invalid input');
```

| Double | Role |
| --- | --- |
| Stub | “When asked, return this.” |
| Mock | “Verify this interaction.” |
| Spy | Watch (or replace) an existing fn |
| Fake | Simplified **working** impl (in-memory cache) |

`jest.fn()` can be any of these. Ask: **what did I replace, and what confidence did I lose?**

Mock slow/dangerous/external deps and hard-to-reproduce failures. A mock that returns `{ success: true }` only proves **our code with that fake**. Mock **boundaries you don’t own**; be cautious mocking **your own** persistence. Interaction asserts are good when the interaction **is** the requirement (charge once, no email on validation fail, ≤3 retries).

Refactor internals without changing observable behavior → test should still pass. Spying `validate` / `save` is brittle wiring.

## Edge cases and failures

An edge is near a **boundary where behavior changes** (99 / 100 / 101), not a random 723. Sources: 0/1/-1/max; empty/one/many; empty/whitespace/Unicode; expiry ±1s; owner vs missing auth; timeout, lost response, duplicate, partial fail, crash.

Happy path: it works. Failure path: it **fails safely**. Invalid input: meaningful classes, not every garbage string. Retries: `mockRejectedValueOnce` then success; assert call count **and** max-attempts stop. Partial workflow: DB ok / pay fail; pay ok / email fail; pay ok / response lost. Duplicate same idempotency key → charge **once**. Draw A→B→C and ask what fails **between** each pair.

## Async, queues, DB

Producer vs consumer separately. Wait for a **completion signal**, not `sleep(3000)`.

Queue: job emitted? worker correct? transient retry? permanent stop? duplicate safe? real queue config?

If the guarantee is SQL (unique, FK, rollback, lock, isolation), **test SQL**. Rollback test: step1 inserts, step2 fails → step1 row **gone**. Race: two withdraws in `Promise.all`, then assert invariant. Outbox: order + outbox row in **same** tx. Isolated test DB, migrate, seed, clean. Not prod/dev.

## Isolation and fixtures

Flakes destroy trust (“probably flaky”). Hidden inputs: `Date.now`, `Math.random`, sleeps, shared module/`process.env`/DB rows, third-party APIs, parallel tests sharing IDs/ports.

Factories (`makeUser({ active: false })`) highlight the one difference. Fixtures reuse a scenario (risk: hidden context). Builders for fat objects. `beforeEach` isolate; `afterEach` reset mocks; don’t hide the scenario in a giant `beforeEach`. Arrange / Act / Assert.

Each test **starts known, independently runnable, leaves the world as found.** Module `Map`, clock, `process.env` = same leak class. Prefer inject (`dueIn(ms, now = Date.now())`, `createPriceCache()`) over globals. If time is already an argument, **pass a Date** — don’t fake timers. Fake timers when time is hidden (`todayKey()`). Don’t `expect(dueIn(0)).toEqual(Date.now())` — the clock can tick. Restore env: save, `delete` vs set, `afterEach`. Local date vs UTC (`getDate` vs `toISOString`).

## Coverage and pyramid

Coverage = what **ran**, not whether you **proved** it. `divide(10, 2)` can hit lines while returning 999. Use as a **map** of untested branches. 100% + `toBeDefined()` is weak; fewer tests on payments/auth/tx can be stronger.

Many fast tests, some integration, few E2E. Effort scales with **failure cost**. `fullName` ≠ charge+ledger+event.

## Frontend hooks

`renderHook` mounts the hook. `act` flushes updates. `result.current` is the public API. Same idea as backend: control deps, assert **observable** state/callbacks (success vs fail, reset not called if callback throws).

## Codebase lessons (patterns)

| If you care about | Test |
| --- | --- |
| Pure calc / semantic dates | Unit, no mocks |
| Query / `ON CONFLICT` / `FOR UPDATE` | Real Postgres |
| Orchestration / compensate-then-rethrow | Unit; persist cleanup = integration |
| Handler swallow vs rethrow | Unit; **name it that** — not “sent to DLQ” |
| Duplicate Worker in **one process** | Call count; cluster-wide needs Redis/DB lock |
| Updater preserves other clone flags | Inspect the updater fn, not `toHaveBeenCalled` |
| Delete builder wiring | Mock call; **rows gone** needs seed + query |
| Controller maps 207 | Unit; journey = Playwright |

Mocked `transaction(fn => fn(tx))` is not BEGIN/ROLLBACK. Sleep-then-assert lock wait is flaky — synchronize. Test names must match **what assertions prove**. Test **recovery failing** (rollback of rollback).

## Corrected misunderstandings

| Wrong | Right |
| --- | --- |
| Unit = one function | Small controlled behavior |
| More mocks = better unit test | May only prove mocks talking to mocks |
| High coverage = safe | Execution ≠ assertion quality |
| Integration is too slow to use | Some bugs only exist at the boundary |
| Test every internal helper | Public behavior unless it has independent meaning |
| Passing test = feature works | Only that scenario |
| Never use real infra | Use it when **it** is the guarantee |
| Flakes are just annoying | They train people to ignore CI |

**Did I mock a dependency, or mock away the behavior I wanted to prove?**
**Where can the bug actually exist — and is this the cheapest maintainable test that catches it?**
