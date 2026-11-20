"""
tests/test_posting.py
Run with:  pytest -v
"""

from fastapi.testclient import TestClient

from app.main import app
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult

client = TestClient(app)

VALID_MESSAGE = "Check out our latest business platform and grow your online visibility. https://example.com"


# --- Fake platforms for testing (no real API calls needed) ---


class FakeSuccessPlatform(BasePlatform):
    name = "FakeSuccess"

    async def post(self, message: str, url: str) -> PlatformResult:
        return self.success(
            posted_url="https://example.com/post/123", public_access=True
        )


class FakeFailPlatform(BasePlatform):
    name = "FakeFail"

    async def post(self, message: str, url: str) -> PlatformResult:
        return self.failure("Authentication failed")


# --- Validation tests ---


def test_valid_message_posts_successfully(monkeypatch):
    import app.services.posting_service as service

    monkeypatch.setattr(
        service,
        "get_platforms",
        lambda: [FakeSuccessPlatform(), FakeFailPlatform()],
    )

    response = client.post("/posting", json={"message": VALID_MESSAGE})
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert len(data["results"]) == 2
    assert data["results"][0]["status"] == "success"
    assert data["results"][0]["posted_url"] == "https://example.com/post/123"
    assert data["results"][0]["public_access"] is True
    assert data["results"][0]["date"] is not None
    assert data["results"][0]["time"] is not None
    assert data["results"][1]["status"] == "failed"
    assert data["results"][1]["error"] == "Authentication failed"


def test_message_too_long():
    long_message = "a" * 201 + " https://example.com"
    response = client.post("/posting", json={"message": long_message})
    assert response.status_code == 422


def test_message_without_link():
    response = client.post("/posting", json={"message": "Hello without any link"})
    assert response.status_code == 422


def test_message_with_two_links():
    response = client.post(
        "/posting",
        json={"message": "Visit https://example.com and https://google.com now"},
    )
    assert response.status_code == 422


def test_message_with_invalid_url():
    response = client.post("/posting", json={"message": "Visit https:// now"})
    assert response.status_code == 422


def test_empty_message():
    response = client.post("/posting", json={"message": ""})
    assert response.status_code == 422


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
