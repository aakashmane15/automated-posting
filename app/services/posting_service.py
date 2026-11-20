from app.platforms.devto_platform import DevToPlatform
from app.platforms.discord_platform import DiscordPlatform
from app.platforms.slack_platform import SlackPlatform
from app.platforms.telegram_platform import TelegramPlatform
from app.platforms.wordpress_platform import WordPressPlatform
from app.schemas import PlatformResult


def get_platforms():
    return [
        TelegramPlatform(),
        DiscordPlatform(),
        SlackPlatform(),
        WordPressPlatform(),
        DevToPlatform(),
    ]


async def post_to_all_platforms(message: str, url: str) -> list[PlatformResult]:
    results = []
    for platform in get_platforms():
        try:
            result = await platform.post(message, url)
        except Exception as exc:
            result = platform.failure(f"Unexpected error: {exc}")
        results.append(result)
    return results
