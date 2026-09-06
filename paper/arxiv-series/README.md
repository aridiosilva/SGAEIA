# SGAEIA arXiv Technical Paper Series

**Author:** Aridio Silva — @aridiosilva  
**Prepared:** September 2026  
**Repository:** `https://github.com/aridiosilva/SGAEIA`

## Manuscripts

1. **Reference Architecture** — submit first. It deliberately begins with Edge Computing → Edge AI → Agentic Edge AI → distributed authority, establishing why SGAEIA is necessary.
2. **Governed Autonomy and Security** — focused formal/security paper.
3. **Integration Ports and Adapter Conformance** — focused software architecture and assurance paper.
4. **Cyber-Range Evaluation Protocol** — pre-results methodology paper; it contains no invented experimental results.

## Scientific discipline

The series distinguishes:
- designed architectural properties;
- formally specified properties;
- locally tested properties;
- properties requiring representative/live experimental validation.

Do not claim production certification or completed TLA+/Alloy model checking.

## Build

Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` inside each paper directory.
