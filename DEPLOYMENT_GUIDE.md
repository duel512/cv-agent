# 🚀 Deployment Guide

Complete step-by-step guide to deploy your Personal AI Assistant online.

## 📋 Prerequisites

Before deploying, make sure you have:

- [ ] OpenAI API key (or Anthropic API key)
- [ ] GitHub account (recommended for easier deployment)
- [ ] Railway account (sign up at https://railway.app)
- [ ] Netlify account (sign up at https://netlify.com)

## 🔧 Step 1: Get Your LLM API Key

### Option A: OpenAI (Recommended for simplicity)

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-...`)
4. Add $5-10 credits to your account at https://platform.openai.com/account/billing

**Cost**: ~$0.002 per conversation (very cheap!)

### Option B: Anthropic Claude (Cheaper, but slightly more complex)

1. Go to https://console.anthropic.com/
2. Create an API key
3. Copy the key (starts with `sk-ant-...`)
4. Add credits to your account

**Cost**: ~$0.0004 per conversation (even cheaper!)

---

## 🚂 Step 2: Deploy Backend to Railway

Railway is a platform that makes deploying Python apps super easy.

### Method 1: Deploy via GitHub (Recommended)

1. **Push your code to GitHub**:
```bash
cd /Users/ruomushao/Documents/Projects_Py/CV_agent
git init
git add .
git commit -m "Initial commit: Personal AI Assistant"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/cv-agent.git
git push -u origin main
```

2. **Connect Railway to GitHub**:
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `cv-agent` repository
   - Railway will automatically detect it's a Python project

3. **Configure environment variables**:
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add these variables:

   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   LLM_PROVIDER=openai
   MODEL_NAME=gpt-3.5-turbo
   CORS_ORIGINS=*
   RATE_LIMIT=10/minute
   PORT=8000
   ```

   **Or if using Anthropic**:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   LLM_PROVIDER=anthropic
   MODEL_NAME=claude-3-haiku-20240307
   CORS_ORIGINS=*
   RATE_LIMIT=10/minute
   PORT=8000
   ```

4. **Deploy**:
   - Railway will automatically build and deploy
   - Wait for deployment to complete (2-3 minutes)

5. **Get your backend URL**:
   - Click "Settings" → "Generate Domain"
   - Copy the URL (e.g., `https://cv-agent-production.up.railway.app`)
   - **Save this URL** - you'll need it for the frontend!

### Method 2: Deploy via Railway CLI

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login**:
```bash
railway login
```

3. **Initialize and deploy**:
```bash
cd /Users/ruomushao/Documents/Projects_Py/CV_agent
railway init
railway up
```

4. **Set environment variables**:
```bash
railway variables set OPENAI_API_KEY=sk-your-key-here
railway variables set LLM_PROVIDER=openai
railway variables set MODEL_NAME=gpt-3.5-turbo
railway variables set CORS_ORIGINS=*
railway variables set RATE_LIMIT=10/minute
```

5. **Generate domain**:
```bash
railway domain
```

### Verify Backend is Working

Test your backend with curl:
```bash
curl https://YOUR-RAILWAY-URL.up.railway.app/health

# Should return:
# {"status":"healthy","provider":"openai","model":"gpt-3.5-turbo"}
```

---

## 🌐 Step 3: Deploy Frontend to Netlify

### Important: Update Backend URL First!

Before deploying, update `frontend/app.js`:

1. Open `frontend/app.js`
2. Find this line:
```javascript
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://your-railway-app.up.railway.app'; // Replace with your Railway URL
```

3. Replace `your-railway-app.up.railway.app` with your actual Railway URL

### Method 1: Deploy via Netlify Dashboard (Easiest)

1. **Go to Netlify**:
   - Visit https://app.netlify.com
   - Click "Add new site" → "Deploy manually"

2. **Drag and drop**:
   - Drag the entire `frontend` folder into the upload area
   - Netlify will deploy it instantly

3. **Get your URL**:
   - Copy the URL (e.g., `https://silly-name-123456.netlify.app`)
   - You can customize this in Site settings → Domain management

### Method 2: Deploy via Netlify CLI

1. **Install Netlify CLI**:
```bash
npm install -g netlify-cli
```

2. **Login**:
```bash
netlify login
```

3. **Deploy**:
```bash
cd /Users/ruomushao/Documents/Projects_Py/CV_agent
netlify deploy --dir=frontend --prod
```

4. **Get your URL**:
   - Netlify will show you the deployed URL
   - Example: `https://ruomu-ai-assistant.netlify.app`

### Method 3: Deploy via GitHub (Auto-deploy on push)

1. **Connect Netlify to GitHub**:
   - In Netlify dashboard, click "Add new site" → "Import from Git"
   - Connect to GitHub and select your repository
   - Configure:
     - Base directory: (leave empty)
     - Build command: `echo "No build needed"`
     - Publish directory: `frontend`

2. **Deploy**:
   - Netlify will automatically deploy
   - Every push to `main` branch will auto-deploy

---

## ✅ Step 4: Test Your Deployed Application

1. **Open your Netlify URL** in a browser
   - Example: `https://ruomu-ai-assistant.netlify.app`

2. **Test the chat**:
   - Try: "Tell me about your background"
   - Try: "What experience do you have with Python?"
   - Try: "What projects have you worked on?"

3. **Check for errors**:
   - Open browser console (F12)
   - Look for any red errors
   - If you see CORS errors, make sure `CORS_ORIGINS=*` is set in Railway

---

## 📝 Step 5: Add URL to Your Resume

Once deployed, add the URL to your resume:

**Option 1: Direct link**:
```
Portfolio: https://ruomu-ai-assistant.netlify.app
```

**Option 2: QR Code**:
1. Generate QR code at https://qr.io
2. Add to resume with text "Scan to chat with my AI assistant"

**Option 3: Custom domain** (optional):
1. Buy a domain (e.g., `ruomushao.com`)
2. In Netlify: Settings → Domain management → Add custom domain
3. Update DNS records as instructed

---

## 🔧 Maintenance & Updates

### Update Your CV Information

1. Edit `backend/data/personal_info.json`
2. Commit and push to GitHub (if using GitHub deployment)
3. Or re-deploy via CLI

Railway will automatically redeploy when you push to GitHub.

### Update the System Prompt

1. Edit `backend/prompt_template.py`
2. Commit and push
3. Railway will automatically redeploy

### Monitor Costs

**Railway**:
- Dashboard → Your project → Usage
- You get $5 free credit
- After that, ~$5/month for hosting

**OpenAI**:
- https://platform.openai.com/usage
- ~$2-5/month for moderate traffic
- Set spending limits to avoid surprises

**Netlify**:
- Free tier is plenty for this use case
- Check bandwidth in dashboard

### Check Logs

**Railway logs**:
```bash
railway logs
```

**Netlify logs**:
- Dashboard → Site → Deploys → [Click on a deploy] → Deploy log

---

## 🐛 Troubleshooting

### Frontend shows "Cannot connect to server"

**Problem**: Frontend can't reach backend

**Solutions**:
1. Check if backend is running: visit `https://YOUR-RAILWAY-URL.up.railway.app/health`
2. Verify `API_BASE_URL` in `frontend/app.js` is correct
3. Check CORS is set to `*` in Railway environment variables
4. Make sure Railway app is not sleeping (visit the URL to wake it)

### Backend shows "OpenAI API error"

**Problem**: OpenAI API key issue

**Solutions**:
1. Verify API key is correct in Railway variables
2. Check you have credits: https://platform.openai.com/account/billing
3. Try regenerating API key and updating in Railway
4. Check Railway logs: `railway logs`

### Rate limit errors

**Problem**: Too many requests from one IP

**Solutions**:
1. Increase `RATE_LIMIT` environment variable (e.g., `20/minute`)
2. Or implement per-user rate limiting in `backend/app.py`

### Railway app keeps crashing

**Problem**: Backend not starting properly

**Solutions**:
1. Check Railway logs for error messages
2. Verify all environment variables are set
3. Test locally first: `cd backend && python app.py`
4. Check `Procfile` and `railway.json` are correct

---

## 💰 Cost Optimization Tips

1. **Use GPT-3.5-turbo** (not GPT-4) - 10x cheaper
2. **Use Claude Haiku** - Even cheaper than GPT-3.5
3. **Set spending limits** in OpenAI/Anthropic dashboard
4. **Enable rate limiting** (already configured)
5. **Monitor usage** weekly to catch any spikes
6. **Limit max_tokens** to 300 (already set in code)

---

## 🎉 You're Done!

Your AI assistant is now live! Share the URL with:
- Recruiters and hiring managers
- In your resume and cover letters
- On your LinkedIn profile
- In your email signature

**Example usage in resume**:
```
🤖 Chat with my AI Assistant: https://ruomu-ai-assistant.netlify.app
Learn about my background, skills, and experience interactively!
```

---

## 📞 Need Help?

If you run into issues:

1. Check this guide again
2. Check Railway/Netlify documentation
3. Review error messages carefully
4. Test locally first with `./start_local.sh`
5. Check browser console for frontend errors (F12)

Good luck! 🚀
