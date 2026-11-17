import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class SlackPlatform(BasePlatform):
    name = "Slack"

    async def post(self, message: str, url: str) -> PlatformResult:
        if not settings.slack_webhook_url:
            return self.failure("SLACK_WEBHOOK_URL not configured")
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    settings.slack_webhook_url, json={"text": message}
                )
            if response.status_code == 200 and response.text.strip() == "ok":
                return self.success(
                    posted_url=settings.slack_webhook_url, public_access=False
                )
            return self.failure(f"Slack webhook failed: {response.text}")
        except Exception as exc:
            return self.failure(str(exc))
