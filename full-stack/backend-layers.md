# Backend: repo vs service vs controller

Not “which folder?” — **who owns this decision** so the code stays understandable, testable, and cheap to change?

```text
Controller  → transport / HTTP:  what did the outside world ask for?
Service     → application:       what should the app do?
Repository  → persistence:       how do I read or persist it?
```

Which layer has **enough** context without knowing more than it needs? Layers exist because they **change for different reasons** (API vs business vs schema). That is **change containment**.

File names are not architecture. Judge by decisions, deps, reasons to change.

## Controller (transport)

Convert HTTP into an application operation: routes, `@Param` / `@Query` / `@Body`, DTOs, pipes, guards, status codes, extract `user.id`, call the use case.

DTO = allowed request shape (not `body: any`). Pipe = validate/parse **before** the method (`ParseIntPipe`, `ZodValidationPipe`).

```text
Structurally valid?  → boundary (DTO / pipe / Zod)
Operation allowed?   → Service
```

Authn = who. Authz: generic permission (`INVENTORY_WRITE`) at the **edge**; object-specific (“can *this* user edit *this* inventory?”) in the **Service**. Controller/guard establishes identity; Service receives `userId` as data — not `service.getUserFromHttpRequest()`.

Service throws `DuplicateOrder`; HTTP maps to 409. Prefer one error vocabulary + a global filter. `@Res()` + `res.status().json()` bypasses Nest returns/filters and duplicates mapping.

Thin:

```ts
return this.userService.createUser({ ...dto, createdBy: user.id });
```

**Would this still be needed from a queue, CLI, cron, or another Service?** If yes, it is not Controller-only. Fat smell: `if`, repo calls, transactions, orchestration, notifications, business auth.

One trivial `GET` → Repository can be fine. Multi-repo orchestration belongs in a Service. Inconsistent `GET → repo` / `POST → service` means later Service rules get **bypassed**.

Never `companyId: body.companyId ?? req.user.companyId` unless that tenant switch is explicitly authorized — default to authenticated tenant.

## Service (use case)

Not “everything leftover.” Owns the **operation**: rules, orchestration, state transitions, several repos/services, tx boundary, domain errors, reuse across HTTP/jobs/CLI.

```text
PENDING → APPROVED allowed  → Service
How to UPDATE status        → Repository
```

**If the DB were replaced tomorrow, would this rule still exist?** Yes → business. No → persistence.

A Service may call many deps if they are **one coherent use case**. Fat = many unrelated reasons to change (calc + PDF + billing + CSV in one constructor). Anemic pass-through is OK as a stable API, not as “every Controller must have a Service.”

Non-HTTP callers (reconciliation job, CSV) are the test: if semantics differ (no notifications, no fraud checks), use a **different** use case (`importHistoricalOrder`), don’t reuse `place()` by accident. Don’t mix `OrdersService` for one query and Repository for another — rules added later get skipped.

## Repository (persistence)

Hide ORM/SQL, joins, soft deletes, mappings, DB errors, persistence txs. Names: `findActiveByCollectionId`, not `approveInventory`.

Conditionals that belong here: integrity (too many rows), unique/FK, corrupt mapping. Not “user cannot approve this order.”

1:1 `findMany(args) → prisma.findMany(args)` is a rename, not a boundary. Service still writes ORM. Expose intent (`findWithWorkflowStatus`). Skip the layer if the app is tiny and queries are trivial.

Presentation/domain in a repo (confidence intervals by L5 source, “these groups must exist for this summary”) → parse in repo, interpret in Service/mapper.

## DI, inversion, cycles

DI = how deps are **provided**. Inversion = high-level logic depends on an **abstraction** when the seam is real — not an interface for everything.

`@Injectable()` = Nest-managed dep. `@Controller()` = HTTP entry (already managed; don’t stack both). Direction: Controller → Service → Repository → DB. Repo must not know HTTP types.

`forwardRef` fixes wiring, not ownership. Cycles → coordinator or a smaller shared capability. Duplicate providers (`ClerkModule` re-registers `CompanyService`) hide cycles — extract `CompanyLookup` / `CompanyIdResolver`.

## Transactions and side effects

Tx = what must **all happen or none**. The layer that sees the **whole** operation usually owns the boundary (often Service). Repo may join an outer tx:

```ts
existingTx ? run(existingTx) : db.transaction(run)
```

Independent nested txs can drop locks/checks. DB tx cannot roll back email/HTTP/broker. Outbox: business writes + event **intent** in the **same** tx; worker publishes later.

Read-check-write races: `SELECT FOR UPDATE`, atomic `UPDATE … WHERE qty >= :qty`, optimistic version, constraints.

## Testing

Controller: HTTP integration (400/401/403, pipes, guards) beats `expect(service.create).toHaveBeenCalled`. Service unit tests (mock repo) are the high-ROI layer. Repository: real SQL, not mocked `findMany`. Mixed HTTP+DB+queue just to test one rule = boundaries too weak.

## Codebase patterns

- L4 Controller: Zod + params → Service. No uniqueness, tx, or repo in the Controller.
- Shared uniqueness + lock + tx; caller passes `insert(tx)` — invariant vs L4-specific persist.
- Repo optional `existingTx` so outer lock stays intact.
- Controller two cleanups, no shared tx → Service + one tx.
- Ingestion `@Res()` / try-catch / status mapping → pipe + Service errors + filter.
- Giant emission-factor Service: split by **reason to change**, not line count; don’t invent strategy trees without real variability.
- Same “invalidate downstream” rule: L4 repo+builder vs MS Service+Drizzle — **filenames ≠ architecture**; WHAT invalid vs HOW deleted should be explicit.
- `startDate > endDate` → Zod `.refine()`, not a Controller `if`.
- Collection interceptor + method→READ/WRITE at the edge; Service uses `userId`, doesn’t re-login.
- Mix of custom errors vs Nest `NotFoundException` can turn 404 into **500** via the filter.
- Workflow factory: extra layer OK because it **owns state-specific selection**.
- Reconciliation: `listForCompany` (no drafts) vs `totalForCompany` (paid only) — compare the **same** population.

## Smells vs healthy

| Smell | Healthy |
| --- | --- |
| Controller: business `if`, multi-repo, ORM, tx, tenant from body | Transport, parse/auth, one Service call |
| Service: HTTP exceptions, Prisma `WhereInput`, request objects, unrelated deps | Coherent use case, domain errors, tx for the invariant |
| Repo: auth, email, UI shaping, 1:1 ORM, workflow orchestration | Intent-named queries, mapping, persistence errors |
| Facade→Manager→Adapter all `return next.do()` | Abstraction hides a **real** decision |

**If a rule still matters from HTTP, queue, cron, CLI, or CSV, it does not live only in the Controller.** Predictable ownership across similar features beats individually clever exceptions.
