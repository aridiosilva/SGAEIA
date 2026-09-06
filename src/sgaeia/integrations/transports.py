from __future__ import annotations

import json
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class JsonTransport(Protocol):
    def __call__(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]: ...


class HttpJsonTransport:
    """Small dependency-free JSON transport for external adapter endpoints."""

    def __init__(self, base_url: str, *, timeout: float = 2.0, headers: dict[str, str] | None = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {"content-type": "application/json", **(headers or {})}

    def __call__(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/{operation.lstrip('/')}"
        req = Request(url, data=json.dumps(payload).encode(), headers=self.headers, method="POST")
        try:
            with urlopen(req, timeout=self.timeout) as resp:  # nosec B310 - explicit adapter endpoint
                raw = resp.read().decode() or "{}"
                return json.loads(raw)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ConnectionError(f"adapter transport failure for {operation}: {exc}") from exc
