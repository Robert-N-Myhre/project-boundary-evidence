## 41. The human operations authority surface: execution stops gain their ruled exits, recovery is a digest-bound human authorization

**Status:** Agreed, 2026-09-08

The three M6.3 fork rulings, realizing the Phase 5 stage doc's human edge
(authorize recovery, abort, or defer) and a deliberate subset of v3.4 section
14.4's execution rows against the six CANCEL-only execution stops M6.2 left.

**Ruling 1 (fork 1, option A): the narrow exit matrix.** AUTHORIZE_RECOVERY
joins exactly the two stops whose section 14.4 rows carry rollback. DEFER, with
the transaction stop's mechanics (a recorded act, sequence advances, halt
persists, later exits remain valid), joins the four interim stops. CANCEL stays
on every stop unchanged and remains the abort/abandon verb.

| Stop | Exits after this change |
|---|---|
| awaiting_wave_validation | CANCEL, DEFER |
| execution_revalidation_refused | CANCEL, DEFER |
| execution_reconcile_required | CANCEL, DEFER, AUTHORIZE_RECOVERY |
| wave_halted | CANCEL, DEFER, AUTHORIZE_RECOVERY |
| execution_engine_failed | CANCEL |
| execution_processing_failure | CANCEL |
| recovery_failed (new, ruling 3) | CANCEL, DEFER |

Deliberately deferred verbs, named rather than dropped: resume-under-recorded-
adjudication waits for M6.4's validation evidence (advancing past a halt with no
validation phase behind it would be evidence-free progression); reconcile-as-a-
correction-act needs a correction artifact contract nobody has designed and is
the recorded middle ground for ruling 3's closed posture; continue-after-
quarantine stays withheld per section 13's day-one rule. execution_engine_failed
keeps CANCEL alone: section 14.4's recover-from-last-durable-state is the
daemon's existing restart re-entry from durable lines, and administrative
release is the operator's hand, both already real.

**Ruling 2 (fork 2, option B): a completed recovery is a phase outcome, not a
run terminal.** The execution line closes rolled_back, remaining waves are dead
(wave progression ends, phase progression continues, so a multi-wave run can
never roll back wave 1 and then patch wave 2), the run flows through Phases 6
and 7 to completion, and the outcome ledger entry carries the recovery in the
execution block's recovery_actions field, which has been held empty-but-present
since M6.2 for exactly this landing. The ledger's charter is what occurred
during approved execution, and authorized work that happened and was then
reversed is precisely the story that must not vanish from the run-level record.
CANCEL still ends runs ledgerless; the cancelled-run precedent is untouched.

**Ruling 3 (fork 3, option A): recovery_failed accepts CANCEL and DEFER only.**
A failed recovery step halts the run at a new recovery_failed stop with the
step's classification on the line. No re-authorization exit exists: the
idempotency key derivation excludes attempt, so a re-issued recovery step
collides with its predecessor's key, and changing key derivation is its own
decision, never a side effect of an exit enum. The consequence was ruled with
open eyes, adversarial reading presented: CANCEL ends the run, lazy claim
release eventually makes the partially-recovered host claimable by a new run,
and the guard against re-mutating a known-bad host is planning evidence (its
facts and patch-ledger history), not the claim, because claims are a
mutation-exclusivity mechanism and not a quarantine. An operator facing a
failed rollback has no governed path that touches the host again in that run;
the recorded future middle ground is the reconcile-correction act above, never
a widened exit set.

**Recorded defaults riding the rulings** (confirmed at the same Q&A):
AUTHORIZE_RECOVERY binds to the verified plan's own selected
recovery_strategy_id, digest-bound the way APPROVE binds the plan; a human
authorizes recovery, never authors one at the stop, and no strategy picker
exists. Every recovery mutation rides compose_authorized_request citing the
recovery decision as its one authorization source. execution_processing_failure
keeps the F8 posture: an infrastructure failure of the phase itself has nothing
to recover.

**Honest scope.** This realizes existing architecture (section 14, the Phase 5
stage doc's human edge); the narrowing to a subset of section 14.4's verbs is a
recorded prototype scope decision, not an architecture change. One item is owed
to the next architecture release: section 14.4's stop table has no row for the
failed-recovery stop its own Phase 5 diagram routes to the human authority, and
ruling 3 supplies that row's content.

**Addendum, agreed 2026-09-08 (surfaced by the M6.3 rev-1 adversarial review).**
The recovery decision is its own governed artifact kind, because the existing
decision machinery structurally cannot carry it: the run's AuthorizationDecision
is one-per-run by design, its composer refuses a second human act beside a
policy-authorized run, and the request composer deliberately takes no alternate
source, so the recorded default ("every recovery mutation cites the recovery
decision as its one authorization source") was ruled but unmechanized. Agreed
mechanism: `<cid>.recovery-decision-<seq>.json`, one per authorizing act (seq is
the authorizing disposition's sequence), write-once, composed only by the
daemon's disposition commit path from a validated human disposition (the same
trust chain as APPROVE, at per-act granularity), read-back-first on
re-processing so a crash between artifact and line re-uses rather than
re-composes. It records actor, bound plan digest, execution mode, strategy id,
wave, host, the prior step's idempotency key, and the disposition it realizes.
Citation rule, never-both preserved: each recovery request cites exactly the
recovery decision (AuthorizationRef's model is already generic and does not
change; a composer path fills it from the recovery decision artifact, never
from free strings); the original patch mutations keep citing the original
decision; the run-level ledger citation is unchanged and recovery_actions rows
cite the recovery decision id. No artifact cites two sources, and the run's
AuthorizationDecision is never touched by any recovery path.
