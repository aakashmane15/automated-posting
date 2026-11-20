"""
app/config.py
Loads API credentials from environment variables (.env file).
Keeping credentials here means we never hard-code secrets in code.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # Discord
    discord_webhook_url: str = os.getenv("DISCORD_WEBHOOK_URL", "")

    # Slack
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")

    # WordPress
    wordpress_url: str = os.getenv("WORDPRESS_URL", "").rstrip("/")
    wordpress_username: str = os.getenv("WORDPRESS_USERNAME", "")
    wordpress_app_password: str = os.getenv("WORDPRESS_APP_PASSWORD", "")

    # Dev.to
    devto_api_key: str = os.getenv("DEVTO_API_KEY", "")


settings = Settings()
