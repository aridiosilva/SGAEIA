# SGAEIA RC2 Working Candidate — Validation Report

**Date:** 2026-09-08  
**Scope:** Alien Cognition and Architectural Assurance implementation increment  
**Baseline preservation:** v0.3.4 remains the immutable public citation baseline. The RC2 increment was applied only to an isolated feature branch; `main`, tags and releases remain unchanged.

## Results

| Validation | Result |
|---|---|
| `python -m pytest -q` | PASS — 38 tests |
| Specification validator | PASS |
| Integration Port validator | PASS |
| Public-release structural validator | PASS against inherited v0.3.2 code baseline |
| Adapter conformance harness | PASS — 9 profiles |
| Python compilation | PASS |
| Paper integration draft compilation | PASS — 6 pages, no unresolved citations |
| Paper visual inspection | PASS for the integration draft |

## Assurance boundary

These results are local repository-level evidence. They are not production
certification, live adapter assurance, cyber-range results, proof of alignment,
or proof of safety. TLA+ and Alloy model-checker execution is not claimed.

## Provenance qualification

The implementation increment originated from the historical v0.3.2 RC1 package.
Before publication, the changed paths were compared with the current canonical
repository, applied to the current `main` commit and validated again. The public
citation baseline remains v0.3.4; this RC2 branch is an unreleased candidate.

The available Paper 01 source is a six-page historical source. The frozen arXiv
candidate is a separate v3 manuscript with 13 pages and three figures. The RC2
paper changes are therefore a compiled integration draft, not a replacement for
the frozen v3 package. They must be merged into the authoritative v3 sources and
visually compared before arXiv submission.
