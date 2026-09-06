# SGAEIA Project Governance

## Purpose

This document defines how changes to the SGAEIA reference architecture are proposed, reviewed, accepted, released, and governed. The project favors traceable engineering decisions over technology preference.

## Roles

### Maintainer
Maintainers protect architectural invariants, review changes, manage releases, and enforce repository policy.

### Contributor
Contributors may propose documentation, specifications, adapters, tests, threat models, controls, and implementation changes through pull requests.

### Security reviewer
A security reviewer evaluates changes that affect trust boundaries, authorization, identity, cryptography, revocation, telemetry, evidence, supply chain, Edge/OT safety, or failure semantics.

### GRC / assurance reviewer
A GRC or assurance reviewer evaluates changes that alter requirement-control-test mappings, compliance mappings, evidence contracts, risk acceptance, or conformance claims.

## Decision model

Routine changes may be accepted after normal review. Changes that alter a normative invariant, conformance level, security boundary, risk formula, or public API SHOULD include an Architecture Decision Record (ADR).

A change MUST NOT be merged if it silently increases authority, weakens fail-secure behavior, removes required evidence, bypasses revocation, or breaks requirement-to-test traceability.

## Normative hierarchy

When artifacts disagree, the intended order is:

1. `MASTER-SPEC.md` and normative specifications under `specs/`;
2. approved ADRs;
3. schemas and policy contracts;
4. executable conformance tests;
5. reference implementation;
6. explanatory documentation and examples.

Conflicts SHOULD be corrected rather than permanently tolerated.

## Releases

Releases use semantic versioning as a project convention:

- PATCH: documentation, tests, fixes, or compatible implementation improvements;
- MINOR: compatible architecture capabilities, integration ports, adapters, or normative extensions;
- MAJOR: incompatible normative changes or architectural contract breaks.

Release candidates SHOULD pass the SDD validator, automated tests, adapter conformance harness, BOM generation, and repository security gates.

## Conformance claims

Passing the local harness does not certify a vendor product, deployment, organization, or safety-critical system. IPS-C2/C3 or higher claims require the evidence specified by the relevant profile in a representative or production-like environment.
