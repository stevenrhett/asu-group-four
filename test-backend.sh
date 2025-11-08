#!/bin/bash
# Quick backend test script

echo "Testing backend connection..."
echo ""

# Test health endpoint
echo "1. Testing /health endpoint:"
curl -s http://localhost:8000/health
echo ""
echo ""

# Test register endpoint
echo "2. Testing /auth/register endpoint:"
curl -s -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","role":"seeker"}'
echo ""
echo ""

echo "Done!"

