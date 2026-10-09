- **2026-08-10 — F9: the conflict defense is live-unreachable while acquisition breadth is
  agent-discretionary (M2.9 walk, run `01KZMQ3378D4TFBW5YBJQB43N8`).** The admission gate
  detects hard-fact conflicts only "from those same records", the recorded tool results of
  the invocation. The walk's conflict probe named app-db-02 (SoT os 9.2, live facts 9.4, the
  seeded reconcile specimen) and the agent made exactly one SoT call, never fetched live
  facts, and the run ACCEPTED with the conflict standing in the stores
  (`fields_corroborated: 0` and telemetry-absent honestly derived on the record, which is
  the day-one matrix working as ruled: corroboration is a derived dimension, not a minimum).
  Two structural facts complete the chain: the agent at temp 0 fetches one exact-name lookup
  per contract-named host across every live run on disk, and requester text cannot widen
  acquisition, because intake's field extraction reduces the description to a bare objective
  before the agent sees it (measured: a verify-against-live-facts sentence in the request
  never survived into the contract). That stripping is an injection-resistance property
  worth keeping; its cost is that no legitimate steering channel exists either. **Observed
  once as a full accept-with-standing-conflict; the one-SoT-call-per-host pattern is
  consistent across all live Phase 2 runs.** Not fixed, deliberately (patch-over-redesign
  is how v1 died): the design question is acquisition policy itself, queued for the
  pre-Phase-3 pass together with F10, with the deterministic-acquisition option (an
  orchestrator pre-pass fetching SoT record and live facts for every contract-named host,
  the gate deciding from recorded absence) named as the grain-following candidate.
  **Ruled 2026-08-10 (Robert, pre-Phase-3 pass): the deterministic acquisition floor,
  ARCHITECTURE-CHANGES #31.** Gate-consumed evidence is orchestrator-acquired through
  the CAG pre-pass; the conflict defense fires from guaranteed inputs. Implementation is
  the dedicated Phase 2 rework slice after the v3.4 release cuts.
  **Closed 2026-08-10 at the M2.10 live acceptance (run `01KZPD8K7N78CGRZSD6DXJ9SJT`):**
  the same conflict probe content that ACCEPTED at the M2.9 walk now refers, live. The
  floor fetched both records (SoT os 9.2 at call 1, live facts 9.4 at call 2), the gate
  detected the disagreement and referred `conflict` with both values kept on the
  finding. First live firing of the conflict arm ever. The clean control
  (`…QPKTC3`, web-prod-01) accepted with 1 corroborated field, where every pre-floor
  live run derived `fields_corroborated: 0`.

- **2026-08-10 — F10: on an absent host, the agent guess-probes attribute values to
  feedback exhaustion instead of proposing the NO_DATA gap (M2.9 walk, runs
  `01KZMRJ5MJ8RHZMWN4HQP6KMHG` and `01KZMRN956NTZDJ7P8ZXYFHHC1`).** Both probes (the ghost
  web-cache-06 and the never-seeded app-report-01): the exact-name lookup returned a legal
  empty, correctly recorded, and the agent then issued `sot_hosts_by_attribute` with
  invented relation values four times, burning the F4 feedback bound, and the run failed
  `invalid_call_feedback_exhausted`. It never once proposed with the NO_DATA gap, although
  the template carries that exact worked example ("named in the request but the Source of
  Truth holds no record under that name"). **0 for 2 on distinct hostnames; nothing was
  fabricated in either run (the anti-fabrication invariant held).** Consequences: the
  `insufficient_evidence` referral reason and the amend-source SME exit are live-unreachable
  at temp 0, and an absent-host request (a requester typo included) dead-ends as a
  processing failure with a CANCEL-only exit. Suspected contributor, unmeasured: the F4
  rejection feedback's own wording ("the argument values are yours to re-examine") invites
  another guess; left unfixed because its effect size is unknown and the channel may not
  survive the acquisition-policy design change. A durable-record limitation noted in
  passing: rejected calls' argument VALUES are deliberately excluded from stage accounts
  (M1.8 minimization), so whether the agent varied its guesses is unknowable from the
  record. Deferred measurement, batched with the F5/F7 research runs: a template not-found
  rule ("if an exact-name lookup returns no record, do not guess attribute values; record
  the NO_DATA gap and propose") and feedback-wording variants, measured for effect size, so
  the cheap fix earns its way in through adjustment governance if it works. The design
  question travels with F9 to the pre-Phase-3 pass: under deterministic acquisition the
  not-found case never depends on agent behavior at all.
  **Ruled 2026-08-10 (Robert, pre-Phase-3 pass): ARCHITECTURE-CHANGES #31.** The floor
  records SoT and live-facts absence deterministically and the gate composes the
  `insufficient_evidence` referral from recorded absence, making the amend-source exit
  reachable without agent cooperation. The cheap-fix experiments (template not-found
  rule, feedback wordings) stay in the batched research runs and gate nothing; the
  feedback-wording channel may not survive the rework.
  **Closed 2026-08-10 at the M2.10 live acceptance (run `01KZPD8K7NCSSHXTC6ZVADS9QV`):**
  the ghost web-cache-06 referred `insufficient_evidence` live, from the floor's
  recorded absence. An unexpected second result, observed once and worth its own line:
  with the floor's absence evidence in its FIRST data block, the agent proposed in one
  round with zero rejected calls and carried the NO_DATA gap, the exact behavior this
  finding measured as 0-for-2 under guess-probing. The deterministic referral no longer
  depends on that behavior, but the behavior itself appears to have been an
  evidence-starvation artifact rather than a model disposition (n=1 live; the batched
  F10 template experiment can still measure it properly, though its motivating failure
  mode is now closed). Known cosmetic residual, deliberate: the referral carries two
  `insufficient_evidence` findings for the same host, one from the floor's absence rule
  (proposal-level) and one from the per-host minimum-evidence rule (the agent proposed
  the ghost, citing the floor's own empty lookup, and no SoT evidence exists for it);
  each names its own rule in its detail, and collapsing them would hide which defense
  fired. The feedback-exhaustion halt remains reachable pre-gate in principle and is
  named as a residual in BUILD_PLAN M2.10; it did not occur in the acceptance run.