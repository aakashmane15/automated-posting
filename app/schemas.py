"""
app/schemas.py
Request / response models + input validation.
"""

import re
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, field_validator

# Simple regex to find URLs in the message
URL_PATTERN = re.compile(r"https?://[^\s]+")


class PostRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        # 1. Message must not be empty
        if not value:
            raise ValueError("Message must not be empty")

        # 2. Message must not exceed 200 characters
        if len(value) > 200:
            raise ValueError("Message must not exceed 200 characters")

        # 3. Exactly one CTA link must be included
        urls = URL_PATTERN.findall(value)
        if len(urls) != 1:
            raise ValueError("Message must contain exactly one CTA link")

        # 4. Validate the URL
        url = urls[0].rstrip(".,)\"'")  # remove trailing punctuation
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("CTA link must start with http:// or https://")
        if not parsed.netloc or "." not in parsed.netloc:
            raise ValueError("CTA link is not a valid URL")

        return value

    @property
    def cta_url(self) -> str:
        """Helper: return the single CTA URL from the message."""
        urls = URL_PATTERN.findall(self.message)
        return urls[0].rstrip(".,)\"'") if urls else ""


class PlatformResult(BaseModel):
    platform: str
    status: str  # "success" or "failed"
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None


class PostResponse(BaseModel):
    success: bool
    results: list[PlatformResult]
