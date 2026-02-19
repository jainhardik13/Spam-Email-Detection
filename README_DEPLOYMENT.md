# 🚀 Spam Email Detector - Render Deployment Guide

## 📋 Prerequisites
- GitHub account
- Render account (free tier works fine)
- Your code pushed to a GitHub repository

---

## 🛠️ Deployment Steps

### Option 1: Using render.yaml (Recommended - Easiest)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and configure everything
   - Click **"Apply"** to deploy

3. **Done!** Your app will be live at: `https://spam-email-detector-xxxx.onrender.com`

---

### Option 2: Manual Setup (More Control)

1. **Push code to GitHub**

2. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository

3. **Configure the service:**
   - **Name:** `spam-email-detector`
   - **Region:** Choose closest to you
   - **Branch:** `main` (or your default branch)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan:** `Free`

4. **Environment Variables (Optional):**
   - `PYTHON_VERSION`: `3.11.0` (or your version)

5. **Click "Create Web Service"**

---

## ✅ Verification

Once deployed, test these endpoints:

1. **Health Check:**
   ```
   GET https://your-app-name.onrender.com/health
   ```
   Should return: `{"status":"healthy","message":"Spam Detection API is running"}`

2. **Home Page:**
   ```
   GET https://your-app-name.onrender.com/
   ```
   Should display the spam detector UI

3. **API Test:**
   ```bash
   curl -X POST https://your-app-name.onrender.com/predict \
     -H "Content-Type: application/json" \
     -d '{"message":"Congratulations! You won $1000. Click here to claim."}'
   ```

---

## 🐛 Troubleshooting

### Issue: "No open ports detected"
**Solution:** The start command must include `--host 0.0.0.0 --port $PORT`
- ✅ Correct: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- ❌ Wrong: `python app.py`

### Issue: Module not found
**Solution:** Ensure all dependencies are in `requirements.txt`
```bash
pip freeze > requirements.txt
```

### Issue: Model files not loading
**Solution:** Verify files are committed to Git:
```bash
git add Model/*.pkl
git commit -m "Add model files"
git push
```

### Issue: Build failed
**Solution:** Check Render logs for specific errors
- Common: Missing dependencies, incompatible Python version

### Issue: Service running but showing JSON instead of HTML
**Solution:** Check that:
1. `Frontend/index.html` exists in your repo
2. The path in `app.py` is correct: `BASE_DIR / "Frontend" / "index.html"`
3. File is committed to Git

---

## 📊 Performance Notes

### Free Tier Limitations:
- **Spin down after 15 minutes** of inactivity
- **Spin up time:** ~30-60 seconds on first request after inactivity
- **Memory:** 512 MB
- **Build time:** ~2-5 minutes

### Optimization Tips:
1. **Use smaller models** if possible
2. **Enable persistent disk** for paid plans (keeps service always running)
3. **Cache model loading** (already implemented with module-level loading)

---

## 🔄 Updating the Deployment

To update your deployed app:

```bash
# Make your changes
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically detect the push and redeploy! 🎉

---

## 📝 Important Files for Render

- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration (optional)
- ✅ `app.py` - Main FastAPI application
- ✅ `Model/spam_model1.pkl` - Trained model
- ✅ `Model/vectorizer1.pkl` - TF-IDF vectorizer
- ✅ `Frontend/index.html` - User interface

---

## 🆚 Render vs Vercel Comparison

| Feature | Render | Vercel |
|---------|--------|--------|
| ML Models | ✅ Great (no size limit) | ❌ Limited (50MB max) |
| Persistent Server | ✅ Yes | ❌ Serverless only |
| Free Tier | 750 hours/month | 100GB bandwidth |
| Cold Start | ~30-60s | ~5-10s |
| Best For | ML/AI apps, APIs | Static sites, NextJS |

**For ML applications like this spam detector, Render is the better choice! ✅**

---

## 📞 Need Help?

- [Render Documentation](https://render.com/docs)
- [Render Community Forum](https://community.render.com/)
- Check Render logs for deployment errors

---

## 🎉 Success!

Your spam detector is now live and accessible worldwide! Share the URL with others to try it out.

