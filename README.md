# Project Boundary — Selected Evidence

This repository is a curated evidence package for **Project Boundary**, an independent architecture investigation into governing consequential enterprise AI.

Boundary used infrastructure automation as a proving ground for two questions:

- **What do I trust a model to consume?**
- **What do I trust the model's reasoning to influence?**

The public [Project Boundary case study](https://robert-n-myhre.github.io/architecture-portfolio/projects/project-boundary/) explains the architecture story. This repository serves a narrower purpose: it publishes selected contemporaneous decisions, raw prototype artifacts, and executable tests that support important claims in that story.

The reusable architecture distilled from the same research is published separately as [Project Sentinel — Governed Agentic Infrastructure Operations](https://robert-n-myhre.github.io/architecture-portfolio/reference-architectures/governed-agentic-infrastructure-operations/).

It is **not** the original engineering repository, a production automation platform, or a complete reproduction kit. The private project accumulated implementation history, experiments, operational scaffolding, and forensic records that would add volume without improving independent review of the architecture.

## Start here

[Evidence index](evidence/README.md) maps public claims to the supporting material.

The strongest evidence packets are:

- [Deterministic acquisition floor](evidence/acquisition-floor/README.md) — a before/after live-system chain showing a deterministic gate miss a standing conflict when the reasoning agent controlled evidence acquisition, followed by the same conflict class being referred after the control owned its minimum evidence.
- [Authority matrix](evidence/authority-matrix/README.md) — three live outcomes from one orchestrator and one active policy portfolio: standing-policy authorization, Advisory with no authorization decision, and refusal when no envelope covered the work.
- [Governed recovery](evidence/recovery/README.md) — the decision record and live-walk evidence behind treating recovery as a separate consequence-bearing act.
- [Executable validation](validation/README.md) — selected original tests that pin two of the architecture's most consequential invariants.
- [Selected architecture decisions](decisions/README.md) — contemporaneous architecture-change entries copied from the private project record.

## Evidence vocabulary

This package distinguishes several evidence levels:

| Label | Meaning |
|---|---|
| **LIVE-DEMONSTRATED** | Exercised through an operator-run integrated prototype path; this label does not mean production deployment. |
| **DETERMINISTICALLY-VALIDATED** | Executable tests, conformance checks, or mutation-style probes establish the named invariant in the prototype. |
| **MEASURED** | Repeated or controlled research produced quantitative or comparative evidence inside a stated population. |
| **IMPLEMENTED-UNCLOSED** | Implementation exists with executable evidence, but planned operator acceptance or milestone closure was not completed. |
| **TARGET / OPEN** | Architecture intent or production obligation without equivalent as-built evidence. |

A successful run establishes that a path occurred. It does not establish production reliability, statistical rates, universal model behavior, or production safety.

## Provenance

The source project was private **Project-Sentinel / Boundary**. The final project-state record used for this package is commit:

`019df210c273fb8a2da4d9141ef5def6531dab8e`

Selected earlier artifacts retain their original run identities and timestamps because those identities are what connect the evidence chain. Hostnames such as `app-db-02`, `web-prod-01`, and `api-prod-01` belong to the project's simulated/lab estate; they are not production estate identifiers.

The package intentionally preserves evidence that contradicts or limits stronger interpretations. See [project-stop-state.md](evidence/project-stop-state.md) for the final record of what remained unaccepted or unbuilt.

## What is intentionally not published

The complete private repository, full run archive, full prompts, environment configuration, private reachability details, exhaustive test suite, internal working transcripts, and forensic authorship reconstruction are not part of this package.

Selected artifacts are included when they materially support an architectural claim. Omission from this repository does not imply that the private project contained no additional evidence.

## Research authorship

AI models and coding agents participated broadly in implementation, testing, review, and alternative development. The project record distinguishes those activities from architecture decision accountability. Selected decision records here preserve contemporaneous wording rather than reconstructing certainty where the original record did not establish it.

**Author:** Robert N. Myhre  
**Project stopped:** October 8, 2026  
**Evidence package curated:** October 2026
