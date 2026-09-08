from pathlib import Path
import csv, json, sys, yaml

ROOT=Path(__file__).resolve().parents[1]
errors=[]

required_docs=[
 "specs/architecture/system-context.md","specs/architecture/security-invariants.md",
 "specs/risks/risk-register.csv","specs/controls/control-catalog.yaml",
 "specs/threat-model/attack-paths.md",
 "specs/integrations/README.md","specs/integrations/conformance-matrix.csv",
 "specs/architecture/alien-cognition-assurance.md",
 "specs/policies/operation-policies.yaml",
 "schemas/capability-token.schema.json","schemas/monitor-decision.schema.json",
 "schemas/human-approval.schema.json","schemas/observed-effect.schema.json"
]
for rel in required_docs:
    if not (ROOT/rel).exists(): errors.append(f"missing {rel}")

for p in (ROOT/"specs/agents").glob("*.yaml"):
    d=yaml.safe_load(p.read_text())
    if not isinstance(d,dict) or d.get("kind")!="Agent": continue
    s=d.get("spec",{})
    if s.get("class")=="L4" and s.get("autonomy")=="A5": errors.append(f"{p}: L4+A5 forbidden")
    if not s.get("identity",{}).get("spiffeId","").startswith("spiffe://"): errors.append(f"{p}: invalid workload identity")
    if s.get("killSwitch",{}).get("required") is not True: errors.append(f"{p}: kill switch required")
    assurance=s.get("capabilityAssuranceLevel")
    if not isinstance(assurance,int) or not 0 <= assurance <= 5:
        errors.append(f"{p}: capabilityAssuranceLevel must be 0..5")
    budgets=s.get("executionBudgets",{})
    for key in ("runtimeSeconds","toolCalls","networkReach"):
        if not isinstance(budgets.get(key),int) or budgets[key] < 0:
            errors.append(f"{p}: invalid execution budget {key}")

controls=yaml.safe_load((ROOT/"specs/controls/control-catalog.yaml").read_text())
ids=[x["id"] for x in controls["controls"]]
if len(ids)!=len(set(ids)): errors.append("duplicate control IDs")

# RC2 schema, API-contract and traceability gates.
for rel in [
    "schemas/agent.schema.json","schemas/capability-token.schema.json",
    "schemas/monitor-decision.schema.json","schemas/human-approval.schema.json",
    "schemas/observed-effect.schema.json","specs/api/openapi.json",
]:
    try:
        json.loads((ROOT/rel).read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        errors.append(f"{rel}: invalid JSON: {exc}")

api=json.loads((ROOT/"specs/api/openapi.json").read_text(encoding="utf-8"))
request_schema=api.get("components",{}).get("schemas",{}).get("AuthorizationRequest",{})
expected_request_fields={"agent_id","operation","resource","trace_id","delegation_chain"}
if set(request_schema.get("properties",{})) != expected_request_fields:
    errors.append("control API contract fields do not match trusted-boundary request model")
if request_schema.get("additionalProperties") is not False:
    errors.append("control API MUST reject untrusted extra request fields")

with (ROOT/"specs/traceability/requirements-controls-tests.csv").open(newline="") as stream:
    trace_rows=list(csv.DictReader(stream))
traced_requirements={row["requirement_id"] for row in trace_rows}
required_rc2={f"SR-{number:03d}" for number in range(25,36)}
missing_rc2=required_rc2-traced_requirements
if missing_rc2:
    errors.append(f"RC2 requirements missing traceability: {sorted(missing_rc2)}")
traced_controls={item for row in trace_rows for item in row["control_ids"].split(";")}
aas_controls={f"CTL-AAS-{number:03d}" for number in range(1,8)}
if aas_controls-traced_controls:
    errors.append(f"AAS controls missing traceability: {sorted(aas_controls-traced_controls)}")
for row in trace_rows:
    target=row["test_or_validation"].split("::",1)[0]
    if not (ROOT/target).exists():
        errors.append(f"{row['requirement_id']}: missing traceability target {target}")

policy_doc=yaml.safe_load((ROOT/"specs/policies/operation-policies.yaml").read_text())
if policy_doc.get("kind")!="OperationPolicySet" or not policy_doc.get("operations"):
    errors.append("operation policy set is missing or empty")
for operation,item in policy_doc.get("operations",{}).items():
    assurance=item.get("assurance",{})
    for dimension in ("monitor","containment","recovery"):
        value=assurance.get(dimension)
        if not isinstance(value,int) or not 0 <= value <= 5:
            errors.append(f"{operation}: assurance {dimension} must be 0..5")

if errors:
    print("SPEC VALIDATION FAILED")
    for e in errors: print("-",e)
    sys.exit(1)
print("SPEC VALIDATION PASSED")


# Integration Port Specification validation
REQUIRED_CONTRACTS={"functional","security","audit","failure","revocation"}
port_ids=[]
for p in sorted((ROOT/"specs/integrations/ports").glob("*.port.yaml")):
    d=yaml.safe_load(p.read_text())
    if d.get("kind")!="IntegrationPort":
        errors.append(f"{p}: kind must be IntegrationPort")
        continue
    port_ids.append(d.get("metadata",{}).get("id"))
    spec=d.get("spec",{})
    contracts=spec.get("contracts",{})
    missing=REQUIRED_CONTRACTS-set(contracts)
    if missing: errors.append(f"{p}: missing contract dimensions {sorted(missing)}")
    for key in REQUIRED_CONTRACTS:
        if not contracts.get(key): errors.append(f"{p}: empty {key} contract")
    if spec.get("evidence",{}).get("required") is not True: errors.append(f"{p}: evidence required")
    if spec.get("revocation",{}).get("supported") is not True: errors.append(f"{p}: revocation required")

for p in sorted((ROOT/"specs/integrations/openapi").glob("*.openapi.yaml")):
    d=yaml.safe_load(p.read_text())
    if d.get("openapi")!="3.2.0": errors.append(f"{p}: OpenAPI baseline must be 3.2.0")
for p in sorted((ROOT/"specs/integrations/asyncapi").glob("*.asyncapi.yaml")):
    d=yaml.safe_load(p.read_text())
    if d.get("asyncapi")!="3.1.0": errors.append(f"{p}: AsyncAPI baseline must be 3.1.0")


# Adapter Profile validation
adapter_ids=[]
known_ports=set(port_ids)
for p in sorted((ROOT/"specs/integrations/adapters").glob("*.adapter.yaml")):
    d=yaml.safe_load(p.read_text())
    if d.get("kind")!="AdapterProfile":
        errors.append(f"{p}: kind must be AdapterProfile")
        continue
    md=d.get("metadata",{})
    spec=d.get("spec",{})
    adapter_ids.append(md.get("id"))
    if md.get("portId") not in known_ports: errors.append(f"{p}: unknown port {md.get('portId')}")
    if spec.get("verification") not in {"contract-harness","live-environment","independent-assurance"}: errors.append(f"{p}: invalid verification scope")
    if spec.get("targetConformance") not in {"IPS-C1","IPS-C2","IPS-C3"}: errors.append(f"{p}: invalid target conformance")
    if spec.get("failureMode")=="fail-open": errors.append(f"{p}: fail-open forbidden")
    if not spec.get("implementation") or not spec.get("baseline"): errors.append(f"{p}: implementation/baseline required")
    if not spec.get("evidence"): errors.append(f"{p}: evidence declarations required")

if len(adapter_ids)!=len(set(adapter_ids)): errors.append("duplicate adapter profile IDs")

known_adapter_ports={}
for p in sorted((ROOT/"specs/integrations/adapters").glob("*.adapter.yaml")):
    d=yaml.safe_load(p.read_text())
    if d.get("kind")=="AdapterProfile": known_adapter_ports[d["metadata"]["id"]]=d["metadata"]["portId"]
for p in sorted((ROOT/"specs/integrations/deployment-profiles").glob("*.yaml")):
    d=yaml.safe_load(p.read_text())
    selected=d.get("spec",{}).get("adapters",{})
    for port_id, adapter_id in selected.items():
        if adapter_id not in known_adapter_ports: errors.append(f"{p}: unknown adapter {adapter_id}")
        elif known_adapter_ports[adapter_id] != port_id: errors.append(f"{p}: adapter {adapter_id} bound to {known_adapter_ports[adapter_id]}, not {port_id}")

import csv
with (ROOT/"specs/integrations/adapter-conformance-matrix.csv").open() as f:
    matrix_ids={r["adapter_id"] for r in csv.DictReader(f)}
if set(adapter_ids)!=matrix_ids:
    errors.append("adapter conformance matrix must cover every adapter profile exactly")

# Re-check because integration validation is appended after the original report block.
if errors:
    print("SPEC VALIDATION FAILED (INTEGRATIONS)")
    for e in errors: print("-",e)
    sys.exit(1)
print("INTEGRATION PORT VALIDATION PASSED")
