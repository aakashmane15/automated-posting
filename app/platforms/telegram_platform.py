import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class TelegramPlatform(BasePlatform):
    name = "Telegram"

    async def post(self, message: str, url: str) -> PlatformResult:
        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            return self.failure("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not configured")
        api_url = (
            f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        )
        payload = {"chat_id": settings.telegram_chat_id, "text": message}
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(api_url, json=payload)
            data = response.json()
            if response.status_code == 200 and data.get("ok"):
                chat_id = settings.telegram_chat_id.lstrip("@")
                return self.success(
                    posted_url=f"https://t.me/{chat_id}", public_access=True
                )
            return self.failure(
                f"Telegram API error: {data.get('description', response.text)}"
            )
        except Exception as exc:
            return self.failure(str(exc))
