## 35. Declared fields keep declared provenance: the operator-intent class is honored per field

**Status:** Agreed, 2026-08-17

Rules the defect #34's gate check surfaced and Robert's challenge named: the intake
pipeline collapses v3.4 section 9.3's "authenticated operator intent" trust class into
the untrusted-free-text class for every structured field except `requested_by`. A
requester-typed category is serialized into the prepared content, re-extracted by the
Intake Understanding Agent, and recorded on the contract as a model inference with a
grounding quote. Measured on the committed estate before this entry: across all 39
accepted contracts, every field except requested_by carries `prepared_content`
provenance, including runs whose submission form supplied the value.

**The rule.** A field the requester supplied on the submission form enters the intake
contract authored by CODE, value taken from the submission record, with `form_field`
provenance, exactly as `requested_by` has since M1.8. The agent infers only what was
left blank: inference is the fallback for absence, never the override of a declaration.
This applies to every declarable form field (category, configuration item, change type,
priority, planned window), not to `objective`, which has no form field and is always
the agent's interpretation of the messy input. The #1/#7/#13 optional-fields design is
unchanged: blank fields still flow to inference with inference provenance.

**What declared provenance does and does not mean.** It records WHO established the
value; it never upgrades whether the value is true or safe. A declared configuration
item is still screened as content and still Phase 2's to verify against the Source of
Truth. Downstream consumers (M3.5's change-class check first) may distinguish
declaration from inference; nothing may read "declared" as "verified".

**Validation follows the existing form path.** Declared fields are verified by
equality against the submission record (M1.9's existing form_field machinery,
generalized), with `verification: None` because there is no quote to verify. A
declared field can never be gapped: a model-proposed gap for a field the requester
declared is dropped at composition, because nothing is absent.

**Residual, named rather than hidden.** A form dropdown is a weaker declaration than a
confirmation round: a requester who accepts a prefill unread has still "declared" it.
Closing that residual is #34's Phase 1 clarification rule, which remains its own slice.
This entry is the first half of #34's realization and the precondition for M3.5's live
acceptance proving a verified plan on the real pipeline.

**No prompt change.** The IUA template stays byte-identical (#29: no new prompt
version). The model may still propose values for declared fields; composition prefers
the declaration, and the proposal remains durably recorded on the invocation's stage
accounts as what it was.

**Correction, 2026-08-17 (same day, pre-implementation, from the slice's adversarial
review).** Three claims in this entry were wrong or unsupported; the rule stands, the
mechanism description is corrected:

1. **The enum fields are discarded, not laundered.** Content preparation's field order
   is shortDescription, description, and configurationItem ONLY: a requester-typed
   category, change type, priority, or planned window never reaches the prepared
   content at all. The model proposes those fields from the description prose alone,
   and the form value is thrown away entirely. The defect is therefore WORSE than this
   entry stated for those fields (a declaration discarded, not demoted), while the
   laundering description is accurate only for configuration_item, which IS part of
   prepared content and does return via model quote.
2. **The measurement claim was overstated.** All 39 accepted contracts do carry
   inference provenance on every field but requested_by, but none of the 7 submissions
   that declared a field ever reached acceptance, so "including runs whose submission
   form supplied the value" was unsupported by the estate and is withdrawn. A fresh
   declaring submission is required to exercise the new path live.
3. **The superseded-proposal durability claim was false as written.** Nothing today
   records a model proposal that composition declines: the success account's contract
   block is built from the composed contract, and raw model output is deliberately
   never echoed. Preserving the superseded proposal (and any dropped gap's reason,
   verbatim) on the composition account is therefore a BUILD ITEM of the realizing
   slice, not an existing property.

**Revision, 2026-08-17 (Robert's ruling at the step-back design discussion).** The
rule stands unchanged; its realization is expanded from a per-field fix to the full
design, after the narrowing options under review (enum-fields-only, deferrals with
dated notes) were rejected as the same patch shape at a larger scale. The agreed
design, one unit delivered in two stages:

**The design.** Intake is two input channels of different section 9.3 trust classes,
each processed by its own controls, merged honestly. Channel 1, structured
declarations (authenticated operator intent): every structured field the requester
supplies, type-validated at the surface, identity-bound, and, for free text,
canonicalized and redacted by the SAME deterministic pipeline the content gets
(controls attach to the content class, not the author); composed into the contract by
code. Channel 2, unstructured content: screened, prepared, interpreted by the IUA,
which proposes values only for what was not declared. One general provenance shape
carries authorship for both: author class (requester-declared, model-inferred,
system-composed), one or MORE source references (form fields, or quote plus digest),
the transformation applied, and the entry point. Declarations are scoped to human
entry points; machine-submitted declarations (scheduler, api, cli) are a named open
question with no writer today. A model reading that contradicts a declaration is
recorded as an advisory discrepancy on the composition account, never dropped and
never blocking. The lesson on the record: a trust class is realized as a class, not
one consumer at a time; requested_by's special case stood where this design should
have been for twenty slices.

**Stage 1 (unblocks M3.5 live acceptance):** the general provenance shape as a new
arm of the existing provenance union (prior artifacts load unchanged; the legacy
form_field arm remains readable and is documented as the old spelling of the same
author class), declarations-win composition for ALL declarable fields including the
two-source planned window and the canonicalized-redacted configuration_item,
derivation-replay validation per transformation, discrepancy and superseded-proposal
recording, and the M3.5 gate accepting both spellings of declared authorship.

**Stage 2 (completes #34):** the declared-or-confirmed sufficiency rule for
authorization-relevant fields, with the structured clarification response it
requires (a confirmation that re-enters as free text would be re-inferred and would
confirm nothing).
