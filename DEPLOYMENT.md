# 🚀 Railway.app Deployment Guide

This guide will help you deploy your Sentiment Analysis Backend to Railway.app and connect it to your Flutter mobile app.

## 📋 Prerequisites

1. A [Railway.app](https://railway.app) account (free tier available)
2. A GitHub account (for connecting your repository)
3. Your Twitter API Bearer Token
4. Your Firebase Service Account JSON file

## 🔧 Step 1: Prepare Your Repository

### 1.1 Create a `.gitignore` file (if not exists)

```gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.venv
serviceAccountKey.json
sentiment.db
*.log
.DS_Store
```

### 1.2 Push Your Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit - sentiment analysis backend"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## 🚂 Step 2: Deploy to Railway

### 2.1 Create a New Project

1. Go to [Railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Authenticate with GitHub and select your repository
5. Railway will automatically detect your Python app

### 2.2 Configure Environment Variables

In your Railway project dashboard:

1. Click on your service
2. Go to the "Variables" tab
3. Add the following environment variables:

#### Required Variables:

```bash
TWITTER_BEARER_TOKEN=your_actual_twitter_bearer_token_here
```

```bash
FIREBASE_CREDENTIALS={"type":"service_account","project_id":"your-project-id","private_key_id":"...","private_key":"...","client_email":"..."}
```

> **Important**: For `FIREBASE_CREDENTIALS`, copy the **entire contents** of your `serviceAccountKey.json` file and paste it as a single-line JSON string.

#### Optional Variables (with defaults):

```bash
CACHE_HOURS=10
MAX_TWEETS_PER_CALL=15
ALLOWED_ORIGINS=*
```

### 2.3 Deploy

1. Railway will automatically deploy your application
2. Wait for the build to complete (this may take 5-10 minutes for the first deployment)
3. Once deployed, Railway will provide you with a public URL like:
   ```
   https://your-app-name.railway.app
   ```

## 📱 Step 3: Connect to Your Flutter App

### 3.1 Get Your Railway URL

1. In your Railway project dashboard
2. Click on your service
3. Go to "Settings" tab
4. Find the "Domains" section
5. Copy the generated domain (e.g., `your-app-name.railway.app`)

### 3.2 Update Your Flutter App

In your Flutter app, update the API base URL:

```dart
// lib/config/api_config.dart or wherever you store your API URL
class ApiConfig {
  static const String baseUrl = 'https://your-app-name.railway.app';

  // Endpoints
  static const String fetchTweets = '$baseUrl/fetch';
  static const String getTweets = '$baseUrl/tweets';
  static const String predictSentiment = '$baseUrl/predict';
}
```

### 3.3 Test Your Connection

Test your API endpoints:

```dart
import 'package:http/http.dart' as http;

Future<void> testConnection() async {
  try {
    final response = await http.get(
      Uri.parse('https://your-app-name.railway.app/health'),
    );

    if (response.statusCode == 200) {
      print('✅ Backend connected successfully!');
      print(response.body);
    }
  } catch (e) {
    print('❌ Connection failed: $e');
  }
}
```

## 🔍 Step 4: Testing Your Deployment

### 4.1 Test the Health Endpoint

Open your browser or use curl:

```bash
curl https://your-app-name.railway.app/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "sentiment-analysis-api"
}
```

### 4.2 Test from Your Flutter App

Make a test API call from your Flutter app:

```dart
// Fetch tweets example
final response = await http.post(
  Uri.parse('${ApiConfig.baseUrl}/fetch'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'query': 'flutter',
    'limit': 10,
  }),
);

if (response.statusCode == 200) {
  final data = jsonDecode(response.body);
  print('Fetched ${data['count']} tweets');
}
```

## 🔄 Step 5: Continuous Deployment

Railway automatically redeploys your app when you push changes to GitHub:

```bash
git add .
git commit -m "Update API endpoint"
git push origin main
```

Railway will detect the changes and automatically rebuild and deploy.

## 📊 Monitoring and Logs

### View Logs

1. Go to your Railway project dashboard
2. Click on your service
3. Go to the "Deployments" tab
4. Click on the latest deployment
5. View real-time logs

### Monitor Performance

Railway provides metrics for:

- CPU usage
- Memory usage
- Network traffic
- Request count

## 🐛 Troubleshooting

### Issue: Build Failed

**Solution**: Check the build logs in Railway dashboard. Common issues:

- Missing dependencies in `requirements.txt`
- Syntax errors in Python code
- Missing environment variables

### Issue: App Crashes on Startup

**Solution**:

1. Check that `FIREBASE_CREDENTIALS` is set correctly
2. Verify `TWITTER_BEARER_TOKEN` is valid
3. Review deployment logs for error messages

### Issue: Flutter App Can't Connect

**Solution**:

1. Verify the Railway URL is correct in your Flutter app
2. Check that CORS is enabled (it's set to `*` by default)
3. Test the `/health` endpoint directly in a browser
4. Ensure your mobile device has internet access

### Issue: 502 Bad Gateway

**Solution**:

1. Check that the app is listening on the correct PORT
2. Verify the startup command in `Procfile` is correct
3. Review application logs for startup errors

## 🔒 Security Best Practices

### For Production:

1. **Update CORS settings**:

   ```bash
   ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

2. **Secure your Firebase credentials**:

   - Never commit `serviceAccountKey.json` to Git
   - Use Railway's environment variables

3. **Rate limiting** (optional):
   Consider adding rate limiting to prevent abuse

4. **HTTPS Only**:
   Railway provides HTTPS by default - ensure your Flutter app uses `https://`

## 📱 Flutter App Configuration

### Add Internet Permission (Android)

In `android/app/src/main/AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <!-- ... rest of your manifest -->
</manifest>
```

### Add Network Configuration (iOS)

In `ios/Runner/Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>
    <key>NSExceptionDomains</key>
    <dict>
        <key>railway.app</key>
        <dict>
            <key>NSIncludesSubdomains</key>
            <true/>
            <key>NSTemporaryExceptionAllowsInsecureHTTPLoads</key>
            <false/>
        </dict>
    </dict>
</dict>
```

## 📝 API Endpoints Reference

Once deployed, your API will have these endpoints:

| Method | Endpoint   | Description                                  |
| ------ | ---------- | -------------------------------------------- |
| GET    | `/`        | API information and available endpoints      |
| GET    | `/health`  | Health check endpoint                        |
| POST   | `/fetch`   | Fetch new tweets from Twitter API            |
| GET    | `/tweets`  | Get cached tweets with sentiment analysis    |
| POST   | `/predict` | Run sentiment analysis on unpredicted tweets |

### Example API Calls:

#### Fetch Tweets

```bash
curl -X POST https://your-app-name.railway.app/fetch \
  -H "Content-Type: application/json" \
  -d '{"query": "flutter", "limit": 50}'
```

#### Get Tweets

```bash
curl "https://your-app-name.railway.app/tweets?query=flutter&limit=20"
```

#### Predict Sentiment

```bash
curl -X POST https://your-app-name.railway.app/predict
```

## 🎉 Success!

Your backend is now deployed and ready to use! Your Flutter app can now:

- ✅ Fetch tweets from Twitter
- ✅ Store them in Firebase Firestore
- ✅ Run sentiment analysis
- ✅ Serve results to your mobile app

## 💡 Tips

1. **Monitor your Railway usage** - The free tier has limits
2. **Use caching** - The app caches tweets to reduce API calls
3. **Test thoroughly** - Test all endpoints before releasing your Flutter app
4. **Keep dependencies updated** - Regularly update your `requirements.txt`

## 🆘 Need Help?

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Check Railway status: https://status.railway.app

---

**Happy Deploying! 🚀**
