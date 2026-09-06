.PHONY: test validate run bom

test:
	python -m pytest -q

validate:
	python scripts/validate_specs.py

run:
	uvicorn sgaeia.api:app --app-dir src --host 0.0.0.0 --port 8080

bom:
	python scripts/generate_agent_bom.py

public-release:
	python scripts/validate_public_release.py
