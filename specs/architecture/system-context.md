# C4 L1 — System Context

```mermaid
flowchart LR
  H[Human Operators] --> P[Secure Governed Multi-Agent Edge AI Platform]
  P <--> E[Enterprise Systems]
  P <--> X[External SaaS/APIs/Models]
  P <--> O[OT / Cyber-Physical Systems]
  P --> G[GRC / SOC / Audit]
```

## Actors
- Human Operators / Approvers
- Agent Owners
- GRC / SOC
- Enterprise applications
- External providers
- Cyber-physical systems

## Security objective
Toda transição externa é uma trust boundary. Nenhuma comunicação recebe confiança implícita pela localização.
