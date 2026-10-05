# Backend architecture styles: layered, onion, hexagonal, clean

Architecture is not folder names. It is **who owns what**, **what may depend on what**, and **how cheap a change is**.

`A → B` means A knows B. If `InventoryService` takes `DrizzleDb`, Drizzle changing can force the service to change.

**Coupling** = how much one part knows about another. Depend on `InventoryRepository`, not `DrizzleDb`, when you only need “persist inventory.”

Runtime flow and **code** dependencies differ. HTTP still runs Controller → use case → repo impl → DB. Onion/Clean try to keep *code* deps pointing **inward**: use case → **interface**; impl → interface.

A **boundary** stops leaks. A use case generally should not know `Request`, `HttpException`, Drizzle query builders, Express.

**What changes for what reason, and who owns that change?** Route → controller. DTO → adapter. Workflow → use case. Rule → domain. Schema → repo. Vendor → adapter.

## The four styles

| Style | Main idea |
| --- | --- |
| **Layered** | Separate technical jobs: Controller → Service → Repository → DB |
| **Onion** | Dependencies point **inward**; domain in the middle |
| **Hexagonal** | Outside world talks through **ports** (contracts) and **adapters** (impls) |
| **Clean** | Entities + use cases stay **framework-independent** |

Same family. Emphasis differs; real code often looks similar.

**Layered** is simple, common in Nest, enough for CRUD. Weakness: services become dumping grounds (DB + queue + HTTP exceptions + vendor SDK in one class). Hurts when logic is complex, many externals, many entry points.

**Onion rings:** Domain = what is true in the business (`Inventory.requiresWorkflow()`). Application = what we are trying to do (create inventory, maybe create workflow). Infrastructure = how (Postgres, HTTP, SQS). Outer may know inner; inner must not know Nest/Drizzle.

**Hexagonal:** Port = contract. Adapter = implementation. **Inbound/driving** starts the use case (HTTP, SQS, cron, CLI). **Outbound/driven** helps it finish (DB, email, vendor). Many ways in, many ways out, **one** core. Six sides are just the diagram.

**Clean:** Entities → use cases → interface adapters (controllers, repo impls, presenters) → frameworks. Nest/Drizzle live at the **edge**, not “never use them.”

```text
Controller              → infra / inbound adapter / interface adapter
Service / use case      → application / core / use case
Domain entity           → domain / entities
Repository interface    → app/domain boundary / outbound port
Repository implementation → infrastructure / outbound adapter
DB, queue, vendor SDK   → outside / frameworks
```

Technical roles (Controller/Service/Repository) ≠ architectural rings (Domain/Application/Infrastructure).

## DI vs dependency inversion

**DI** = Nest **gives** you the dep (`constructor(private repo: DrizzleInventoryRepository)`). Wiring.

**DIP** = important code depends on a **contract**, impl conforms (`Use Case → Interface ← Drizzle`). Design.

You can have DI **without** DIP. `implements Repository` is not a port unless **callers inject the interface**, not the concrete class. Tokens (`provide: Token.OgmpInvRepo, useClass: …`) let Nest pick the impl.

## Boundaries that matter

**Tx:** application owns **what must be atomic** (lock + check + insert); infra owns BEGIN/COMMIT. A `Transaction` type on `insert(tx)` leaks — often a **correctness over purity** tradeoff. UnitOfWork only if you need another backend.

**Validation:** shape/UUID/required → edge. “Can this inventory be approved?” → app/domain.

**Auth:** JWT valid → edge. “This user may approve *this* inventory?” → app/domain.

**Errors:** `InventoryCannotBeApprovedError` in core; filter maps to HTTP. Repos throw data/not-found, not `HttpException`.

**Queues:** consumers are inbound adapters. Same use case from HTTP and SQS. Detached `.then()` after `return { status: "processing" }` means **nobody owns** retries/errors — enqueue a job the worker owns.

**Tests:** can you test the rule without HTTP/DB? Domain unit, use-case with fakes, repo integration, thin E2E. Architecture does not replace integration tests.

Map DB rows **before** calc (`calculateSpatialError(input)`, not the Drizzle row) so schema churn doesn’t hit math.

Architecture cannot stop **business** rule changes. It should put the change in the code that **owns** that reason. Vendor swaps (Flagsmith, Prisma, Kafka) should hit adapters.

## When to add ceremony

Useful: complex rules, multiple entry points, replaceable vendors, shared use cases, persistence and domain change independently.

Overkill: `GetSourceMeasurementsUseCase` + port + adapter + mapper + presenter for `return this.repository.get…()`. Not every CRUD needs an interface.

**Smallest boundary that protects a real reason for change.** More layers/interfaces ≠ more senior.

## Codebase patterns

- Top-Down create: Controller → Service → repo/Drizzle. Fine as **layered**. Pain is **duplicated create flows** across inventory types, not missing ports.
- `createInventoryWithUniqueName`: lock + check + insert in one tx. Drizzle `tx` in app is an acceptable leak.
- Shared workflow state machine: factory → state service (rules) → repo. App logic off HTTP. Weak: `[key: string]: unknown` update shape.
- TDI orchestrator: fetch / calculate / save / rollback are **different jobs**; orchestrator owns partial-fail cleanup. Map rows before calc helpers — don’t port every helper.
- `libs/calculations` (`calculateSpatialError`): no Nest/Drizzle; `api-nest → calculations`, not the reverse.
- Feature flags: `FeatureFlagProvider` port, Flagsmith adapter — vendor vs policy change independently. Cleanest ports/adapters example.
- BUI import: HTTP + SQS → same `ImportPrimaryBuiService`. Smell: floating finalize promise.
- Newer: `BaseError` → filter. Older: `DatabaseException extends HttpException` in repos — HTTP in infra.
- Primary state machine vs older OGMP: similar features, different styles. New work should **pick a default**, not rewrite everything.
- External inventory reads: Controller → service → repos → API shape. Thin layered reads are OK until they grow real write rules.
- `implements InventoryRepository` but service injects `TopDownInventoryRepository` extra methods → generic constraint, **not** DIP.
- Source-measurement list: keep layered. If DB select type is the public API, map it.

## Cheat sheet

```text
Layered     Controller → Service → Repository → DB
Onion       Infra → Application → Domain (deps inward)
Hexagonal   Inbound adapters → core → outbound adapters
Clean       Frameworks → adapters → use cases → entities

DI          Nest injects the object
DIP         Depend on the contract, not Drizzle/Flagsmith/…

Protect     important logic from replaceable tech
Skip        interfaces that don’t separate different reasons to change
```
