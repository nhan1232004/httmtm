# ShopVN Setup Guide

## Requirements
- Docker & Docker Compose (recommended)
- OR: Python 3.11+ + Node.js 18+
- 4GB RAM minimum
- GPU optional (for faster ML training)

## Quick Start (5 minutes)

### Step 1: Clone/Prepare
```bash
cd /d/httmtm
ls -la  # Verify project structure
```

### Step 2: Start Services
```bash
docker-compose up --build
# Wait 2-3 minutes for builds and startup
```

### Step 3: Access Applications
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Seller Dashboard:** http://localhost:3001
- **Buyer Portal:** http://localhost:3002

### Step 4: Test Full Workflow

#### Option A: Register New Accounts
```
1. Go to http://localhost:3002 (Buyer)
2. Click "Register"
3. Enter email, password, name
4. Receive OTP in console (or configure SMTP_USER SMTP_PASSWORD)
5. Enter OTP
6. Account created!

7. Go to http://localhost:3001 (Seller Dashboard)
8. Register as seller (same process)
```

#### Option B: Use Demo Accounts
```
Seller:
  Email: seller@demo.com
  Password: SellerPass123!

Buyer 1:
  Email: buyer1@demo.com
  Password: BuyerPass123!
```

## Complete E2E Flow

### Seller Workflow
```
1. Login as seller → http://localhost:3001
2. Navigate to "Products"
3. Click "Add Product" - Creates new inventory
4. Fill form: Name, Description, Price, Stock, Category
5. Save product
6. Go to "Orders" tab
7. View orders from buyers
8. Update order status (pending → shipped → delivered)
9. Go to "Analytics" tab
10. View customer segments, recommendations, basket analysis
11. Go to "Dashboard" tab
12. See KPIs, revenue trends
```

### Buyer Workflow
```
1. Login as buyer → http://localhost:3002
2. Browse Products
3. Click product → See details + "Recommended for you"
4. "Add to Cart"
5. Click Cart (top right)
6. Review items → "Proceed to Checkout"
7. Enter shipping address
8. Enter payment card details
9. Receive OTP in console
10. Enter OTP to verify transaction
11. Order confirmed!
12. Go to "My Orders"
13. Track order status
14. Leave review
```

## Troubleshooting

### Issue: Containers won't start
```bash
# Check logs
docker-compose logs backend
docker-compose logs seller
docker-compose logs buyer

# Rebuild
docker-compose down
docker-compose up --build
```

### Issue: Port already in use
```bash
# Change ports in docker-compose.yml:
ports:
  - "8001:8000"    # Change 8000 to 8001
  - "3011:80"      # Change 3001 to 3011
  - "3012:80"      # Change 3002 to 3012
```

### Issue: OTP emails not sending
```bash
# Set credentials (if using real email)
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"  # Get from Google Account

# OTP codes print to backend console if SMTP fails
```

### Issue: Database errors
```bash
# Reset database
rm ShopVN_Final_Project/shopvn/data/shop.db
docker-compose restart backend
```

## Local Development (Without Docker)

### Backend
```bash
cd ShopVN_Final_Project/shopvn
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Data & Models
python augment_data.py      # Create 1M transactions
python -c "from data_processing import load_all; load_all(force=True)"
python train_models.py      # Train ML models

# Start server
uvicorn server:app --reload --port 8000
# API at http://localhost:8000
```

### Seller Frontend
```bash
cd web/seller
npm install --legacy-peer-deps
npm run dev
# Dashboard at http://localhost:5173
```

### Buyer Frontend
```bash
cd web/buyer
npm install --legacy-peer-deps
npm run dev
# Portal at http://localhost:5174
```

## Project Data Summary

- **Dataset:** 1,000,000 transactions (augmented from UCI Online Retail)
- **After cleaning:** 845,403 transactions
- **Customers:** 8,440 unique
- **Products:** 3,910 unique
- **Categories:** 6 main categories
- **Date Range:** Dec 2010 - Dec 2011
- **Total Revenue:** GBP 17.5M

## ML Models Status

All 5 models trained and ready:
- ✅ K-Means Clustering (Customer segments)
- ✅ SVD Collaborative Filtering (Product recommendations)
- ✅ FP-Growth (Market basket analysis)
- ✅ Prophet (Revenue forecasting)
- ✅ Isolation Forest (Anomaly detection)

Models are loaded at startup and cached for fast inference.

## Performance

Expected response times:
- API endpoints: 50-200ms
- Recommendations: 100-500ms
- Analytics endpoints: 200-1000ms
- Page loads: 1-3s
- Checkout: 2-5s

## Next Steps for Production

1. **Database:** Switch SQLite → PostgreSQL
2. **Auth:** Add OAuth2, 2FA
3. **Email:** Configure production SMTP
4. **Payments:** Integrate Stripe/PayPal
5. **Monitoring:** Add Prometheus + Grafana
6. **Logging:** Centralized logging (ELK Stack)
7. **CDN:** Add CloudFront/CloudFlare
8. **Caching:** Add Redis cache
9. **Load Balancing:** AWS ELB / Nginx
10. **Security:** WAF, rate limiting, DDoS protection

---

**ShopVN v2.0 - Complete Deployment Guide**
Ready for production with Docker containers!
