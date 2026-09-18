import asyncio
from delicious_scanner.services.http import build_target_client
def test_client_has_safe_baseline()->None:
    async def run()->None:
        c=build_target_client()
        try:assert c.follow_redirects is False
        finally:await c.aclose()
    asyncio.run(run())
