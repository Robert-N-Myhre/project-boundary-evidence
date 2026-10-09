## Project ended 2026-10-08 (Robert's ruling: harvest the repo, build stops here)

Robert ended the project on 2026-10-08: the architectural work he wanted is
captured and further build is diminishing returns. The harvest itself happens
in a separate repository and is out of scope for this one. This entry records
the stop-state so a reader does not mistake unfinished for finished.

**Last closed slice: M6.3** (2026-09-10, live-accepted). Everything above this
entry stands as recorded.

**M6.4 is BUILT, NOT ACCEPTED.** The build (04e920a, realizing #42 and its
addendum) and the walk roster (cbd349d) are committed; the suite stood at 3107
with 1 operator-side skip at the build commit. The live acceptance walk never
ran: the simulated world was reseeded on 2026-09-11 at 21:52Z for it, and no
run exists after run D (01M26CWR6R, 2026-09-10). Every M6.4 claim is therefore
deterministically proven only, none live-observed. BUILD_PLAN's M6.4 box stays
unticked on purpose.

**Never started:** M6.5 (the Validation Anomaly Agent and 6B telemetry), M6.6
(the verdict on the ledger), M6.7 (the real-Ansible adapter), M6.8 (the
Milestone 6 close), and Milestone 7 (Phase 7, outcome and learning).

**Architecture state:** v3.4 is the last release. Changes #32 through #42 are
Agreed in ARCHITECTURE-CHANGES.md and were never folded into a release, so the
current architecture is v3.4 read together with those eleven entries. The
guardrails and the PDO register conform to v3.4 only; the guardrails 1.5
recovery-decision clause and the #38/#39 flags were owed to the next release
and remain owed.

**As-built coverage:** phases 1 through 4. Phase 5 (M5, M6.1 through M6.3) and
the unaccepted 6A work have no as-built; their record is this file's slice
entries.

**Abandoned as recorded, not resolved:** every item under "Standing queues and
parked items" (the two-real-VMs trial, the batched models-up research session,
the M5.3 audit carry-forwards, the parked items), the boot_prior_kernel capture
debt, the confidence-gated category auto-accept finding, and the open M5 and M6
teach-backs.

**Evidence housekeeping:** data/sim-estate.retired-20260911T215214Z is
committed with this entry. It is the world retired by the M6.4 pre-walk reseed,
so it holds run D's end-world (the failed patch on web-prod-01 with the
recovery aborted at boot).

**Machine state at close:** orchestrator daemon, both model servers, and the
web app stopped on 2026-10-08. Branch pushed to origin.