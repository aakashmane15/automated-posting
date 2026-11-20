from fastapi import FastAPI
from app.schemas import PostRequest, PostResponse
from app.services.posting_service import post_to_all_platforms

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="Posts one message to Telegram, Discord, Slack, WordPress and Dev.to",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Automated Posting API is running"}


@app.post("/posting", response_model=PostResponse)
async def posting(request: PostRequest):
    results = await post_to_all_platforms(message=request.message, url=request.cta_url)
    success = any(r.status == "success" for r in results)
    return PostResponse(success=success, results=results)
