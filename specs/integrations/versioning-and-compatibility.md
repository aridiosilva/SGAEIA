# Integration Port Versioning and Compatibility

## Port version

Each `IntegrationPort` has an independent semantic version.

- MAJOR: breaking semantic change in operation, security, failure or revocation contract.
- MINOR: backward-compatible capability or evidence extension.
- PATCH: clarification/correction that does not change required behavior.

## Adapter declaration

An adapter SHALL declare:

```text
implementation_id
implementation_version
port_id
supported_port_version
conformance_level
```

## Compatibility rule

A newer adapter MAY implement an older port if all mandatory semantics remain satisfied. A newer port MUST NOT be assumed compatible solely because transport schemas parse successfully.

## API specification baselines

Reference HTTP contracts use **OpenAPI 3.2.0**. Reference event contracts use **AsyncAPI 3.1.0**. These are interchange/documentation formats and do not supersede the semantic port contract.

Changing OpenAPI/AsyncAPI tooling SHALL NOT silently change authorization, failure, evidence or revocation semantics.
