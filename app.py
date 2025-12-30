from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import search_recent_tweets
from database import get_cached_tweets, init_db
from predict_and_update import run_predictions

app = FastAPI()

# Enable CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# Request Model
class SearchRequest(BaseModel):
    query: str
    limit: int = 100

@app.post("/fetch")
async def fetch_tweets(request: SearchRequest):
    """Fetch tweets from Twitter API and cache them"""
    df = search_recent_tweets(request.query, limit=request.limit)
    return {"status": "success", "count": len(df), "message": f"Fetched {len(df)} tweets"}

@app.get("/tweets")
async def get_tweets(query: str, limit: int = 50):
    """Get cached tweets with sentiment analysis"""
    df_db = get_cached_tweets(query, limit=limit)
    if df_db.empty:
        return {"tweets": [], "count": 0}
    
    # Convert dataframe to a list of dictionaries for Flutter
    tweets_list = df_db.to_dict(orient='records')
    return {"tweets": tweets_list, "count": len(tweets_list)}

@app.post("/predict")
async def predict_tweets(background_tasks: BackgroundTasks):
    """Run sentiment analysis predictions on unpredicted tweets"""
    background_tasks.add_task(run_predictions)
    return {"status": "success", "message": "Sentiment analysis started"}

@app.get("/")
async def root():
    return {"message": "Sentiment Analysis Backend API is running", "status": "ok"}

# To run: uvicorn app:app --host 0.0.0.0 --port 8000 --reload