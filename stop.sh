#!/bin/bash
# ShopVN Shutdown Script

echo "Stopping ShopVN services..."
echo ""

cd docker
docker-compose down

echo ""
echo "✓ Services stopped"
echo ""
echo "To restart: ./start.sh"
