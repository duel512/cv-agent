#!/bin/bash

# Local development startup script for Personal AI Assistant

echo "🚀 Starting Personal AI Assistant..."
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Please copy .env.example to .env and add your API keys:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your API key"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking backend dependencies..."
cd backend
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
fi

# Start the backend
echo ""
echo "✅ Starting backend on http://localhost:8000"
echo "📝 API docs available at http://localhost:8000/docs"
echo ""
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Open frontend
echo "✅ Opening frontend..."
echo "🌐 Frontend available at http://localhost:3000"
echo ""
cd ../frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo ""
echo "================================"
echo "✨ Application is running!"
echo "================================"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Handle Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for processes
wait
