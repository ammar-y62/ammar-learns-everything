# API design: idempotency, validation, error responses

API design is **behavior design**, not route naming. The contract is: if a client sends this request, what can it reliably expect — including failure, retries, duplicates, old clients, and edge cases.

Junior: “Does the happy path work?”
Senior: “Can clients depend on this when things go wrong?”

## Contract

Types/DTOs describe **shape**. The API contract describes **behavior**.

Includes: accepted/rejected inputs, status codes, error shape, stable error **codes**, retry safety, duplicate-request behavior, lost-response behavior, old clients, user vs log vs leaked info, partial failure.

Consumers are not just the current frontend: old UIs, mobile versions, scripts, jobs, other services, Postman, retries, malicious callers.

The frontend is not the source of truth. “The button is disabled” is not a backend guarantee.

## Running example

```text
DELETE /companies/:companyId/projects/:projectId/simulations/:simulationName/programs/:programName
```

Removing a known resource is `DELETE`, not `POST` (POST usually means create / submit / command).

Shape can be valid, user authenticated, resource exists — and the operation is still disallowed: **the selected baseline program cannot be removed.** That is a business-rule failure, not malformed input.

| Kind | Example |
| --- | --- |
| Invalid input | `programName` missing from the path |
| Business rule | Valid `DELETE` of the current baseline |

## Idempotency

Same request multiple times → **same final effect** as sending it once. Not necessarily the same response.

```text
DELETE /users/42
1st → 204
2nd → 404 or 204
final state: still deleted
```

Danger is **uncertainty**, not only failure:

```text
client sends request
server succeeds
response is lost / timeout
client retries
duplicate side effect (payment, order, email, inventory, …)
```

If the answer to “response lost — should the client retry?” is yes, the API must say whether retry is **safe**.

HTTP conventions (implementation must still honor them):

| Method | Usual meaning | Idempotent? |
| --- | --- | --- |
| GET | read | usually (no business side effects) |
| PUT | replace known resource | usually |
| DELETE | remove known resource | usually |
| POST | create / action | **not** by default |
| PATCH | partial update | **depends** (`email: new@…` yes; `incrementBy: 1` no) |

POST can be made retry-safe with an **idempotency key** (or client request id / dedupe table):

```text
same key + same request → return stored result, do not redo the side effect
```

Also decide: same key + different body, in-progress ops, concurrent same-key requests, expired stored responses.

Review question: **what happens if this exact request is received twice?**

## Validation

**Client validation helps the user. Server validation protects the system.**

Client: required fields, format, fast UX. Not trustworthy.

Server must enforce authz, ownership, existence, uniqueness, state, business rules — even if the UI is broken, old, bypassed, or missing.

Client can make invalid actions harder. Server must make them **impossible**.

## NestJS layers

| Layer | Owns | Throws |
| --- | --- | --- |
| Pipes | shape, DTO, parsing | NestJS `BadRequestException` ok |
| Guards | auth, route access | NestJS `Unauthorized` / `Forbidden` ok |
| Services | business rules, entity state | **`@eip-mono/errors` only** |

```ts
// bad: NestJS exception in a service
throw new BadRequestException('Cannot delete baseline program.');

// good
throw new BadRequestError(
  'User attempting to remove program selected as baseline.',
  {
    userMessage: `Cannot remove the baseline program '${baselineProgram}'. Change the baseline program in simulation settings first.`,
    severityLevel: 'LOW',
    logData: { companyId, projectId, simulationName, baselineProgram },
  },
);
```

## Error responses

Errors are part of the contract. Serve **programs**, **users**, and **devs**.

```json
{
  "error": {
    "code": "BASELINE_PROGRAM_CANNOT_BE_REMOVED",
    "message": "Cannot remove the baseline program. Change the baseline in simulation settings first.",
    "fields": { "email": "Email is required." },
    "requestId": "req_9f82a1"
  }
}
```

- **code** — stable, machine-readable. Clients branch on this, never on English `message.includes(...)`.
- **message** — safe, actionable, no stack traces / table names / secrets.
- **fields** — when validation is field-level.
- **requestId** — bridge from user report → logs/traces.

| Status | Meaning |
| --- | --- |
| 400 | shape / validation invalid |
| 401 | not authenticated |
| 403 | authenticated but not allowed |
| 404 | missing or intentionally hidden |
| 409 | conflicts with current state |
| 422 | well-formed but semantically invalid |
| 429 | rate limited (`Retry-After`) |
| 500 / 503 | unexpected / temporary |

Usually **do not retry**: 400, 401, 403, 404, 409, 422.

Often **retryable** (still not automatically safe): 408, 429 (after wait), 502, 503, 504, some 500s.

## Thrown errors (three audiences)

```ts
throw new BadRequestError('Dev-facing: what went wrong technically.', {
  userMessage: 'Safe, actionable message for the user.',
  severityLevel: 'LOW',
  logData: { companyId, projectId, resourceName },
});
```

| Piece | For |
| --- | --- |
| First arg | logs / developers |
| `userMessage` | users (omit if they should not see it) |
| `severityLevel` | ops (`LOW` = expected rejection, not a wake-up) |
| `logData` | debug context: ids/names, **no** PII, tokens, raw payloads |

Log messages are not user messages.

| Class | When |
| --- | --- |
| `BadRequestError` | invalid input or **expected** business-rule rejection (baseline delete → `LOW`) |
| `ResourceNotFoundError` | entity missing / not in this context |
| `DataValidationError` | schema/shape/contract integrity, not business meaning |
| `InvalidStateError` | persisted/system state is inconsistent or transition is invalid |
| `UnauthorizedError` | authn/authz failure in application logic |

Do not pick the class by vibes. Baseline delete is expected user behavior → `BadRequestError` + `LOW`, not `InvalidStateError`.

## Do not

- NestJS exceptions in services
- Vague `'Bad request.'`
- Internals in user-facing text (`ldar_simulation row 53`)
- PII/secrets in `logData`

## Review checklist

- Twice: same request — state still stable? hidden side effects?
- Lost response: retry safe? need a key? poll status?
- Client UX vs server contract — are we trusting the frontend?
- Pipe vs guard vs service? right `@eip-mono/errors` class?
- Stable `code`, safe `userMessage`, useful `logData`, correct severity?
- Old clients still work?

## Corrected misunderstandings

| Wrong | Right |
| --- | --- |
| Frontend already validates, backend can skip | Frontend is UX; backend is the contract |
| POST = create, PUT = update | Choose methods for **behavior and retry**, not CRUD labels |
| Idempotent = identical response | Same **final effect** |
| Retries are always good | Retries can duplicate side effects |
| Errors are just messages | Codes for programs, messages for people, ids for logs |
| 200 means the whole workflow succeeded | Define what success includes (order vs pay vs email) |
| Endpoint works → API is done | Done when clients can integrate **without guessing** |
