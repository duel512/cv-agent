# 🚀 Quick Start Guide

**Get your AI assistant running in under 5 minutes!**

---

## Local Testing (Right Now)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here

# 3. Run the application
./start_local.sh

# 4. Open http://localhost:3000 in your browser
```

That's it! Your AI assistant is running locally.

---

## Deploy to Production (10 minutes)

### Step 1: Deploy Backend to Railway (5 min)

```bash
# Option A: Via GitHub (recommended)
git init
git add .
git commit -m "Initial commit"
git push origin main
# Then connect Railway to your GitHub repo

# Option B: Via CLI
npm install -g @railway/cli
railway login
railway init
railway up
railway domain  # Get your backend URL
```

**Add these environment variables in Railway dashboard**:
```
OPENAI_API_KEY=sk-your-actual-key
LLM_PROVIDER=openai
MODEL_NAME=gpt-3.5-turbo
CORS_ORIGINS=*
RATE_LIMIT=10/minute
```

### Step 2: Deploy Frontend to Netlify (3 min)

```bash
# 1. Update frontend/app.js with your Railway URL
# Replace: https://your-railway-app.up.railway.app
# With: https://YOUR-ACTUAL-URL.up.railway.app

# 2. Deploy
npm install -g netlify-cli
netlify login
netlify deploy --dir=frontend --prod
```

### Step 3: Test & Share (2 min)

1. Open your Netlify URL
2. Test with: "Tell me about your background"
3. Add URL to your resume! 🎉

---

## Common Commands

```bash
# Test locally
./start_local.sh

# Check backend health
curl http://localhost:8000/health

# Deploy backend
railway up

# Deploy frontend
netlify deploy --dir=frontend --prod

# View Railway logs
railway logs

# Test prompt generation
cd backend && python prompt_template.py
```

---

## File Locations

```
CV_agent/
├── .env                      ← Add your API key here
├── backend/
│   ├── app.py               ← Main backend server
│   └── data/
│       └── personal_info.json  ← Your CV data
└── frontend/
    └── app.js               ← Update Railway URL here
```

---

## Need Help?

- **Full documentation**: See README.md
- **Deployment guide**: See DEPLOYMENT_GUIDE.md
- **Implementation details**: See IMPLEMENTATION_SUMMARY.md
- **API docs**: http://localhost:8000/docs (when running)

---

## Costs

- **Railway**: $5/month (first $5 free)
- **Netlify**: Free
- **OpenAI API**: ~$2-5/month
- **Total**: ~$7-10/month

---

## URLs to Remember

- OpenAI API Keys: https://platform.openai.com/api-keys
- Railway Dashboard: https://railway.app
- Netlify Dashboard: https://app.netlify.com
- Your Backend: https://YOUR-PROJECT.up.railway.app
- Your Frontend: https://YOUR-SITE.netlify.app

---

Ready to go! 🚀
