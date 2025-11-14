#!/bin/zsh
# Complete startup script for Job Portal Application

set -e

echo "🚀 Job Portal - Complete Startup Script"
echo "========================================"
echo ""

# Load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Check current Node version
CURRENT_NODE=$(node --version 2>/dev/null || echo "none")
echo "📦 Current Node.js version: $CURRENT_NODE"

# Install and use Node 20 if needed
if [[ "$CURRENT_NODE" != v20* ]]; then
    echo "⚙️  Installing Node.js 20..."
    nvm install 20 --silent
    nvm use 20
    nvm alias default 20
    echo "✅ Node.js 20 installed and activated"
else
    echo "✅ Node.js 20 already active"
fi

echo ""
echo "Node version: $(node --version)"
echo "npm version: $(npm --version)"
echo ""

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Backend already running on port 8000"
else
    echo "Starting backend in background..."
    cd backend
    if [ -d "venv" ]; then
        source venv/bin/activate
        uvicorn app.main:app --reload --port 8000 > /tmp/jobportal-backend.log 2>&1 &
        echo "✅ Backend started (PID: $!)"
        echo "   Logs: /tmp/jobportal-backend.log"
    else
        echo "❌ Backend venv not found. Run: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    fi
    cd ..
fi

echo ""

# Setup and start frontend
echo "📦 Setting up frontend..."
cd frontend

# Clean and reinstall if needed
if [ ! -d "node_modules" ] || [[ "$CURRENT_NODE" != v20* ]]; then
    echo "   Installing dependencies..."
    rm -rf node_modules package-lock.json
    npm install
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting frontend development server..."
echo "   This will run in the foreground. Press Ctrl+C to stop."
echo ""
sleep 2

npm run dev

