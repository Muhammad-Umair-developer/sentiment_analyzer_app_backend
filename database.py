import firebase_admin
from google.cloud.firestore_v1 import FieldFilter
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime, timedelta
from config import CACHE_HOURS, FIREBASE_CREDENTIALS, SERVICE_ACCOUNT_PATH
import json
import os

# Initialize Firebase only once
def initialize_firebase():
    """Initialize Firebase with credentials from environment or file"""
    if firebase_admin._apps:
        return
    
    try:
        # Priority 1: Use FIREBASE_CREDENTIALS environment variable (JSON string)
        if FIREBASE_CREDENTIALS:
            try:
                cred_dict = json.loads(FIREBASE_CREDENTIALS)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                print("Firebase initialized from environment variable")
                return
            except json.JSONDecodeError:
                print("Warning: FIREBASE_CREDENTIALS is not valid JSON, trying as file path")
                if os.path.exists(FIREBASE_CREDENTIALS):
                    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
                    firebase_admin.initialize_app(cred)
                    print(f"Firebase initialized from file: {FIREBASE_CREDENTIALS}")
                    return
        
        # Priority 2: Use SERVICE_ACCOUNT_PATH file
        if os.path.exists(SERVICE_ACCOUNT_PATH):
            cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
            firebase_admin.initialize_app(cred)
            print(f"Firebase initialized from file: {SERVICE_ACCOUNT_PATH}")
            return
        
        # Priority 3: Try default serviceAccountKey.json
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            print("Firebase initialized from serviceAccountKey.json")
            return
        
        raise FileNotFoundError(
            "No Firebase credentials found. Please set FIREBASE_CREDENTIALS environment variable "
            "or provide serviceAccountKey.json file"
        )
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        raise

initialize_firebase()

db = firestore.client()

COLLECTION = "tweets"

def init_db():
    # Firestore is schemaless, no table creation needed
    pass

def insert_tweets_df(df: pd.DataFrame):
    """Insert a DataFrame of tweets into Firestore."""
    if df is None or df.empty:
        return
    for _, row in df.iterrows():
        doc_ref = db.collection(COLLECTION).document(row['tweet_id'])
        doc_ref.set({
            'query': row['query'],
            'date': row['date'],
            'username': row['username'],
            'content': row['content'],
            'clean_text': row['clean_text'],
            'vader_label': row['vader_label'],
            'vader_score': row['vader_score'],
            'distil_label': row['distil_label'],
            'distil_score': row['distil_score'],
            'inserted_at': datetime.utcnow().isoformat()
        })

def get_cached_tweets(query: str, limit: int = 100):
    """Return cached tweets for a query within CACHE_HOURS."""
    cutoff = datetime.utcnow() - timedelta(hours=CACHE_HOURS)
    docs = (
        db.collection(COLLECTION)
        .where(filter=FieldFilter("query", "==", query))
        .where(filter=FieldFilter("inserted_at", ">=", cutoff.isoformat()))
        .order_by("inserted_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
)


    rows = []
    for doc in docs:
        d = doc.to_dict()
        d['tweet_id'] = doc.id
        rows.append(d)

    if not rows:
        return pd.DataFrame(columns=[
            'tweet_id', 'query', 'date', 'username', 'content',
            'clean_text', 'vader_label', 'vader_score',
            'distil_label', 'distil_score', 'inserted_at'
        ])
    return pd.DataFrame(rows)

def exists_tweet(tweet_id: str) -> bool:
    """Check if a tweet already exists in Firestore."""
    doc_ref = db.collection(COLLECTION).document(tweet_id)
    return doc_ref.get().exists
