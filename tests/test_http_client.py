import asyncio

from delicious_scanner.services.http import build_target_client


def test_client_has_safe_baseline() -> None:
    async def run() -> None:
        client = build_target_client()
        try:
            assert client.follow_redirects is False
        finally:
            await client.aclose()

    asyncio.run(run())
