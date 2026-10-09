# Selected Executable Validation

These are **original test files copied from the private Boundary implementation**, not simplified examples written for publication.

They are included because they pin architecture invariants that are difficult to evaluate from prose alone.

## `test_acquisition_floor.py`

Private source SHA: `41cc514a9e2872e791bcc3eb81d698860571b631`

The file exercises Architecture Change 31's deterministic acquisition floor. Among other properties, it tests:

- target derivation is bounded;
- the Source-of-Truth and live-facts calls occur in deterministic order;
- Source-of-Truth absence does not suppress live-facts acquisition;
- the floor uses a budget independent from discretionary agent reads;
- budget shortfall halts before model reasoning;
- acquisition defects halt before model reasoning;
- durable call records identify whether acquisition was floor- or agent-originated.

The tests use fixtures/fakes at external seams while exercising the real orchestration and gateway contracts under test. They are **DETERMINISTICALLY-VALIDATED** evidence, not live-system evidence.

## `test_recovery_decision.py`

Private source SHA: `f246f0447b4491e8314e1939986d7a7bd229ccb6`

The file exercises Architecture Change 41's recovery-decision artifact. It pins:

- recovery authorization identity is per human act, not per run;
- decision artifacts are write-once/read-back-first;
- reprocessing does not mint a new authorization;
- a policy-authorized run can still receive a distinct human recovery authorization;
- composing recovery authority never mutates the run's original AuthorizationDecision;
- only the AUTHORIZE_RECOVERY disposition can produce this artifact.

This is **DETERMINISTICALLY-VALIDATED** evidence. The separate [recovery evidence packet](../evidence/recovery/README.md) contains the live acceptance record.

## Why only two test files?

The private project contains a much larger suite. Publishing test count or a broad source dump would make the repository larger without making the important architecture claims easier to inspect.

These two files were selected because each is directly tied to a public architectural turn and contains executable negative-path behavior, not merely happy-path checks.
