## 31. The deterministic acquisition floor: gate-consumed evidence is orchestrator-acquired

**Status:** Agreed, 2026-08-10, shipped in v3.4

Rules the acquisition-policy fork queued at the M2.9 walk (findings F9 and F10 in
`RESEARCH_NOTES.md`), the headline item of the pre-Phase-3 design pass. Narrows #19; it
does not repeal it.

**The finding that forced the ruling.** Phase 2's acquisition breadth was entirely
agent-discretionary, and the walk measured the discretion failing in both directions. F9:
the agent at temp 0 issues exactly one exact-name SoT lookup per contract-named host and
has never fetched live facts, so the admission gate's conflict detection, which reads only
"from those same records", accepted a run with a standing SoT/live-facts conflict in the
stores. F10: on an absent host the agent guess-probes invented attribute values to
feedback exhaustion instead of proposing the NO_DATA gap, leaving the
`insufficient_evidence` referral and the amend-source exit live-unreachable. The shared
root: both defenses depended on the agent choosing to fetch their triggering inputs.

**The rule.** Evidence that a deterministic gate or defense consumes is acquired
deterministically. The orchestrator, through the existing Context Acquisition Gateway,
runs a pre-pass (the acquisition floor) before the agent is invoked, fetching the gate's
evidence minimum for every contract-named host. The agent's own tool loop remains, per
#19, for everything that is genuinely judgment: what else to look at. Stated at the
principle level, extending #21's boundary one step deeper:

> A model never holds a source connection, and a defense never depends on discretionary
> model behavior for its inputs. Deterministic code executes every call, and
> deterministic code decides the calls a gate's evidence depends on.

**Floor contents scale with the gates, not the estate.** The floor is one entry per gate
input class, currently two: the SoT record and the live facts for each contract-named
host. Adding an MCP server or roster tool adds discretionary capability, never floor
entries; a floor entry is added only when a ruling gives a gate a new evidence input, as
part of that same ruling. A defense found starving (the F9 pattern) graduates its input
into the floor through a measured finding and a ruling, the adjustment-governance shape.

Sub-rulings, all agreed with the entry:

- **Floor scope:** per contract-named host, one exact-name SoT lookup and one live-facts
  fetch. Each store's absence is a legal recorded outcome; SoT-absent does not skip the
  live-facts fetch, both absences are recorded.
- **Deterministic absence disposition:** a contract-named host absent from the SoT
  produces the `insufficient_evidence` referral from recorded absence, no agent
  cooperation required. The amend-source exit becomes reachable.
- **Budget:** floor calls run under their own named bound, outside the agent's tool-call
  budget, so the floor can never starve the discretionary loop.
- **Delivery:** floor results enter the recorded gateway call stream first (positions,
  digests, screening, withholding, identical to agent-issued calls) and are delivered to
  the agent so it reasons from them rather than re-fetching; agent-issued calls append
  after the floor's positions. The citation and verification model of #22/#23 extends
  unchanged.
- **Floor membership is a reviewed code change, never loose config** (M1.7's verdict-table
  reasoning: a config edit must not silently starve a defense), and it is governed control
  surface under #29 either way, since floor results shape the agent's context.
- **Corroboration stays a derived dimension day-one.** The floor makes it real; promoting
  it to a gate minimum is a later evidence-backed change under the standing adjustment
  posture.
- **No steering channel is added.** Intake's extraction stripping stays; the floor removes
  the need F9 exposed, and requester text still cannot widen acquisition.
- **F10's candidate cheap fixes stay batched research** (template not-found rule, feedback
  wordings); they gate nothing, and the feedback-wording channel may not survive this
  change.
- **The rule ports to Phase 3 with the boundary of #30:** whatever the orchestrator's
  wave-plan verification consumes is floor-acquired from the governed planning inputs;
  what the Planning & Risk Agent reads beyond that stays discretionary.

Per-failure-mode reading, both directions weighed at the fork:

| Failure mode | Under #19 as shipped (agent-discretionary breadth) | Under the floor, and its bound |
| --- | --- | --- |
| Standing SoT/live-facts conflict on a named host | Observed live (F9): one SoT call, live facts never fetched, run accepted with the conflict standing | Both records or their recorded absence are guaranteed present; conflict detection fires from deterministic inputs |
| Contract-named host absent from the SoT (requester typo included) | Observed live twice (F10): guess-probing to feedback exhaustion, processing-failure dead end, CANCEL-only exit | Deterministic `insufficient_evidence` referral from recorded absence; amend-source exit reachable |
| Adversary counting on evidence never being fetched | The defense is decorative: no steering needed, the agent already declines | The floor does not depend on model behavior at all |
| Over-fetch / unbounded pre-pass growth | Not applicable | Bounded: floor entries exist only for ruled gate inputs, under a named bound, reviewed in code; the estate and roster grow without touching it |
| Judgment moved out of the agent (the #19 concern) | Not applicable | Bounded: the floor is the gate's evidence minimum, which "from those same records" always presumed; discretionary acquisition beyond it remains agent-issued |
