# SGAEIA RC2 Working Candidate — Validation Report

**Date:** 2026-09-08  
**Scope:** Alien Cognition and Architectural Assurance implementation increment  
**Post-merge state:** RC2 `v0.4.0-rc.1` was integrated into `main` by squash merge of PR #13. The public citation baseline, tags and releases remain unchanged at the immutable `v0.3.4`.

## Results

| Validation | Result |
|---|---|
| `python -m pytest -q` | PASS — 51 tests |
| Specification validator | PASS |
| Integration Port validator | PASS |
| Release/candidate identity validator | PASS — public baseline `v0.3.4`; development candidate `v0.4.0-rc.1` |
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
repository, applied to the current `main` commit and validated again. Package,
OpenAPI and master-spec metadata now identify the unreleased candidate as
`v0.4.0-rc.1`; the public citation baseline remains the immutable `v0.3.4`.

Paper 01 v4 is integrated in `main` as the reviewed manuscript candidate
for the first public arXiv submission (`v1` on arXiv). Its source package was
validated at 15 pages, 3 figures and 36 references. These checks establish
repository/package integrity only: the manuscript has not been submitted or
published on arXiv, and no endorsement is claimed.
