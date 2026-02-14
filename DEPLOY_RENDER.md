# 🚀 DEPLOY TO RENDER.COM - STEP BY STEP

## Why Render?
- ✅ FREE tier available
- ✅ Easy deployment
- ✅ Auto-deploys from GitHub
- ✅ Built-in SSL (HTTPS)
- ✅ Custom domains supported

---

## Prerequisites

1. ✅ Groq API Key (get free from https://console.groq.com)
2. ✅ GitHub account
3. ✅ All your project files

---

## STEP 1: Prepare Your GitHub Repository

### 1.1 Create New Repository on GitHub

1. Go to https://github.com
2. Click **"New repository"**
3. Name it: `heart-health-assistant`
4. Make it **Public** (required for free Render tier)
5. Don't add README, .gitignore, or license
6. Click **"Create repository"**

### 1.2 Upload Your Files

**Option A: Using GitHub Web Interface (Easiest)**

1. In your new repository, click **"uploading an existing file"**
2. Drag and drop ALL files from your `cloud-deployment` folder:
   - app.py
   - main.py
   - vector.py
   - heart_medicine_dataset.csv
   - requirements.txt
   - .env.example
   - templates/ folder (with index.html inside)
3. Write commit message: "Initial commit"
4. Click **"Commit changes"**

**Option B: Using Git Command Line**

```bash
cd cloud-deployment
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/heart-health-assistant.git
git push -u origin main
```

---

## STEP 2: Deploy on Render

### 2.1 Sign Up for Render

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub account** (recommended)

### 2.2 Create New Web Service

1. From Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Click **"Connect GitHub"** (if not already connected)
4. Find and select your `heart-health-assistant` repository
5. Click **"Connect"**

### 2.3 Configure Your Service

Fill in these settings:

**Basic Info:**
- **Name:** `heart-health-assistant` (or any name you like)
- **Region:** Choose closest to your users
- **Branch:** `main`
- **Root Directory:** Leave empty

**Build & Deploy:**
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`

**Plan:**
- Select **"Free"** (starts with 0)

### 2.4 Add Environment Variables

1. Scroll down to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Add:
   ```
   Key: GROQ_API_KEY
   Value: your_groq_api_key_here
   ```
   (Paste your actual Groq API key)

4. Click **"Add"**

### 2.5 Deploy!

1. Scroll to bottom
2. Click **"Create Web Service"**
3. Render will start building...

---

## STEP 3: Wait for Deployment

### What Happens:

1. **Building** (2-3 minutes)
   - Installs Python dependencies
   - Downloads HuggingFace models
   - Creates vector store

2. **Live** ✅
   - Your app is deployed!
   - You'll see a green "Live" badge

### Your URL

You'll get a URL like:
```
https://heart-health-assistant.onrender.com
```

---

## STEP 4: Test Your Deployment

1. Click on your URL
2. You should see the Jupiter UI!
3. Try entering symptoms:
   - "mild chest pain when exercising"
4. Click "Analyze Symptoms"
5. Wait 5-10 seconds (first request is slower)
6. See the AI recommendation!

---

## 🎉 SUCCESS! Your Website is Live!

Share your URL with anyone:
```
https://heart-health-assistant.onrender.com
```

---

## ⚠️ Important Notes for Free Tier

### Sleep Mode
- Free tier apps sleep after 15 minutes of inactivity
- First request after sleeping takes ~30 seconds (waking up)
- Subsequent requests are fast

### Solutions:
1. **Upgrade to paid ($7/month)** - Always on
2. **Use Cron Job** - Keep it awake (free)
   - Use https://cron-job.org
   - Ping your URL every 10 minutes
3. **Accept the wait** - Fine for personal projects

---

## 🔧 Troubleshooting

### Build Failed

**Error: "Could not find requirements.txt"**
- Make sure `requirements.txt` is in root of your repository
- Check GitHub - file should be visible

**Error: "Module not found"**
- Check `requirements.txt` has all dependencies
- Try adding missing module to requirements.txt

### Deploy Failed

**Error: "Port already in use"**
- Render handles ports automatically
- Make sure your app.py has: `port = int(os.environ.get("PORT", 5000))`

**Error: "GROQ_API_KEY not set"**
- Go to Render dashboard → your service → Environment
- Add GROQ_API_KEY variable
- Redeploy

### Runtime Errors

**502 Bad Gateway**
- Check Render logs (in dashboard)
- Usually means app crashed
- Look for Python errors in logs

**Slow responses**
- First request creates vector store (slow)
- faiss_index will be cached
- Subsequent requests are faster

---

## 🔄 Updating Your App

When you make changes:

1. Update files on GitHub
2. Commit and push
3. Render **auto-deploys** new version!
4. No manual steps needed

Or manually trigger deploy:
1. Go to Render dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

---

## 📊 Monitoring

### View Logs

1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time logs

### Check Health

Visit: `https://your-app.onrender.com/api/health`

Should return:
```json
{
  "status": "running",
  "model": "Groq Llama 3.1 70B",
  "api_key_configured": true,
  "embeddings": "HuggingFace (free)"
}
```

---

## 🎨 Custom Domain (Optional)

Free custom domain:

1. Buy domain (e.g., from Namecheap)
2. In Render dashboard → Settings → Custom Domains
3. Add your domain
4. Update DNS records as shown
5. Wait for SSL certificate (automatic)

---

## 💰 Upgrading to Paid (Optional)

Benefits of $7/month plan:
- ✅ No sleep mode (always on)
- ✅ Faster responses
- ✅ More reliable
- ✅ Better for production

To upgrade:
1. Dashboard → your service → Settings
2. Change instance type to "Starter"
3. Add payment method

---

## ✅ Final Checklist

- ☐ GitHub repo created with all files
- ☐ Render account created
- ☐ Web service connected to GitHub
- ☐ GROQ_API_KEY environment variable set
- ☐ Deployment successful
- ☐ Tested URL - Jupiter UI loads
- ☐ Tested AI - recommendations work
- ☐ Shared URL with others

---

## 🎉 You're Live!

Your Heart Health Assistant is now accessible to anyone in the world!

**Next Steps:**
- Share your URL
- Monitor usage in Render dashboard
- Consider upgrading if you get lots of traffic

Need help? Check Render docs: https://render.com/docs
