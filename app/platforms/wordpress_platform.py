import base64
import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class WordPressPlatform(BasePlatform):
    name = "WordPress"

    async def post(self, message: str, url: str) -> PlatformResult:
        if not settings.wordpress_url or not settings.wordpress_username:
            return self.failure("WORDPRESS_URL / WORDPRESS_USERNAME not configured")
        api_url = f"{settings.wordpress_url}/wp-json/wp/v2/posts"
        credentials = f"{settings.wordpress_username}:{settings.wordpress_app_password}"
        auth_header = "Basic " + base64.b64encode(credentials.encode()).decode()
        payload = {"title": message[:50], "content": message, "status": "publish"}
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    api_url, json=payload, headers={"Authorization": auth_header}
                )
            if response.status_code == 201:
                return self.success(
                    posted_url=response.json().get("link", api_url), public_access=True
                )
            return self.failure(
                f"WordPress API error {response.status_code}: {response.text[:200]}"
            )
        except Exception as exc:
            return self.failure(str(exc))
