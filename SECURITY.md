# Security Policy

## Scope

SGAEIA is a security reference architecture and demonstrative implementation. Security reports are particularly important when they concern bypasses of architectural invariants, including identity, authorization, policy enforcement, capability restriction, delegation bounds, revocation, kill switch, evidence integrity, adapter substitution, or Edge fail-secure behavior.

## Reporting a vulnerability

**Do not open a public GitHub issue for an undisclosed vulnerability.**

Canonical security policy: `https://github.com/aridiosilva/SGAEIA/security/policy`.

After the public repository is created, enable GitHub Private Vulnerability Reporting and use it as the preferred disclosure channel. Until that private reporting channel is configured, avoid publishing exploit details; contact the project maintainer through a private channel listed on the maintainer's GitHub profile.

Include, when possible:

- affected version/commit;
- impacted component, integration port, adapter, policy, or invariant;
- prerequisites;
- minimal reproduction;
- security impact;
- whether credentials, data, or cyber-physical effects are involved;
- suggested mitigation, if known.

## Disclosure expectations

The project aims to acknowledge valid reports, investigate, coordinate a fix, and publish an appropriate advisory or release note. Exact timelines cannot be guaranteed for an open-source reference project. Coordinated disclosure is preferred when public detail could enable exploitation before a mitigation exists.

## Supported versions

Until 1.0, the latest tagged minor release is the primary supported development line. Older pre-1.0 revisions may receive documentation-only fixes at maintainer discretion.

## Important limitation

Passing repository tests or adapter conformance does not certify a deployment as secure. Deployment-specific security, privacy, safety, legal, regulatory, and operational assurance remain the responsibility of the deploying organization.
