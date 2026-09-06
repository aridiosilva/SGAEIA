# arXiv Submission Guide — SGAEIA

## Before submission
1. Create/sign in to your arXiv account.
2. Complete author identity and connect ORCID if available.
3. Check whether endorsement is required for the intended category.
4. Make the exact GitHub release public only after secret/private-data review.
5. Use the source ZIP for the paper you are submitting.

## Submission
1. From the arXiv user page choose **START NEW SUBMISSION**.
2. Upload the source ZIP.
3. Confirm TeX processor and top-level `main.tex`.
4. Remove extraneous files.
5. Compile on arXiv and inspect the generated PDF.
6. Enter title, author, abstract, comments, primary category/cross-lists, and license.
7. Verify metadata against the manuscript.
8. Complete **Submit Article** and monitor moderation status.

## Paper 01 recommendation
Primary: `cs.AI` (reasonable alternative: `cs.DC`).  
Cross-lists: `cs.CR`, `cs.DC`, `cs.MA`, `cs.NI` when substantively justified.

## Source hygiene
arXiv source is public. Upload only what is required to compile. Remove `.env`, credentials, logs, editor backups, private notes/comments, unused figures, local absolute paths, correspondence, and unpublished unrelated material. Compile the exact ZIP in a clean directory before upload.

## After announcement
Record the arXiv ID in README/CITATION.cff; tag the matching GitHub release; optionally archive it in Zenodo; cite Paper 01 in later papers. Corrections should be new versions of the same arXiv work, not duplicate submissions.

arXiv is a moderated preprint repository, not peer review. Pursue peer-reviewed publication after establishing the preprint.
