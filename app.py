from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import search_recent_tweets
from database import get_cached_tweets, init_db
from predict_and_update import run_predictions
import os

app = FastAPI(
    title="Sentiment Analysis API",
    description="Backend API for tweet sentiment analysis",
    version="1.0.0"
)

# Enable CORS for Flutter app - configure allowed origins
# For production, you can set ALLOWED_ORIGINS environment variable
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
try:
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")

# Request Model
class SearchRequest(BaseModel):
    query: str
    limit: int = 100

@app.post("/fetch")
async def fetch_tweets(request: SearchRequest):
    """Fetch tweets from Twitter API and cache them"""
    try:
        df = search_recent_tweets(request.query, limit=request.limit)
        return {"status": "success", "count": len(df), "message": f"Fetched {len(df)} tweets"}
    except Exception as e:
        return {"status": "error", "message": str(e), "count": 0}

@app.get("/tweets")
async def get_tweets(query: str, limit: int = 50):
    """Get cached tweets with sentiment analysis"""
    try:
        df_db = get_cached_tweets(query, limit=limit)
        if df_db.empty:
            return {"tweets": [], "count": 0}
        
        # Convert dataframe to a list of dictionaries for Flutter
        tweets_list = df_db.to_dict(orient='records')
        return {"tweets": tweets_list, "count": len(tweets_list)}
    except Exception as e:
        return {"tweets": [], "count": 0, "error": str(e)}

@app.post("/predict")
async def predict_tweets(background_tasks: BackgroundTasks):
    """Run sentiment analysis predictions on unpredicted tweets"""
    try:
        background_tasks.add_task(run_predictions)
        return {"status": "success", "message": "Sentiment analysis started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    return {
        "message": "Sentiment Analysis Backend API is running", 
        "status": "ok",
        "version": "1.0.0",
        "endpoints": {
            "POST /fetch": "Fetch tweets from Twitter API",
            "GET /tweets": "Get cached tweets with sentiment analysis",
            "POST /predict": "Run sentiment analysis on unpredicted tweets",
            "GET /health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy", "service": "sentiment-analysis-api"}

# Main entry point for Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)