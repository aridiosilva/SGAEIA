# Cross-Cutting Security Requirements for Integration Adapters

Every production adapter SHALL:

1. authenticate its caller/workload when the port is protected;
2. authorize operations independently of network location;
3. validate input schema and reject ambiguous critical requests;
4. bind decisions/results to subject, action, resource and freshness where applicable;
5. propagate trace/correlation identifiers;
6. produce auditable evidence with implementation and port identifiers;
7. define timeout, retry, cache and partition behavior;
8. fail closed or degrade authority for critical operations;
9. support credential/capability/policy revocation appropriate to the port;
10. expose health separately from authorization success;
11. avoid secrets in logs and protect regulated/sensitive payloads;
12. be covered by SAST/SCA/configuration scanning and integration/security tests;
13. publish software/supply-chain provenance where production policy requires it;
14. preserve SGAEIA security invariants under dependency failure.

## Forbidden equivalence assumptions

The following are not sufficient to claim conformance:

- same product category;
- same protocol;
- same response shape;
- same vendor marketing capability;
- successful happy-path demo.

Conformance is based on preserved semantics and evidence.
