from __future__ import annotations

import httpx


def build_target_client(*, timeout_seconds: float = 10.0) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        timeout=httpx.Timeout(timeout_seconds, connect=min(timeout_seconds, 5.0)),
        follow_redirects=False,
        trust_env=False,
        headers={"User-Agent": "Delicious-Scanner/0.1"},
    )
