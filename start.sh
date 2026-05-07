#!/bin/bash
# ShopVN Complete Project Startup Script
# Usage: chmod +x start.sh && ./start.sh

echo "================================"
echo "ShopVN - E-Commerce Platform"
echo "Intelligent ML-Driven System"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed!"
    echo "Please install Docker from https://www.docker.com/"
    exit 1
fi

echo -e "${BLUE}[1/3]${NC} Building Docker images..."
cd docker
docker-compose build --no-cache

echo ""
echo -e "${BLUE}[2/3]${NC} Starting services..."
docker-compose up -d

echo ""
echo -e "${BLUE}[3/3]${NC} Waiting for services to be ready..."
sleep 5

# Check health
echo ""
echo "================================"
echo -e "${GREEN}Services Started!${NC}"
echo "================================"
echo ""
echo "Backend API:"
echo "  URL: http://localhost:8000"
echo "  Docs: http://localhost:8000/docs"
echo ""
echo "Seller Dashboard:"
echo "  URL: http://localhost:3001"
echo ""
echo "Buyer Portal:"
echo "  URL: http://localhost:3002"
echo ""
echo "================================"
echo "Commands:"
echo "  View logs:  docker-compose -f docker/docker-compose.yml logs -f"
echo "  Stop:       docker-compose -f docker/docker-compose.yml down"
echo "  Restart:    docker-compose -f docker/docker-compose.yml restart"
echo "================================"
echo ""
