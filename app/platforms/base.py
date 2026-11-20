"""
app/platforms/base.py
Base class that every platform must follow.
This keeps all platforms consistent and makes it easy to add new ones.
"""

from datetime import datetime

from app.schemas import PlatformResult


class BasePlatform:
    name: str = "Base Platform"

    async def post(self, message: str, url: str) -> PlatformResult:
        """Each platform implements its own posting logic."""
        raise NotImplementedError

    # --- Helpers so every platform returns the same format ---

    def success(self, posted_url: str, public_access: bool) -> PlatformResult:
        now = datetime.now()
        return PlatformResult(
            platform=self.name,
            status="success",
            posted_url=posted_url,
            public_access=public_access,
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            error=None,
        )

    def failure(self, error: str) -> PlatformResult:
        return PlatformResult(
            platform=self.name,
            status="failed",
            posted_url=None,
            public_access=False,
            date=None,
            time=None,
            error=error,
        )
