from pathlib import Path
import json,yaml
ROOT=Path(__file__).resolve().parents[1]
agents=[]
for p in (ROOT/"specs/agents").glob("*.yaml"):
    d=yaml.safe_load(p.read_text())
    if isinstance(d,dict) and d.get("kind")=="Agent":
        agents.append({"id":d["metadata"]["id"],"owner":d["metadata"]["owner"],"class":d["spec"]["class"],"autonomy":d["spec"]["autonomy"],"trustZone":d["spec"]["trustZone"],"identity":d["spec"]["identity"]["spiffeId"],"capabilities":d["spec"]["capabilities"]["allow"]})
out={"format":"SGAEIA-Agent-BOM","version":"0.1","agents":agents}
(ROOT/"bom/agent-bom.generated.json").write_text(json.dumps(out,indent=2)+"\n")
print(f"generated {len(agents)} agents")
