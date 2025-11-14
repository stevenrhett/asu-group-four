#!/bin/bash
# Simple frontend startup script

echo "🚀 Starting Job Portal Frontend"
echo "================================"
echo ""

# Load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"

# Use Node 20
echo "Loading Node.js 20..."
nvm use 20

echo ""
echo "Node version: $(node --version)"
echo "npm version: $(npm --version)"
echo ""

# Navigate to frontend
cd "$(dirname "$0")/frontend"

# Clean and reinstall
echo "Cleaning old dependencies..."
rm -rf node_modules package-lock.json

echo ""
echo "Installing dependencies (this may take 1-2 minutes)..."
npm install

echo ""
echo "✅ Installation complete!"
echo ""
echo "🌐 Starting development server..."
echo "   Press Ctrl+C to stop"
echo ""

# Start dev server
npm run dev

