import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

_client = None

def get_youtube_client():
    global _client
    if _client is not None:
        return _client
        
    if not YOUTUBE_API_KEY:
        raise ValueError("Missing YouTube API Key")
    # Cache the client globally so it doesn't fetch the discovery doc on every single search
    _client = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, static_discovery=False)
    return _client

def search_videos(query: str, max_results: int = 100):
    client = get_youtube_client()
    videos = []
    next_page_token = None
    
    while len(videos) < max_results:
        request = client.search().list(
            q=query,
            part='id,snippet',
            maxResults=min(50, max_results - len(videos)),
            type='video',
            order='relevance',
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response.get('items', []):
            videos.append({
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channel_title': item['snippet']['channelTitle'],
                'publish_date': item['snippet']['publishedAt']
            })
            
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
            
    return videos

def get_video_comments(video_ids: list, max_comments_per_video: int = 500):
    client = get_youtube_client()
    all_comments = []
    
    for video_id in video_ids:
        comments_count = 0
        next_page_token = None
        
        try:
            while comments_count < max_comments_per_video:
                request = client.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=min(100, max_comments_per_video - comments_count),
                    pageToken=next_page_token,
                    textFormat='plainText'
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    all_comments.append({
                        "video_id": video_id,
                        "text": text
                    })
                    comments_count += 1
                    
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
        except Exception as e:
            # Catch errors like disabled comments for a specific video
            print(f"Error fetching comments for {video_id}: {e}")
            continue
            
    return all_comments
