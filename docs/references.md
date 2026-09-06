# Referências normativas e técnicas

> Verifique versão, aplicabilidade e licenciamento antes de uso normativo em produção.

1. **NIST SP 800-207A** — A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments. https://csrc.nist.gov/pubs/sp/800/207/a/final
2. **NIST AI RMF 1.0** — Artificial Intelligence Risk Management Framework. https://www.nist.gov/itl/ai-risk-management-framework
3. **NIST AI 600-1** — Generative Artificial Intelligence Profile. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
4. **NIST SP 800-218A** — Secure Software Development Practices for Generative AI and Dual-Use Foundation Models. https://csrc.nist.gov/pubs/sp/800/218/a/final
5. **NIST CSF 2.0** — Cybersecurity Framework. https://www.nist.gov/cyberframework
6. **MITRE ATLAS** — AI threat knowledge base, incluindo GenAI e Agentic AI. https://atlas.mitre.org/
7. **OWASP GenAI Security Project / Agentic Security Initiative**. https://genai.owasp.org/initiatives/agentic-security-initiative/
8. **OWASP Agent Control Standard (ACS)** — publicado em 1 Sep 2026. https://genai.owasp.org/resource/agent-control-standard-acs/
9. **SPIFFE Standard** — workload identities. https://spiffe.io/docs/latest/spiffe-specs/
10. **ISO/IEC 42001:2023** — AI management systems. https://www.iso.org/standard/42001
11. **ISO/IEC 23894:2023** — AI risk management. https://www.iso.org/standard/77304.html
12. **ETSI MEC** — Multi-access Edge Computing. https://www.etsi.org/technologies/multi-access-edge-computing
13. **IEC 62443** — Industrial communication networks / IACS security, quando aplicável ao plano OT.

## Nota de arquitetura
O NIST SP 800-207A sustenta o foco em identidades de aplicações/serviços e enforcement com gateways/sidecars; SPIFFE fornece um padrão de identidade criptográfica de workloads; OWASP ACS reforça controles declarativos e instrumentação de agentes em runtime; MITRE ATLAS fornece táticas/técnicas específicas para sistemas de IA, inclusive agentivos.

## API and event contract specifications

- OpenAPI Initiative — OpenAPI Specification 3.2.0 (published 19 September 2025).
- AsyncAPI Initiative — AsyncAPI Specification 3.1.0 (released 31 January 2026).

## Adapter reference baselines — verified September 2026

The Adapter Conformance Framework records current upstream baselines for reproducibility; production deployments must maintain their own supported-version policy and should not blindly follow `latest`.

- SPIRE releases — https://github.com/spiffe/spire/releases
- SPIFFE Workload API — https://spiffe.io/docs/latest/spiffe-specs/spiffe_workload_api/
- Open Policy Agent — https://github.com/open-policy-agent/opa
- Istio releases — https://istio.io/latest/news/releases/
- OpenTelemetry Collector releases — https://github.com/open-telemetry/opentelemetry-collector-releases/releases
- NATS Python client — https://github.com/nats-io/nats.py
- NATS Server releases — https://github.com/nats-io/nats-server/releases
- Apache Kafka downloads — https://kafka.apache.org/community/downloads/
- PostgreSQL project news — https://www.postgresql.org/about/news/
- Kubernetes releases — https://kubernetes.io/releases/
- Kubernetes Python client — https://github.com/kubernetes-client/python
- K3s releases — https://github.com/k3s-io/k3s/releases
