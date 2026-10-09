# Evidence Index

This index maps the main public Boundary claims to the smallest useful set of supporting material.

| Claim | Evidence status | Selected evidence | What it establishes | Important limit |
|---|---|---|---|---|
| A deterministic control must own reliable access to the evidence it needs. | **LIVE-DEMONSTRATED + DETERMINISTICALLY-VALIDATED** | [Acquisition-floor packet](acquisition-floor/README.md), [Architecture Change 31](../decisions/architecture-change-31.md), [test_acquisition_floor.py](../validation/test_acquisition_floor.py) | Before the change, a live run accepted despite a standing SoT/live-facts conflict because only one side was fetched. After the change, the same conflict class had both inputs acquired before reasoning and referred. | Prototype/lab evidence; it does not establish production reliability or that every future gate has the correct evidence minimum. |
| Governance of a source and semantic trust of every field are different properties. | **LIVE-DEMONSTRATED + ARCHITECTURE/DECISION EVIDENCE** | [Architecture Change 35](../decisions/architecture-change-35.md), acquisition-floor artifacts, authority-matrix artifacts | The project distinguished requester declarations, model inference, governed structured facts, free-form prose, provenance, screening, and verification rather than assigning one trust level to an entire source. | The public package does not publish the complete screening corpus or claim reliable detection of all hostile content. |
| Autonomy is an enterprise authority posture, not a model capability switch. | **LIVE-DEMONSTRATED + DETERMINISTICALLY-VALIDATED** | [Authority-matrix packet](authority-matrix/README.md), [Architecture Change 39](../decisions/architecture-change-39.md) | One active portfolio produced standing-policy authorization for one workload, Advisory for another, and refusal for uncovered work. | Boundary did not complete the promotion-evidence loop required for a full earned-autonomy lifecycle. |
| Advisory means useful work can exist without mutation authority. | **LIVE-DEMONSTRATED** | [Advisory gate record](authority-matrix/advisory.authorization-gate.jsonl) and its verified plan | The gate explicitly produced no authorization decision because the effective lane was Advisory; nothing was authorized or executed. | Advisory usability was demonstrated; long-term enterprise workflow and promotion evidence remained incomplete. |
| Recovery that mutates state requires separate authorization. | **LIVE-DEMONSTRATED + DETERMINISTICALLY-VALIDATED** | [Recovery packet](recovery/README.md), [Architecture Change 41](../decisions/architecture-change-41.md), [test_recovery_decision.py](../validation/test_recovery_decision.py) | The project created a per-act recovery decision bound to the verified plan/strategy; live runs exercised refusal, successful recovery, and failed recovery. | Several recovery arms remained deterministic-only, and later validation phases were unfinished. |
| The project stopped at diminishing architecture return rather than production completion. | **CONTEMPORANEOUS PROJECT RECORD** | [Project stop state](project-stop-state.md) | The final record explicitly distinguishes the last live-accepted slice, built-but-unaccepted deterministic validation, and work never started. | This is a stopping/coverage record, not proof that remaining production obligations were solved. |

## Reading raw evidence

Files under `acquisition-floor/` and `authority-matrix/` are selected original prototype artifacts or exact selected JSONL records. They have not been rewritten into illustrative examples.

The adjacent README explains why each file is present. Interpretation lives in the README; evidence remains evidence.

## Evidence not included in the first public cut

Boundary also produced measured semantic-screening research, as-built reconciliations for phases 1–4, execution-probe captures, mutation-test records, and many additional run artifacts. Those remain private in the first cut because the evidence above is sufficient to support the flagship public claims without recreating the engineering archive.
