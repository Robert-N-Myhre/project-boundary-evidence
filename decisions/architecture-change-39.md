## 39. The envelope portfolio: covering-envelope selection by declared bounds, overlap unrepresentable

**Status:** Agreed, 2026-08-29

The Milestone 5 planning ruling (fork 2, option A), motivated by F19: the prototype's
single active-envelope pointer means one tier's work can pass at a time, so the
autonomy matrix's core story, different workload tiers proceeding under different
lanes simultaneously, cannot be demonstrated. The architecture's own language is
plural ("the active policy set", "standing policies"); PDO-002 records the lifecycle
obligation. This entry agrees the reference implementation's realization of the
plural.

**The active policy becomes a portfolio.** Activation remains explicit and named
(config lists the active envelope ids; presence in a directory still activates
nothing; each named envelope must still load as status active with an approval
block). Nothing infers membership.

**A run's covering envelope is selected deterministically, before any reasoning, from
the envelope's own declared bounds.** The selection key is what an envelope already
declares it sanctions: authorized change class, allowed tiers, allowed dependency
classes. The run's side of the key is established upstream of planning: the
requester-vouched change class (#34/#35) and the scope's Phase-2-recorded tier and
dependency classes. The planning floor delivers the covering envelope to the agent as
input; verification, precheck, and the authorization gate all evaluate against that
same envelope. A run with ZERO covers refers at planning exactly as an uncovered run
does today: no active envelope sanctions this kind of work, and the remedy is
authoring policy, never approving past it.

**Overlap is unrepresentable at activation, and re-refused at selection.** Two active
envelopes may not claim the same (change class, tier, dependency class) cell: the
loader and the conformance suite refuse an overlapping portfolio at activation, the
same structural move as hostname uniqueness in the Source of Truth. Defense in depth:
the run-time selector independently refuses if it ever computes two covers, so a
defanged activation check cannot silently become first-match-wins. The rejected
alternative (evaluate against all active envelopes, tie-break on multiple passes) is
named and declined because per-run precedence over overlapping policies is exactly
the "multiple valid interpretations of the operating envelope" PDO-002 forbids, and a
precedence order is a widening lever.

**Standing eligibility's letter changes with it.** "The class's envelope_ref equals
the one active envelope" becomes "equals the COVERING envelope for this run". A grant
still binds to one exact envelope version (#38's version pin and the
certificate-expiry model are untouched); what changes is only which envelope the
comparison is made against, now that more than one may be in force.

**Honest scope.** This realizes concurrent sanctioned work classes; it does not build
the production policy lifecycle (authoring, review, publication, revocation remain
git custody per PDO-002's posture). Mixed-tier scopes find no single cover and refer,
consistent with #38's mixed-tier reduction one phase later. Ships with Milestone 5
(M5.2); flagged for the next architecture release alongside the #38 items.

**Clarifications agreed at the M5.2 slice Q&A (2026-08-30), both option A.**

*Fork 1, run-to-class matching under a portfolio.* Matching stays (change class,
tier) alone, preserving #38's M4.3 rationale: a class whose envelope_ref names a
draft still MATCHES runs, so tier-2 work derives its honest day-one Advisory
rather than reporting "no operation class". The new rule is an ACTIVE REGISTER
INVARIANT: at most one operation class per (change class, tier) cell, refused at
load with the colliding cell named, the same make-it-unrepresentable move this
entry applies to envelopes. A consequence, accepted on the record rather than
designed away: a class matched by name for one workload can cover another in the
same cell (the tier-2 api runs match `tier2-db-minor-patching`), and the remedy
is a governed register rename, an operator act, never machinery. The record
always names which class matched.

*Fork 2, the zero-cover record.* A run no active envelope covers refers at
planning, PRE-FLOOR: status `planning_referred`, reason `no_covering_envelope`,
findings enumerating PER ACTIVE ENVELOPE which declared bound excluded the run,
in the policy's own field names. No floor call, no model call, no plan artifact.
Same stop, same resolution loop, same dispositions: one stop with two spellings
would be a taxonomy the operator pays for. A reachable second case is ruled with
it: two envelopes CAN both cover a run whose scope hosts sit in no service group
(the dependency-class conjunct is vacuous there), so that lands the same referral
under reason `ambiguous_cover`, naming both envelopes and the ungrouped hosts.
The system refuses to tie-break between two readings of the operating envelope,
which is PDO-002's own line.
