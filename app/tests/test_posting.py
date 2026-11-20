from fastapi.testclient import TestClient
from app.main import app
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult

client = TestClient(app)
VALID_MESSAGE = "Check out our latest business platform and grow your online visibility. https://example.com"


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


def test_valid_message_posts_successfully(monkeypatch):
    import app.services.posting_service as service

    monkeypatch.setattr(
        service, "get_platforms", lambda: [FakeSuccessPlatform(), FakeFailPlatform()]
    )
    response = client.post("/posting", json={"message": VALID_MESSAGE})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["results"][0]["status"] == "success"
    assert data["results"][1]["status"] == "failed"


def test_message_too_long():
    assert (
        client.post(
            "/posting", json={"message": "a" * 201 + " https://example.com"}
        ).status_code
        == 422
    )


def test_message_without_link():
    assert (
        client.post("/posting", json={"message": "Hello without any link"}).status_code
        == 422
    )


def test_message_with_two_links():
    assert (
        client.post(
            "/posting",
            json={"message": "Visit https://example.com and https://google.com now"},
        ).status_code
        == 422
    )


def test_message_with_invalid_url():
    assert (
        client.post("/posting", json={"message": "Visit https:// now"}).status_code
        == 422
    )


def test_empty_message():
    assert client.post("/posting", json={"message": ""}).status_code == 422


def test_health_check():
    assert client.get("/").json()["status"] == "ok"
