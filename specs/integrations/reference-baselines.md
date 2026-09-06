# Reference Technology Baselines — September 2026

These versions are **reference baselines observed from official upstream release channels as of 2026-09-05**. They are not permanent pins and do not imply certification by the upstream projects.

| Technology | Reference baseline | Role |
|---|---:|---|
| SPIRE | 1.15.2 | IP-IDENTITY |
| Open Policy Agent | 1.16.2 | IP-PDP |
| Istio | 1.31.0 | IP-MESH |
| OpenTelemetry Collector | 0.160.0 | IP-OBS |
| NATS Server | 2.14.5 | IP-BUS |
| Apache Kafka | 4.3.1 | IP-BUS alternative |
| PostgreSQL | 18.6 | IP-STATE |
| Kubernetes | 1.37.0 | IP-EDGE |
| K3s | supported Kubernetes-compatible release branch | IP-EDGE alternative |

## Upstream references

- SPIRE releases: https://github.com/spiffe/spire/releases
- OPA releases: https://github.com/open-policy-agent/opa/releases
- Istio releases: https://istio.io/latest/news/releases/
- OpenTelemetry Collector releases: https://github.com/open-telemetry/opentelemetry-collector-releases/releases
- NATS Server releases: https://github.com/nats-io/nats-server/releases
- Apache Kafka downloads: https://kafka.apache.org/community/downloads/
- PostgreSQL release news: https://www.postgresql.org/about/news/
- Kubernetes releases: https://kubernetes.io/releases/
- K3s releases: https://github.com/k3s-io/k3s/releases

A production profile SHOULD establish an organization-controlled compatibility window rather than automatically following `latest`.
