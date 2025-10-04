# Personal AI Assistant - Ruomu Shao

An AI-powered chatbot that represents my professional profile for recruitment purposes. Built with FastAPI backend and vanilla JavaScript frontend, deployed on Railway and Netlify.

🔗 **Live Demo**: [Coming soon - add your Netlify URL here]

## 📋 Overview

This project provides an interactive AI assistant that can answer questions about my professional background, skills, experience, and qualifications. It's designed to give recruiters and hiring managers an engaging way to learn about me.

### Key Features

- ✅ **AI-Powered Responses**: Uses OpenAI GPT-3.5-turbo or Anthropic Claude for natural conversations
- ✅ **Complete CV Context**: Full professional profile embedded in every response
- ✅ **Cost-Effective**: No fine-tuning needed, minimal hosting costs (~$7-10/month)
- ✅ **Easy to Update**: Simply edit JSON file to update CV information
- ✅ **Professional UI**: Clean, responsive chat interface
- ✅ **Rate Limited**: Prevents abuse with 10 requests/minute per IP
- ✅ **Mobile Friendly**: Works seamlessly on all devices

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Netlify   │ ───────>│   Railway    │ ───────>│ OpenAI API  │
│  (Frontend) │         │  (Backend)   │         │  or Claude  │
└─────────────┘         └──────────────┘         └─────────────┘
     HTML/CSS/JS         FastAPI + Python         GPT-3.5/Haiku
```

### Tech Stack

**Backend**:
- FastAPI (Python web framework)
- OpenAI API or Anthropic Claude
- SlowAPI (rate limiting)
- Deployed on Railway

**Frontend**:
- Vanilla HTML/CSS/JavaScript (no framework)
- Deployed on Netlify

**Data**:
- JSON file (no database needed)
- Full CV fits in LLM context window

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key OR Anthropic API key
- Railway account (for backend deployment)
- Netlify account (for frontend deployment)

### Local Development

1. **Clone and setup**:
```bash
cd CV_agent
```

2. **Install backend dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env and add your API key
```

Example `.env`:
```env
# Choose OpenAI (recommended for cost)
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
MODEL_NAME=gpt-3.5-turbo

# OR choose Anthropic
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# LLM_PROVIDER=anthropic
# MODEL_NAME=claude-3-haiku-20240307

PORT=8000
CORS_ORIGINS=*
RATE_LIMIT=10/minute
```

4. **Run the backend**:
```bash
cd backend
python app.py
# Backend runs on http://localhost:8000
```

5. **Run the frontend**:
```bash
# In a new terminal
cd frontend
# Open index.html in a browser or use a local server:
python -m http.server 3000
# Frontend runs on http://localhost:3000
```

6. **Test the chat**:
- Open http://localhost:3000 in your browser
- Start chatting with the AI assistant

## 📦 Deployment

### Backend Deployment (Railway)

1. **Install Railway CLI**:
```bash
npm i -g @railway/cli
```

2. **Login to Railway**:
```bash
railway login
```

3. **Initialize project**:
```bash
railway init
# Select "Create a new project"
```

4. **Add environment variables**:
```bash
railway variables set OPENAI_API_KEY=sk-your-key-here
railway variables set LLM_PROVIDER=openai
railway variables set MODEL_NAME=gpt-3.5-turbo
railway variables set CORS_ORIGINS=*
railway variables set RATE_LIMIT=10/minute
```

5. **Deploy**:
```bash
railway up
```

6. **Get your backend URL**:
```bash
railway domain
# Example: https://cv-agent-production.up.railway.app
```

7. **Copy this URL** - you'll need it for the frontend configuration.

### Frontend Deployment (Netlify)

1. **Update backend URL in frontend**:
Edit `frontend/app.js` and replace the Railway URL:
```javascript
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://YOUR-RAILWAY-URL.up.railway.app'; // Replace this!
```

2. **Install Netlify CLI**:
```bash
npm i -g netlify-cli
```

3. **Login to Netlify**:
```bash
netlify login
```

4. **Deploy**:
```bash
netlify deploy --dir=frontend --prod
```

5. **Get your frontend URL**:
- Netlify will provide a URL like: `https://ruomu-ai-assistant.netlify.app`
- Add this URL to your resume!

### Alternative: Deploy via GitHub

Both Railway and Netlify support automatic deployment from GitHub:

1. Push your code to GitHub
2. Connect your Railway/Netlify account to the repository
3. Configure environment variables in the dashboard
4. Automatic deployments on every push

## 📝 Customization

### Update Your CV Data

Edit `backend/data/personal_info.json` with your information:

```json
{
  "name": "Your Name",
  "title": "Your Title",
  "contact": {
    "email": "your.email@example.com",
    ...
  },
  ...
}
```

Changes take effect immediately - just restart the backend or redeploy.

### Modify the System Prompt

Edit `backend/prompt_template.py` to customize how the AI responds:
- Change tone and personality
- Add/remove sections
- Modify conversation examples
- Adjust response guidelines

### Customize the UI

Edit `frontend/style.css` to change:
- Colors (modify CSS variables in `:root`)
- Layout and spacing
- Fonts and typography
- Mobile responsiveness

## 💰 Cost Breakdown

### Monthly Operating Costs

| Service | Cost | Notes |
|---------|------|-------|
| Railway (Backend) | $5/month | Includes $5 free credit initially |
| Netlify (Frontend) | $0 | Free tier sufficient |
| OpenAI API (GPT-3.5) | ~$2-5/month | Based on ~1000-2000 conversations |
| **Total** | **~$7-10/month** | Scales with usage |

### Cost Optimization Tips

1. Use **GPT-3.5-turbo** instead of GPT-4 (10x cheaper)
2. Or use **Claude Haiku** (even cheaper than GPT-3.5)
3. Set `max_tokens=300` to limit response length
4. Enable rate limiting to prevent abuse
5. Monitor usage in OpenAI/Anthropic dashboard

## 🧪 Testing

### Test the Prompt Template

```bash
cd backend
python prompt_template.py
```

This will print the full system prompt to verify it looks correct.

### Test the Backend API

```bash
# Start the backend
cd backend
python app.py

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/welcome

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What experience do you have with Python?",
    "conversation_history": []
  }'
```

### Test the Frontend

Open `http://localhost:3000` and try these questions:
- "Tell me about your background"
- "What experience do you have with networking?"
- "What projects have you worked on?"
- "What are your technical skills?"
- "How can I contact you?"

## 📚 Project Structure

```
CV_agent/
├── backend/
│   ├── app.py                    # FastAPI server
│   ├── prompt_template.py        # System prompt generator
│   ├── requirements.txt          # Python dependencies
│   └── data/
│       └── personal_info.json    # Your CV data
├── frontend/
│   ├── index.html               # Chat UI
│   ├── style.css                # Styling
│   └── app.js                   # Chat logic
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── railway.json                 # Railway config
├── Procfile                     # Railway process
├── runtime.txt                  # Python version
├── netlify.toml                 # Netlify config
└── README.md                    # This file
```

## 🔒 Security Considerations

- ✅ Rate limiting (10 req/min per IP)
- ✅ CORS properly configured
- ✅ API keys stored in environment variables
- ✅ No sensitive data in frontend code
- ✅ Input validation on backend
- ✅ Max token limits to prevent cost abuse

## 🐛 Troubleshooting

### Backend Issues

**Error: "OpenAI API error"**
- Check your API key is valid
- Verify you have credits in your OpenAI account
- Check the model name is correct

**Error: "Module not found"**
- Run `pip install -r requirements.txt`
- Make sure you're in the `backend/` directory

**Error: "Port already in use"**
- Change PORT in `.env` to a different number
- Or kill the process using that port

### Frontend Issues

**Error: "Cannot connect to server"**
- Make sure backend is running
- Check the `API_BASE_URL` in `app.js` is correct
- Verify CORS settings allow your frontend domain

**Chat not loading**
- Check browser console for errors (F12)
- Verify the backend `/welcome` endpoint is working
- Try refreshing the page

### Deployment Issues

**Railway deployment fails**
- Check environment variables are set correctly
- Verify `requirements.txt` is in the `backend/` folder
- Check Railway logs: `railway logs`

**Netlify deployment fails**
- Ensure `netlify.toml` is in project root
- Verify publish directory is set to `frontend`
- Check Netlify deploy logs in dashboard

## 📖 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /welcome` - Get welcome message
- `POST /chat` - Send message and get AI response

## 🤝 Contributing

This is a personal project, but feel free to fork and customize it for your own use!

## 📄 License

MIT License - feel free to use this for your own personal AI assistant.

## 👤 Contact

**Ruomu Shao**
- Email: shaoruomu19@gmail.com
- LinkedIn: [ruomu-shao](https://www.linkedin.com/in/ruomu-shao-71878124b/)
- GitHub: [duel512](https://github.com/duel512)

---

Built with ❤️ using FastAPI, OpenAI, and vanilla JavaScript
