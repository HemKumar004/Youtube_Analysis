from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..services.youtube import search_videos, get_video_comments
from ..services.nlp import clean_text, extract_entities, analyze_sentiment, extract_top_topics
import pandas as pd

router = APIRouter()

class AnalysisRequest(BaseModel):
    topic: str
    max_videos: int = 100

@router.post("/analyze")
def run_analysis(req: AnalysisRequest):
    try:
        # 1. Extraction
        videos = search_videos(req.topic, max_results=req.max_videos)
        if not videos:
            return {"message": "No videos found", "data": {}}
            
        video_ids = [vid['video_id'] for vid in videos]
        # Fetching up to 500 comments per video for thorough analysis
        comments = get_video_comments(video_ids, max_comments_per_video=500) 
        
        # 2. NLP Processing
        processed_comments = []
        organization_mentions = {}
        person_mentions = {}
        sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        
        cleaned_texts = []
        
        for c in comments:
            text = c['text']
            cleaned = clean_text(text)
            cleaned_texts.append(cleaned)
            
            # Entities
            entities = extract_entities(text) # spacy needs original capitalization
            for org in entities.get('organizations', []):
                organization_mentions[org] = organization_mentions.get(org, 0) + 1
            for person in entities.get('persons', []):
                person_mentions[person] = person_mentions.get(person, 0) + 1
                
            # Sentiment
            sentiment = analyze_sentiment(cleaned)
            sentiment_counts[sentiment] += 1
            
            processed_comments.append({
                "video_id": c['video_id'],
                "cleaned_text": cleaned,
                "sentiment": sentiment
            })
            
        # Topic Analysis
        top_topics = extract_top_topics(cleaned_texts, top_n=10)
        
        # Sort and take top 10 entities
        top_orgs = dict(sorted(organization_mentions.items(), key=lambda item: item[1], reverse=True)[:10])
        top_persons = dict(sorted(person_mentions.items(), key=lambda item: item[1], reverse=True)[:10])
        
        return {
            "status": "success",
            "summary": {
                "total_videos": len(videos),
                "total_comments_analyzed": len(comments)
            },
            "analysis": {
                "organizations": top_orgs,
                "persons": top_persons,
                "sentiments": sentiment_counts,
                "topics": top_topics
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
