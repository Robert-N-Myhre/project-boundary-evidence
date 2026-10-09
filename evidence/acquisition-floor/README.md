# Deterministic Acquisition Floor — Before/After Evidence

This packet preserves the strongest live before/after finding in Boundary.

The deterministic scope-admission gate already knew how to detect a Source-of-Truth/live-facts conflict. The architectural flaw was that the reasoning agent controlled whether both inputs were retrieved.

## Before — gate exists, evidence does not arrive

Run `01KZMQ3378D4TFBW5YBJQB43N8` (2026-08-10) targeted `app-db-02`.

The selected proposal artifact shows **one tool call**: `sot_host_by_name`. It records RHEL 9.2 from the governed Source of Truth. No live-facts call exists in the invocation.

The selected accepted-scope artifact records:

- `fields_corroborated: 0`;
- telemetry `ABSENT`;
- the OS mapping accepted from the Source-of-Truth evidence that was available.

The exact selected terminal log record in [before-agent-discretionary.terminal.jsonl](before-agent-discretionary.terminal.jsonl) records `scope_admission: ACCEPT_SCOPE`.

The contemporaneous [F9/F10 finding record](finding-f9-f10.md) records that the fixture stores simultaneously held different live facts for the same host. The gate did not fire because its second input was never acquired.

## Architecture change

[Architecture Change 31](../../decisions/architecture-change-31.md) moved gate-required evidence acquisition to deterministic orchestration before reasoning.

The rule did **not** remove discretionary model investigation. It created a minimum acquisition floor for the evidence a deterministic defense already required.

## After — same conflict class is now reachable

Run `01KZPD8K7N78CGRZSD6DXJ9SJT` exercised the conflict after Change 31.

The selected proposal artifact records two calls with `acquisition_origin: "floor"`:

1. Source of Truth: RHEL 9.2.
2. Live facts: RHEL 9.4.

The terminal record preserves the resulting `REFER_TO_SME` decision and a first-class `conflict` finding containing both values and both evidence positions.

This is **LIVE-DEMONSTRATED** evidence that the previously unreachable conflict defense became reachable when the control owned its minimum evidence.

## Missing-host arm

Run `01KZPD8K7NCSSHXTC6ZVADS9QV` demonstrates the other F9/F10 failure direction. The floor records Source-of-Truth absence, still performs the live-facts read, and the gate refers `insufficient_evidence` without depending on the reasoning agent to discover the absence.

## Clean control

Run `01KZPD8K7N95GC9236NKQPKTC3` is the clean control: both floor calls are present, the comparable OS field corroborates, and scope admission accepts.

## Executable evidence

The original [test_acquisition_floor.py](../../validation/test_acquisition_floor.py) separately pins the invariant with executable negative paths. It is deterministic test evidence, not a substitute for the live before/after records.

## Limits

These runs show reachability and causal architecture behavior in the Boundary prototype. They do not establish production rates, availability, or that the correct evidence floor can be inferred automatically for arbitrary future controls.
