#!/bin/bash
# ShopVN Environment Setup
# Sets up environment variables and credentials

echo "ShopVN Environment Configuration"
echo "================================"
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "✓ .env file already exists"
    cat .env
    exit 0
fi

echo "Creating .env file..."
echo ""

# Get Gmail credentials
read -p "Gmail address (for OTP emails) [optional]: " SMTP_USER
read -sp "Gmail app password [optional]: " SMTP_PASSWORD
echo ""

# Create .env file
cat > .env << EOF
# ShopVN Environment Variables

# SMTP Configuration (Gmail)
SMTP_USER=${SMTP_USER:-your-email@gmail.com}
SMTP_PASSWORD=${SMTP_PASSWORD:-your-app-password}

# Database
DATABASE_URL=sqlite:///./backend/data/shop.db

# API
API_PORT=8000
API_HOST=0.0.0.0

# Frontend
SELLER_PORT=3001
BUYER_PORT=3002

# Security
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256

# Environment
ENV=production
EOF

echo ""
echo "✓ .env file created"
echo ""
echo "Environment variables set!"
