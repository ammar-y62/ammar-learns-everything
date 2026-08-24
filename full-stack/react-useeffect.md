# React: useEffect, dependency arrays, stale closures

`useEffect` is not a lifecycle helper. It is tied to React’s render model and JS closures.

## Foundations

- **Props** = data from the parent. Component does not own them.
- **State** = data the component owns and updates. Updates cause a re-render.
- **Render** = React calling the component function to decide UI.
- **Re-render** = calling it again after props/state/parent changes.
- Each render is a **snapshot**: its own props, state, variables, handlers, effect callbacks. React does not edit the old render; it creates a new one.
- **Closure**: a function remembers values from the render where it was created.
- UI uses the newest snapshot. Old timers, promises, handlers, and effects can still hold older values.

## Mental model

Wrong: “run code after render.”

Better: **synchronize something outside React with the current render** (API, timers, listeners, websockets, localStorage, document title, third-party libs).

```text
props/state change
→ React re-renders
→ each render has its own snapshot
→ after render, React compares effect deps
→ if deps changed: previous cleanup, then new effect
→ effect syncs external work with the latest render
```

`useEffect` does **not** cause re-renders.

```text
Wrong:  dep changes → useEffect re-renders
Right:  props/state change → re-render → then effect may run
```

If there is no external system, ask: can this happen during render or in an event handler?

```tsx
// unnecessary
useEffect(() => {
  setFullName(firstName + " " + lastName);
}, [firstName, lastName]);

// during render
const fullName = firstName + " " + lastName;
```

## Dependency arrays

After every render, React compares current deps to the previous render. If at least one changed, the effect runs.

| Array | Meaning |
| --- | --- |
| omitted | after every render |
| `[]` | after first mount (Strict Mode may run twice in dev) |
| `[roomId, userId]` | after first render, then when those values change |

Deps are **correctness**, not vibes. Include every value the effect **reads**. Ask: what does this effect read, and what should happen when each value changes?

Two failure modes:

- **Missing deps** → old snapshot stays alive (stale sync).
- **Unstable deps** (new object/fn every render) → effect restarts too often.

```tsx
// missing: UI can show new roomId while still connected to the old one
useEffect(() => {
  const connection = createConnection(serverUrl, roomId);
  connection.connect();
  return () => connection.disconnect();
}, []);

// honest
useEffect(() => {
  const connection = createConnection(serverUrl, roomId);
  connection.connect();
  return () => connection.disconnect();
}, [serverUrl, roomId]);

// unstable: new object every render → effect restarts every render
const options = { serverUrl, roomId };
useEffect(() => {
  connect(options);
}, [options]);
```

## Cleanup

Return a function from the effect. React runs it **before the effect reruns** (deps changed) or **on unmount**. The external system does not trigger cleanup — React does.

```text
roomId A → B
→ cleanup old effect (disconnect A)
→ run new effect (connect B)
```

```tsx
function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    const connection = connectToRoom(roomId);
    return () => connection.disconnect();
  }, [roomId]);

  return <h1>Room: {roomId}</h1>;
}
```

Timer: effect may run once (`[]`); the interval callback still fires every N ms. Cleanup `clearInterval` so it does not keep running after unmount.

## Stale closures

The UI can show the latest value while an old effect/callback still uses an older one.

```tsx
function Example({ siteId }) {
  useEffect(() => {
    console.log("Effect sees:", siteId);
  }, []);

  return <div>{siteId}</div>;
}
```

```text
siteId A → effect captures A
siteId B → UI shows B, empty deps so effect does not rerun, still remembers A
```

## Refs

A **ref** is a box that survives renders. Updating `.current` does not re-render.

- `ref.current = fn` → save
- `ref.current?.()` → call whatever is saved

Old callbacks can read `ref.current` instead of the value they closed over.

```tsx
const latestRoomIdRef = useRef(roomId);
useEffect(() => {
  latestRoomIdRef.current = roomId;
}, [roomId]);

setTimeout(() => console.log(latestRoomIdRef.current), 5000);
```

## Real example: `useReactiveValidation`

Hook: `apps/eip-next/src/app/(app)/workflows/_hooks/use-reactive-validation.ts`

Consumer: Top-Down Advanced Settings form.

User edits fields → clear old issues → wait (debounce, ~500ms) → server validation → show errors/warnings.

**Split of responsibility:** form owns *what* validation means (`validateStep` via `useCallback`). Hook owns *when* to run it.

**Trigger values** (main effect deps — should rerun validation): `validate`, `enabled`, `debounceMs`

**Fresh callbacks** (refs — latest version, should *not* retrigger validation): `onClearErrors`, `onSetErrors`

Those callbacks are inline in the parent, so they get a new identity every parent render. Putting them in the main dep array would cause validation storms. `validateStep` is `useCallback`’d, so it changes when form fields / `tdiName` change — that *is* the signal to validate again.

```tsx
// Effect 1: keep latest callbacks in refs (does not clear errors)
useEffect(() => {
  onClearErrorsRef.current = onClearErrors;
  onSetErrorsRef.current = onSetErrors;
}, [onClearErrors, onSetErrors]);

// Effect 2: orchestration
useEffect(() => {
  onClearErrorsRef.current?.();

  if (enabled && onSetErrorsRef.current) {
    validationTimeoutRef.current = setTimeout(async () => {
      try {
        const result = await validate();
        onClearErrorsRef.current?.();
        onSetErrorsRef.current?.(result.errors, result.warnings);
      } catch {
        // keep previous validation state
      }
    }, debounceMs);
  }

  return () => clearTimeout(validationTimeoutRef.current);
}, [validate, enabled, debounceMs]);
```

```text
form field changes
→ validateStep identity changes
→ main effect reruns
→ cleanup cancels old timeout
→ clear old errors
→ new 500ms timer
→ if user types again, repeat
→ on pause: await validate(), then set errors/warnings
```

Naive version (`[]` + no debounce/cleanup/refs) only validates the **first render**. Looks fine on load; breaks when the user edits.

## Async races

Debounce cleanup cancels the **pending timeout**, not an **in-flight request**.

```text
Request A (old values) starts
user edits → Request B starts
B finishes, UI is correct
A finishes later and overwrites newer state
```

Debounce prevents extra requests from starting. Once a request is in flight, still need `AbortController`, request ids, or ignoring stale results.

## Tradeoffs

Keep the effect **local** when it is small and isolated (`document.title = pageTitle`).

Move to a **custom hook / data layer** when it repeats or has debounce, cleanup, races, retries, caching. Risk: the hook hides dep behavior.

## Review questions

- Am I syncing an external system, or just organizing code?
- Are deps honest, complete, and stable?
- Can late async work overwrite newer state? Does cleanup cancel timers only, or requests too?
- Would this be simpler during render or in an event handler?
- Local effect vs hook vs data-fetching abstraction?

## Corrected misunderstandings

| Wrong | Right |
| --- | --- |
| `useEffect` tracks deps and causes re-renders | Re-render first, then the effect may run |
| `[]` means every refresh / every render | Runs after mount. A browser refresh remounts the app, so it runs again |
| Cleanup is triggered by the external system | React runs cleanup on dep change or unmount |
| First effect in `useReactiveValidation` clears errors | It only updates callback refs. The second effect does the work |
| `onClearErrors` / `onSetErrors` change because the hook calls them | They change because the parent recreates inline functions |
| `validateStep` changes every render like those callbacks | It is `useCallback`’d; it changes when its deps change |
