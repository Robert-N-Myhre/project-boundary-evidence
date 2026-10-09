# Source Manifest

This manifest records where the staged public evidence came from in the private Boundary project.

The public package does not link to the private repository. Paths and commit identifiers are preserved so the repository owner can reconcile a public copy against the original source.

## Source cutoffs

- Final project-state source: `019df210c273fb8a2da4d9141ef5def6531dab8e`
- M5.2 contemporaneous authority source: `0dbf50b6ab0b21d67cef07daa301c254f45bdd92`

## Architecture decisions

| Public file | Private source |
|---|---|
| `decisions/architecture-change-31.md` | `docs/ARCHITECTURE-CHANGES.md`, lines 797–872 at final cutoff |
| `decisions/architecture-change-35.md` | `docs/ARCHITECTURE-CHANGES.md`, lines 1074–1179 at final cutoff |
| `decisions/architecture-change-39.md` | `docs/ARCHITECTURE-CHANGES.md`, lines 1411–1487 at final cutoff |
| `decisions/architecture-change-41.md` | `docs/ARCHITECTURE-CHANGES.md`, lines 1551–1648 at final cutoff |

All four public decision files are verbatim range copies.

## Executable validation

| Public file | Private source | Private blob SHA |
|---|---|---|
| `validation/test_acquisition_floor.py` | `tests/orchestrator/test_acquisition_floor.py` at final cutoff | `41cc514a9e2872e791bcc3eb81d698860571b631` |
| `validation/test_recovery_decision.py` | `tests/orchestrator/test_recovery_decision.py` at final cutoff | `f246f0447b4491e8314e1939986d7a7bd229ccb6` |

Both test files are complete verbatim copies.

## Acquisition-floor evidence

All source files below come from `data/runs/` at the final project-state cutoff.

| Public stem | Private run |
|---|---|
| `before-agent-discretionary.*` | `01KZMQ3378D4TFBW5YBJQB43N8` |
| `after-conflict.*` | `01KZPD8K7N78CGRZSD6DXJ9SJT` |
| `after-missing-host.*` | `01KZPD8K7NCSSHXTC6ZVADS9QV` |
| `after-clean-control.*` | `01KZPD8K7N95GC9236NKQPKTC3` |

JSON artifacts are verbatim copies. Each `.terminal.jsonl` file contains an exact selected terminal record from the corresponding private `.log`; it is not a reconstructed summary.

`evidence/acquisition-floor/finding-f9-f10.md` is a verbatim copy of `RESEARCH_NOTES.md` lines 404–481 at the final cutoff.

## Authority-matrix evidence

Raw authority artifacts come from the M5.2 contemporaneous source commit.

| Public file | Private source |
|---|---|
| `standing-authorized.authorization-decision.json` | `data/runs/01M18ANACBDE16YHF18JWK8A13.authorization-decision.json` |
| `standing-authorized.waveplan-verified.json` | `data/runs/01M18ANACBDE16YHF18JWK8A13.waveplan-verified.round1.json` |
| `standing-authorized.authorization-gate.jsonl` | exact selected gate + terminal records from `data/runs/01M18ANACBDE16YHF18JWK8A13.log` |
| `advisory.waveplan-verified.json` | `data/runs/01M18ANACCFJVEF88W2NPY71FA.waveplan-verified.round1.json` |
| `advisory.authorization-gate.jsonl` | exact selected gate + terminal records from `data/runs/01M18ANACCFJVEF88W2NPY71FA.log` |
| `no-covering-envelope.planning-referral.jsonl` | exact selected terminal record from `data/runs/01M18ANACCXDA8RKPBBZ660MPQ.log` |

`m5.2-live-acceptance.md` is a verbatim copy of `PROGRESS.md` lines 703–776 at the final cutoff, preserving both the live acceptance and the F21 limitation found during close.

## Recovery and project stop state

- `evidence/recovery/m6.3-live-walk.md` — verbatim `PROGRESS.md` lines 1066–1160 at final cutoff.
- `evidence/project-stop-state.md` — verbatim `PROGRESS.md` lines 1162–1207 at final cutoff.

## Curated material

README/index files are publication-layer interpretation written during the harvest. They are intentionally separate from the raw/source evidence above.
