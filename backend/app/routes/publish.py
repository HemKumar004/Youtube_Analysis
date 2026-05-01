# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from ..services.twitter import publish_tweet

# router = APIRouter()

# class PublishRequest(BaseModel):
#     content: str

# @router.post("/publish")
# def publish_to_twitter(req: PublishRequest):
#     try:
#         result = publish_tweet(req.content)
#         if result.get("success"):
#             return {"status": "success", "data": result}
#         else:
#             raise HTTPException(status_code=400, detail=result.get("error"))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.twitter import publish_tweet

router = APIRouter()

class PublishRequest(BaseModel):
    content: str

@router.post("/publish")
def publish_to_twitter(req: PublishRequest):
    try:
        result = publish_tweet(req.content)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        print("🔥 PUBLISH ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )