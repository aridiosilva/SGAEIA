# RC2 Implementation Status

This working candidate strengthens SGAEIA with Alien Cognition and Architectural
Assurance controls. It is not a release, certification or production assurance
claim. The immutable public citation baseline remains v0.3.4.

| Area | Status in RC2 working candidate |
|---|---|
| Trusted request boundary | API rejects client-supplied security context; server policy resolution tested |
| Untrusted reasoning denial | Trusted policy classification implemented and tested |
| Independent monitor gate | Registration, signature, time window and intent binding implemented and tested |
| Capability-gated autonomy | Missing assurance defaults to zero; ceiling enforcement tested |
| Runtime/tool/network budgets | Server-resolved counters and manifest budgets implemented and tested |
| Protected control-plane denial | Server-derived resource classification implemented and tested |
| Collective privilege aggregation | Integrated reference evaluator and denial scenario tested |
| Delegation expiry/purpose/provenance | Integrated reference validation; invalid input fails closed |
| Local evidence digest chain | Automatic chaining implemented; durable signing/external anchoring pending |
| Post-effect reconciliation | Separate observer record and divergence-triggered revocation implemented |
| Rollback and staged deployment | Requirements and revocation reference behavior implemented; live rollback adapter pending |
| Sandbagging/deceptive adaptation evaluation | Research/evaluation agenda only |

The current local suite reports 51 passing pytest tests, including HTTP trust-boundary, task-graph cycle, evidence-chain and post-effect binding scenarios. This remains
repository-level evidence and does not establish production or live-system assurance.

## Version and manuscript identity

- Development candidate: `v0.4.0-rc.1` (`0.4.0rc1` in Python package metadata).
- Immutable public software baseline: `v0.3.4`, preserved in `CITATION.cff` and its version DOI.
- Paper 01 v4 is integrated in `main` as the reviewed candidate for a first public arXiv submission (`v1` on arXiv). It has not been submitted or published on arXiv.
