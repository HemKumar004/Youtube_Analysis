from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.openai_service import generate_social_media_content

router = APIRouter()

class GenerationRequest(BaseModel):
    topic: str

@router.post("/generate-post")
def generate_post(req: GenerationRequest):
    try:
        result = generate_social_media_content(req.topic)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
