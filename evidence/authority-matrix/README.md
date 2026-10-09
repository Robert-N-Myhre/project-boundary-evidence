# Authority Portfolio — Three Live Outcomes

This packet supports the claim that Boundary represented autonomy as a governed authority posture rather than as a model capability switch.

The M5.2 live acceptance used one orchestrator with multiple active bounded policy envelopes and produced three distinct outcomes.

## 1. Standing-policy authorization

Run `01M18ANACBDE16YHF18JWK8A13` was tier-3 routine work.

[standing-authorized.authorization-decision.json](standing-authorized.authorization-decision.json) is the original authorization artifact. It binds authorization to:

- a verified plan digest and plan reference;
- simulation execution mode;
- a named operation class;
- a named policy;
- a named standing grant.

The exact selected gate record in [standing-authorized.authorization-gate.jsonl](standing-authorized.authorization-gate.jsonl) records `effective_lane: policy_authorized`, `standing_eligible: true`, and `POLICY_AUTHORIZED`.

## 2. Advisory — verified work without mutation authority

Run `01M18ANACCFJVEF88W2NPY71FA` produced a verified plan for tier-2 work.

The exact gate record in [advisory.authorization-gate.jsonl](advisory.authorization-gate.jsonl) explicitly records:

- `effective_lane: advisory`;
- `standing_eligible: false`;
- `ADVISORY_DELIVERED`;
- an **absent authorization decision**, because Advisory is not standing mutation authority.

The terminal record says `authorized: false`, `decision_id: null`, and that nothing was authorized or executed.

The absence of an authorization-decision file is therefore part of the evidence, not missing data.

## 3. No covering envelope — refuse before reasoning

Run `01M18ANACCXDA8RKPBBZ660MPQ` matched no active policy envelope for the workload's tier/dependency class combination.

The exact record in [no-covering-envelope.planning-referral.jsonl](no-covering-envelope.planning-referral.jsonl) shows:

- `planning_referred`;
- `no_covering_envelope`;
- every active envelope's excluding bound named;
- no plan artifact and no authority path.

## Architecture decision

[Architecture Change 39](../../decisions/architecture-change-39.md) is the contemporaneous decision that generalized one active envelope into a non-overlapping portfolio with deterministic cover selection and refusal rather than tie-breaking.

[m5.2-live-acceptance.md](m5.2-live-acceptance.md) is the contemporaneous milestone record for the three-run live walk. It also preserves the F21 limitation discovered at close: Advisory did not yet produce the evidence needed for a complete earned-autonomy promotion lifecycle.

## Limits

This packet demonstrates governed lanes and policy coverage in the prototype. It does not establish a production policy lifecycle, statistically justified promotion thresholds, or a complete earned-autonomy lifecycle.
