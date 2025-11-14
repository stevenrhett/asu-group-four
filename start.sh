#!/bin/bash
# Quick Start Script for Job Portal
# Run this to start the entire application

set -e

echo "🚀 Job Portal - Quick Start"
echo "============================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "⚠️  Docker is not running!"
    echo "👉 Please start Docker Desktop and run this script again."
    echo ""
    echo "Alternative: Start MongoDB locally without Docker:"
    echo "   brew install mongodb-community"
    echo "   brew services start mongodb-community"
    exit 1
fi

# Start MongoDB
echo "📦 Starting MongoDB..."
if docker ps -a | grep -q job-portal-mongo; then
    echo "   MongoDB container exists, starting it..."
    docker start job-portal-mongo > /dev/null 2>&1 || true
else
    echo "   Creating new MongoDB container..."
    docker run -d \
        --name job-portal-mongo \
        -p 27017:27017 \
        mongo:latest > /dev/null 2>&1
fi

# Wait for MongoDB to be ready
echo "   Waiting for MongoDB to be ready..."
sleep 3

# Check MongoDB is running
if docker ps | grep -q job-portal-mongo; then
    echo "   ✅ MongoDB running on localhost:27017"
else
    echo "   ❌ MongoDB failed to start"
    exit 1
fi

echo ""
echo "📚 Next steps:"
echo ""
echo "1️⃣  Start the Backend (in a new terminal):"
echo "   cd backend"
echo "   source venv/bin/activate  # or: python3 -m venv venv && source venv/bin/activate"
echo "   pip install -r requirements.txt  # first time only"
echo "   uvicorn app.main:app --reload --port 8000"
echo ""
echo "2️⃣  Start the Frontend (in another new terminal):"
echo "   cd frontend"
echo "   npm install  # first time only"
echo "   npm run dev"
echo ""
echo "3️⃣  Open your browser:"
echo "   👉 http://localhost:3000"
echo ""
echo "Press CTRL+C to stop this script (MongoDB will keep running)"
echo "To stop MongoDB: docker stop job-portal-mongo"
echo ""

# Keep script running
tail -f /dev/null
