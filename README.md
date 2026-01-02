# Real-Time Sentiment Monitoring System - Backend API

A **FastAPI-based backend** for real-time sentiment analysis of tweets using the **X (Twitter) API**. This backend provides REST API endpoints for Flutter mobile applications and uses **VADER** and **DistilBERT** models for sentiment analysis. Data is stored in **Firebase Firestore** for caching and persistence.

> **🚀 NEW TO DEPLOYMENT?** → Start here: [START_HERE.md](START_HERE.md)

---

## 🚀 Features

- 🔴 **Real-time tweet fetching** using the X API (via Tweepy)
- 🧠 **Dual sentiment analysis models**:
  - **VADER** (rule-based, fast)
  - **DistilBERT** (transformer-based, deep learning)
- 🎯 **RESTful API** built with FastAPI
- ☁️ **Firebase Firestore backend** to store:
  - Search queries
  - Usernames
  - Tweets
  - Sentiment scores from both models
  - Timestamps
- ⚡ **Smart caching mechanism**:
  - If a user searches the same query within **10 hours**, results are fetched from Firebase
  - Reduces API usage and improves response time
- 📱 **Mobile-ready**: Optimized for Flutter Android/iOS apps
- 🌐 **CORS enabled**: Works with cross-origin requests
- 🚂 **Railway.app ready**: Easy deployment with environment variables

---

## 🏗️ System Architecture

```
Flutter App (Android/iOS)
        ↓
FastAPI Backend (Railway.app)
        ↓
X API (Tweepy)  ←── Cache Check (Firebase, 10 hours)
        ↓
Sentiment Analysis (VADER / DistilBERT)
        ↓
Firebase Firestore Database
```

---

## 📦 Tech Stack

- **Framework**: FastAPI + Uvicorn
- **Database**: Firebase Firestore
- **ML Models**: VADER, DistilBERT (Hugging Face Transformers)
- **Deployment**: Railway.app
- **API Client**: Tweepy (Twitter/X API v2)
- **APIs**: X (Twitter) API
- **NLP Models**: VADER, DistilBERT

---

## � Quick Deploy to Railway

**Want to deploy in 5 minutes?** Follow the [QUICKSTART.md](QUICKSTART.md) guide!

For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📋 Local Development Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/sentiment-backend.git
cd sentiment-backend
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ X API Configuration

- Create a developer account on **X (Twitter)**
- Generate API Bearer Token
- Add to environment variables or `.env` file:

````bash
TWITTER_BEARER_TOKEN=your_bearer_token_here
* Generate a **service account key (JSON)** - download as `serviceAccountKey.json`
* Place the file in the project root OR set as environment variable

```bash
# Option 1: Use file (for local development)
# Place serviceAccountKey.json in project root

# Option 2: Use environment variable (for Railway)
export FIREBASE_CREDENTIALS='{"type":"service_account",...}'
````

### 6️⃣ Download NLTK Data

```bash
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

### 7️⃣ Run Locally

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

```
http://localhost:8000
```

### 8️⃣ Test the API

Open browser:

```
http://localhost:8000/health
```

---

## 📱 Flutter Integration

See [flutter_integration_example.dart](flutter_integration_example.dart) for complete Flutter code examples.

### Quick Flutter Setup

1. **Add HTTP package** to `pubspec.yaml`:

```yaml
dependencies:
  http: ^1.1.0
```

2. **Update API URL** in your Flutter app:

```dart
static const String baseUrl = 'https://your-app.railway.app';
```

3. **Add Internet Permission** (Android):

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

---

## 🚀 Deploy to Production

### Deploy to Railway.app

Follow these guides:

- **Quick (5 min)**: [QUICKSTART.md](QUICKSTART.md)
- **Detailed**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## 📊 API Endpoints

| Method | Endpoint   | Description                      |
| ------ | ---------- | -------------------------------- |
| GET    | `/`        | API information                  |
| GET    | `/health`  | Health check                     |
| POST   | `/fetch`   | Fetch tweets from Twitter        |
| GET    | `/tweets`  | Get cached tweets with sentiment |
| POST   | `/predict` | Run sentiment analysis           |

### Example API Calls

#### Fetch Tweets

```bash
curl -X POST http://localhost:8000/fetch \
  -H "Content-Type: application/json" \
  -d '{"query": "flutter", "limit": 50}'
```

#### Get Analyzed Tweets

```bash
curl "http://localhost:8000/tweets?query=flutter&limit=20"
```

---

## 🧠 Sentiment Models

### VADER

- Rule-based sentiment analyzer
- Fast and lightweight
- Ideal for social media text

### DistilBERT

- Transformer-based deep learning model
- More accurate contextual understanding
- Computationally heavier

Users can select the model directly from the UI.

---

## 🧪 Caching Logic (10 Hours)

- Every query is stored with a timestamp in Firebase
- When the same query is searched again:

  - If the time difference ≤ **10 hours**, cached data is returned
  - Otherwise, fresh tweets are fetched from X API

---

## 📌 Future Enhancements

- Live sentiment streaming dashboard
- Support for multilingual sentiment analysis
- User authentication with Firebase Auth
- Topic-wise sentiment comparison
- Deployment on cloud platforms

---

## 👨‍💻 Author

**Bilal Rafique**
BS (Computer Science)

---

## 📜 License

This project is for educational and research purposes.

---

⭐ If you like this project, consider giving it a star on GitHub!
