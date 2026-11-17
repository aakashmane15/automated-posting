import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class DevToPlatform(BasePlatform):
    name = "Dev.to"

    async def post(self, message: str, url: str) -> PlatformResult:
        if not settings.devto_api_key:
            return self.failure("DEVTO_API_KEY not configured")
        payload = {
            "article": {
                "title": message[:60],
                "body_markdown": message,
                "published": True,
            }
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    "https://dev.to/api/articles",
                    json=payload,
                    headers={"api-key": settings.devto_api_key},
                )
            if response.status_code == 201:
                return self.success(
                    posted_url=response.json().get("url", "https://dev.to"),
                    public_access=True,
                )
            return self.failure(
                f"Dev.to API error {response.status_code}: {response.text[:200]}"
            )
        except Exception as exc:
            return self.failure(str(exc))
