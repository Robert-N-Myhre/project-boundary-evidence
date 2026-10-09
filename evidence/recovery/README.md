# Governed Recovery — Separate Consequence Authority

This packet supports the claim that Boundary treated recovery as a new consequence-bearing act when recovery could mutate state.

## Architecture decision

[Architecture Change 41](../../decisions/architecture-change-41.md) records the governing decision.

The key architectural distinction is that the original authorization covers the planned operation. A later recovery mutation is authorized by a separate per-act recovery decision, bound to the verified plan and its already-selected recovery strategy. The operator authorizes recovery; the operator does not invent a new mutation at the stop.

## Executable invariant evidence

The original [test_recovery_decision.py](../../validation/test_recovery_decision.py) pins the recovery-decision mechanism. In particular, it proves that:

- a policy-authorized run can receive a distinct recovery authorization;
- recovery authorization is per act;
- reprocessing reuses rather than remints the decision;
- composing recovery authority does not alter the run's original AuthorizationDecision.

## Live acceptance record

[m6.3-live-walk.md](m6.3-live-walk.md) is a verbatim excerpt from the final private project record. In that source record, "live" means the operator-driven integrated prototype using the simulated estate; it does not mean production infrastructure.

It preserves three materially different live outcomes:

- **refused recovery** when mutation could not be proven;
- **successful governed recovery** under a separately composed recovery decision, with recovery actions represented in the ledger;
- **failed recovery** that stopped without submitting the later undo step.

The same record explicitly identifies recovery arms that remained deterministic-only.

## Limits

The public packet does not claim the entire recovery/validation lifecycle was complete. Boundary's final project record says M6.3 was the last live-accepted slice; deterministic validation was built afterward but never operator-accepted. Later anomaly validation, a real execution adapter, and final outcome/learning were not completed.
