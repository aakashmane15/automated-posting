import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class DiscordPlatform(BasePlatform):
    name = "Discord"

    async def post(self, message: str, url: str) -> PlatformResult:
        if not settings.discord_webhook_url:
            return self.failure("DISCORD_WEBHOOK_URL not configured")
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    settings.discord_webhook_url, json={"content": message}
                )
            if response.status_code in (200, 204):
                return self.success(
                    posted_url=settings.discord_webhook_url, public_access=True
                )
            return self.failure(
                f"Discord webhook failed with status {response.status_code}"
            )
        except Exception as exc:
            return self.failure(str(exc))
