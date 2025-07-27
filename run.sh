#!/bin/bash

# Vibr - Vibe Coding Playground Docker Runner
echo "🎮 Starting Vibr - Vibe Coding Playground..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed."
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"
    echo "Or install Docker Engine from https://docs.docker.com/engine/install/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is required but not available."
    echo "Please install Docker Compose or use Docker Desktop which includes it."
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running."
    echo "Please start Docker Desktop or Docker Engine and try again."
    exit 1
fi

echo "✅ Docker environment check passed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cat > .env << EOF
# Anthropic API Key (optional - you can add this later)
ANTHROPIC_API_KEY=

# Database settings
DATABASE_URL=sqlite:///./vibr.db

# Security
SECRET_KEY=your-secret-key-change-in-production
EOF
    echo "📝 Created .env file. You can edit it to add your API keys."
fi

# Build and start the containers
echo "🔨 Building and starting containers..."
if command -v docker-compose &> /dev/null; then
    docker-compose up --build -d
else
    docker compose up --build -d
fi

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
if command -v docker-compose &> /dev/null; then
    docker-compose ps
else
    docker compose ps
fi

echo ""
echo "🎉 Vibr is now running!"
echo ""
echo "🌐 Access your application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo ""
echo "🚀 Happy coding with Vibr!" 