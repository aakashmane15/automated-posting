import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    discord_webhook_url: str = os.getenv("DISCORD_WEBHOOK_URL", "")
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")
    wordpress_url: str = os.getenv("WORDPRESS_URL", "").rstrip("/")
    wordpress_username: str = os.getenv("WORDPRESS_USERNAME", "")
    wordpress_app_password: str = os.getenv("WORDPRESS_APP_PASSWORD", "")
    devto_api_key: str = os.getenv("DEVTO_API_KEY", "")


settings = Settings()
