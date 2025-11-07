#!/bin/bash
# Setup script to install and configure Node.js 20 via nvm

echo "=== Node.js Setup via nvm ==="
echo ""

# Load nvm
export NVM_DIR="$HOME/.nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    echo "✓ Loading nvm..."
    source "$NVM_DIR/nvm.sh"
else
    echo "✗ nvm not found. Installing..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    source "$NVM_DIR/nvm.sh"
fi

echo ""
echo "Current Node version: $(node --version 2>&1)"
echo ""

# Install Node 20
echo "Installing Node.js 20..."
nvm install 20
echo ""

# Use Node 20
echo "Activating Node.js 20..."
nvm use 20
echo ""

# Verify
echo "=== Installation Complete ==="
echo "Node version: $(node --version)"
echo "npm version: $(npm --version)"
echo "Node location: $(which node)"
echo ""

# Make it default
echo "Setting Node 20 as default..."
nvm alias default 20
echo ""

echo "=== Next Steps ==="
echo "1. Close this terminal and open a new one (or run: source ~/.bashrc)"
echo "2. Verify with: node --version (should show v20.x.x)"
echo "3. Then run: cd frontend && npm install && npm run dev"
echo ""

