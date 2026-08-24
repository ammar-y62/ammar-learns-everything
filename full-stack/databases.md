# Databases: transactions, indexes, types, N+1 queries, race conditions

A database **protects shared state** (many requests, instances, workers, retries). App code describes what should happen. The DB can **enforce** what is allowed.

App check ≠ guarantee. Two requests can both `findUnique` then both `create`. Authoritative uniqueness is `UNIQUE` / unique index. UX check is fine; constraint is the contract. If violating a rule would corrupt the system, enforce it in the DB (`NOT NULL`, `UNIQUE`, `FK`, `CHECK`, `PK`).

## Database types (by workload)

| Kind | Examples | Fit |
| --- | --- | --- |
| Relational | Postgres, MySQL | relationships, constraints, transactions — strong default when correctness matters |
| Document | MongoDB | nested / irregular records; Postgres `JSONB` often enough |
| Key-value | Redis | `token → session`, TTL, millions of exact lookups |
| Search | Elasticsearch | full-text, fuzzy, ranking — **not** SoT |
| Warehouse | Snowflake, BigQuery, ClickHouse, Databricks | huge scans/aggregations, BI/ML |

**ACID:** all-or-nothing, encoded rules stay valid, concurrency controlled, commit survives. **BASE:** available, replicas may disagree, eventual converge. Not a strict SQL-vs-NoSQL rule anymore.

```text
Postgres = product / business state (SoT)
Elasticsearch = searchable copy (inverted index: term → docs)
Warehouse = understand the product (pipelines from OLTP)
```

**OLTP:** few rows, low latency, high correctness. **Analytics:** large scans, group-by years of data. Pre-aggregate when dashboards cannot scan raw facts.

## Queries and indexes

SQL says **what**. The planner decides **how** (seq scan, index, join, sort). Cost is work done, not how short the SQL looks. Ask: query count, rows examined vs returned, index match, sorts, joins, lock waits, fat columns, round trips.

**Index** = shortcut so the DB need not inspect every row. PK (and usually `UNIQUE`) get indexes; `WHERE name = 'ammar'` does not unless you create one.

Indexes cost storage, cache, and **write** (insert/update/delete). Index **query patterns**, not every column.

**Composite** `(status, created_at)` is used **left to right**. `WHERE status` and `status + created_at` (and `ORDER BY created_at` after status) can use it. `WHERE created_at` alone generally cannot. **SQL predicate order does not matter; index column order does.**

Same idea: `(user_id, created_at)` → good for that user, that user + time range, that user `ORDER BY created_at DESC LIMIT 20` (B-tree can scan backwards). Weak for time-only. Partial help: `user_id = 42 AND type = 'login'` finds the user then filters `type`. Ask: how much work remains after the index?

**Selectivity:** `email = one row` vs `status` 50/50 on 10M rows. Planner may seq-scan if the index barely narrows. Index present ≠ index used. Seq scan is not automatically bad (tiny table, or returning most of a huge table).

**Partial index:** only rows matching a predicate (`WHERE deleted_at IS NULL`). Smaller, matches soft-delete / pending / unpaid queries. Queries for “all rows” cannot use it.

## N+1

1 query for a list + **N** queries inside a loop. 100 users → 101 round trips. `users.map(id)` then `WHERE user_id IN (...)` is **one** query — in-memory loops ≠ DB trips.

Fixes: ORM `include` (verify SQL — not always one query), batch then group in memory (2 queries), aggregate if you only need a count. Goal is a **bounded** query count, not always one giant join (join can explode row width).

ORMs hide lazy loads. Smell: `await find(...)` / related access **inside** `for` / `map(async)`. Measure query count at 1 / 10 / 100 / 1000 items.

## Transactions

All related ops commit or none. Use when “op1 succeeds, op2 fails” would be invalid (transfer, order + inventory, user + membership).

Transactions do **not** automatically kill races. Read-modify-write inside `$transaction` can still lose updates. Isolation, locks, atomic SQL, and constraints still matter.

ACID only enforces **rules that exist in the DB**. Unwritten app rules are not magic.

## Races and concurrency

Race = result depends on timing. **Lost update:** both read 100, both write 70; should be 40.

Unsafe: read → compute in app → write. Safer: `UPDATE … SET balance = balance - 30 WHERE id = 1 AND balance >= 30` (0 vs 1 row). Move check **into** the write. Same for claiming jobs: `UPDATE … SET status = 'processing' WHERE status = 'pending'` — do not separate “is pending?” from “claim it.”

Retries / double-click / lost response: uniqueness + **idempotency key**. Assume important commands may run twice. Codebase pattern: prefer atomic/targeted updates (`updateSimulationParametersAtomic`) over load whole row → mutate → save; optional `WHERE version = $n` or `jsonb_set`.

| Tool | When |
| --- | --- |
| Atomic `UPDATE` | correctness in one statement (counters, balances, claim) |
| Transaction | multiple writes are one business op |
| `SELECT … FOR UPDATE` | must read, decide, then write; hold the lock **briefly** |
| Optimistic version | conflicts rare; 0 rows → stale, reload/retry |

Isolation (practical): **Read Committed** (Postgres default) — no dirty reads, world can change between statements. **Repeatable Read** — stable snapshot, writes may need retry. **Serializable** — more anomalies rejected, more retries/less concurrency. Do not jump to serializable before unique / atomic / lock / idempotency.

## Workload picks (exercise)

- Session tokens, millions of lookups, 24h TTL → **key-value** (Redis)
- Product search + typos → **search engine**; Postgres remains SoT
- Bank ledger (never lose/double money, audit) → **relational** + entries that balance, not just `UPDATE balance`
- Flexible profile JSON → document **or** Postgres JSONB
- Daily revenue by SKU, 3 years, huge groups → warehouse (or Postgres at small scale); often a pipeline from OLTP

## Mental models

| Topic | Junior | Senior |
| --- | --- | --- |
| Writes | check in app, then write | what can change between check and write? what if twice? |
| Indexes | make tables faster | which query, columns, order, selectivity, will the planner use it? |
| N+1 | each query is fast | how does query count grow with N? |
| Transactions | inside tx = safe | partial-completion vs concurrency are different questions |

For important writes: never-invalid states, which **layer** guarantees them, two requests, two executions, crash mid-way, commit but lost response, retry safety.

**Correctness must survive concurrency and repetition, not just the happy path.**
