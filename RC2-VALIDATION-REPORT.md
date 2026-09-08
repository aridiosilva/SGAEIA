# SGAEIA RC2 Working Candidate — Validation Report

**Date:** 2026-09-08  
**Scope:** Alien Cognition and Architectural Assurance implementation increment  
**Baseline preservation:** v0.3.4 remains the immutable public citation baseline. The RC2 increment was applied only to an isolated feature branch; `main`, tags and releases remain unchanged.

## Results

| Validation | Result |
|---|---|
| `python -m pytest -q` | PASS — 51 tests |
| Specification validator | PASS |
| Integration Port validator | PASS |
| Public-release structural validator | PASS against inherited v0.3.2 code baseline |
| Adapter conformance harness | PASS — 9 profiles |
| Python compilation | PASS |
| Control API trust-boundary tests | PASS — client security claims rejected |
| OpenAPI/schema/traceability gates | PASS |
| Dependency warnings | 2 upstream FastAPI/Starlette deprecation warnings; no test failure |

## Assurance boundary

These results are local repository-level evidence. They are not production
certification, live adapter assurance, cyber-range results, proof of alignment,
or proof of safety. TLA+ and Alloy model-checker execution is not claimed.

## Provenance qualification

The implementation increment originated from the historical v0.3.2 RC1 package.
Before publication, the changed paths were compared with the current canonical
repository, applied to the current `main` commit and validated again. The public
citation baseline remains v0.3.4; this RC2 branch is an unreleased candidate.

Paper integration is outside this software RC2 validation increment. The
authoritative 13-page Paper 01 v3 source is synchronized separately and remains
the baseline for a future, explicitly reviewed Alien Cognition manuscript
revision.
