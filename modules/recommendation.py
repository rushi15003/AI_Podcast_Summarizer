import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# YouTube API Key (Replace with your actual API key)
YOUTUBE_API_KEY = "AIzaSyAExb8CUloM-Ltz8uXBULxiLG7UFkU1W20"

def search_related_videos_tfidf(transcription):
    """Find semantically similar videos using TF-IDF approach."""
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=podcast&type=video&maxResults=10&key={YOUTUBE_API_KEY}"
    response = requests.get(search_url).json()
    
    candidate_videos = []
    descriptions = []
    
    for item in response.get("items", []):
        title = item["snippet"]["title"]
        description = item["snippet"].get("description", "")
        video_id = item["id"]["videoId"]
        thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
        
        candidate_videos.append({"title": title, "video_id": video_id, "thumbnail": thumbnail, "description": description})
        descriptions.append(description)
    
    if not descriptions:
        return []
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([transcription] + descriptions)
    
    # Compute Cosine Similarity
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Rank top 5 similar videos
    ranked_videos = sorted(zip(candidate_videos, similarity_scores), key=lambda x: x[1], reverse=True)[:5]
    
    return [{"title": vid["title"], "video_id": vid["video_id"], "thumbnail": vid["thumbnail"]} for vid, _ in ranked_videos]
