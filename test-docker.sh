#!/bin/bash

# Test script for Vibr Docker setup
echo "🧪 Testing Vibr Docker Setup..."

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build images
echo "🔨 Building Docker images..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Failed to build Docker images"
    exit 1
fi

echo "✅ Docker images built successfully"

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 15

# Test backend health
echo "🔍 Testing backend health..."
BACKEND_HEALTH=$(curl -s http://localhost:8000/health)
if [[ $BACKEND_HEALTH == *"healthy"* ]]; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    docker-compose logs backend
    docker-compose down
    exit 1
fi

# Test frontend
echo "🔍 Testing frontend..."
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ $FRONTEND_RESPONSE -eq 200 ]; then
    echo "✅ Frontend is responding"
else
    echo "❌ Frontend test failed (HTTP $FRONTEND_RESPONSE)"
    docker-compose logs frontend
    docker-compose down
    exit 1
fi

echo ""
echo "🎉 All tests passed! Vibr is running successfully."
echo ""
echo "🌐 Access your application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo ""
echo "📋 To stop the services:"
echo "   docker-compose down"
echo ""
echo "🚀 Happy coding with Vibr!" 