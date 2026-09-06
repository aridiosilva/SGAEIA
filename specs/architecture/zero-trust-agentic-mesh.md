# Zero-Trust Agentic Mesh (ZTAM)

## Componentes lógicos
- Agent Proxy
- Identity Proxy
- Policy Proxy / PEP
- A2A Gateway
- Tool Gateway
- Egress Gateway
- Telemetry/Evidence Collector

## Path
```text
Agent A → local proxy → identity/policy/risk → encrypted mesh → remote proxy → Agent B
```

## Requisitos
- mTLS/workload identity;
- default-deny;
- egress allow-list;
- anti-replay;
- schema/intent validation;
- distributed tracing;
- rate/compute/cost limits;
- local policy cache para Edge fail-secure.
