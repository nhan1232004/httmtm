# ShopVN - Intelligent E-Commerce Platform

**AI-Driven E-Commerce System with ML Analytics & Personalization**

## Overview

ShopVN is a complete, production-ready e-commerce platform featuring:
- **1M+ transactions** for realistic data
- **5 ML algorithms** for recommendations, segmentation, forecasting, and anomaly detection
- **Dual interfaces**: Admin/Seller Dashboard + Customer Buyer Portal
- **OTP-based authentication** via email
- **Real-time analytics** and business intelligence
- **Fully containerized** with Docker

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Buyer Portal (React)                  │
│  - Browse products & recommendations                    │
│  - Shopping cart & checkout with OTP                    │
│  - Order tracking & reviews                             │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ HTTP/REST API
                   ↓
┌─────────────────────────────────────────────────────────┐
│         FastAPI Backend (Python)                        │
│  - Authentication (JWT + OTP via Email)                 │
│  - Product & Order Management                           │
│  - ML Model Inference (36+ endpoints)                   │
└──────────┬──────────────────────────────┬───────────────┘
           │                              │
           ↓                              ↓
    ┌─────────────┐          ┌──────────────────────┐
    │ SQLite DB   │          │  ML Models (Pickled) │
    │ (1M+ trans) │          │  - KMeans            │
    └─────────────┘          │  - SVD (Collab Filt) │
                             │  - FP-Growth (Basket)│
                             │  - Prophet (Forecast)│
                             │  - IsolationForest   │
                             └──────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                Seller Dashboard (React)                 │
│  - Order management & analytics                         │
│  - Product inventory & CRUD                             │
│  - Customer insights & RFM segmentation                 │
│  - Revenue forecasting & anomaly alerts                 │
└─────────────────────────────────────────────────────────┘
```

## Features

### 7 Requirements Met ✅

| # | Requirement | Implementation | Status |
|---|------------|-----------------|--------|
| 1 | >1M transactions | Augmented UCI data to 1M rows | ✅ Complete |
| 2 | Problem/Topic | AI-driven e-commerce with 5 algorithms | ✅ Complete |
| 3 | Algorithms | KMeans, SVD, FP-Growth, Prophet, IsolationForest | ✅ Complete |
| 4 | Dashboard | Seller React SPA with full analytics | ✅ Complete |
| 5 | Interactivity | Full CRUD for products/orders + OTP verification | ✅ Complete |
| 6 | Customer Interface | Buyer React SPA with recommendations + checkout | ✅ Complete |
| 7 | Data Consistency | Unified SQLite schema + audit logging + OTP | ✅ Complete |

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Set email credentials (optional, for OTP emails)
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"

# Start all services
docker-compose up --build

# Access applications
Backend API:    http://localhost:8000 (API docs at /docs)
Seller Dashboard: http://localhost:3001
Buyer Portal:   http://localhost:3002
```

### Option 2: Local Development

#### Backend Setup
```bash
cd ShopVN_Final_Project/shopvn
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Load data and train models
python -c "from data_processing import load_all; load_all(force=True)"
python train_models.py

# Start API server
uvicorn server:app --reload --port 8000
```

#### Seller Dashboard
```bash
cd web/seller
npm install --legacy-peer-deps
npm run dev  # Opens on http://localhost:5173
```

#### Buyer Portal
```bash
cd web/buyer
npm install --legacy-peer-deps
npm run dev  # Opens on http://localhost:5174
```

## Demo Users

### Seller Account
- **Email:** seller@demo.com
- **Password:** SellerPass123!
- **Role:** Seller

### Buyer Accounts
- **Email:** buyer1@demo.com
- **Password:** BuyerPass123!
- **Role:** Buyer

Or **register new accounts** using OTP verification.

## API Endpoints (36+)

### Authentication
```
POST   /api/auth/register              - Create account (legacy)
POST   /api/auth/login                 - Login with email/password
POST   /api/auth/register/send-otp     - Send OTP to email
POST   /api/auth/register/verify-otp   - Verify OTP + create account
GET    /api/auth/me                    - Get current user profile
```

### Products
```
GET    /api/products                   - List products (with filters)
GET    /api/products/{id}              - Get product details
GET    /api/products/categories        - Get all categories
POST   /api/seller/products            - Create product (seller only)
PUT    /api/seller/products/{id}       - Update product
DELETE /api/seller/products/{id}       - Delete product
```

### Shopping
```
GET    /api/cart                       - View cart (buyer only)
POST   /api/cart/add                   - Add item to cart
PUT    /api/cart/{item_id}             - Update quantity
DELETE /api/cart/{item_id}             - Remove item
POST   /api/orders/checkout            - Place order
```

### Analytics & ML
```
GET    /api/analytics/overview         - Dashboard KPIs
GET    /api/analytics/segments         - Customer RFM segments
GET    /api/analytics/rules            - Market basket analysis
GET    /api/analytics/forecast         - Revenue forecast
GET    /api/analytics/anomalies        - Suspicious transactions
GET    /api/recommend/{customer_id}    - Personalized recommendations
GET    /api/segment/{customer_id}      - Customer RFM segment
GET    /api/basket/suggest             - Basket recommendations
```

Full API docs at: `http://localhost:8000/docs`

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + Vite + React Router |
| **Backend** | FastAPI + SQLAlchemy (SQLite) |
| **Auth** | JWT Bearer + OTP (Email SMTP) |
| **ML/Analytics** | Scikit-learn, Pandas, NumPy, Plotly |
| **Containerization** | Docker + Docker Compose |
| **API Documentation** | OpenAPI/Swagger |

## Data

- **Source:** UCI Online Retail Dataset II (~542K transactions)
- **Augmented:** 1,000,000 realistic transactions
- **Records:** 845,403 cleaned transactions after preprocessing
- **Customers:** 8,440 unique customers
- **Products:** 3,910 unique products
- **Revenue:** GBP 17.5M total
- **Date Range:** Dec 2010 - Dec 2011

## ML Models

1. **K-Means Clustering** - Customer segmentation (5-7 groups)
   - Input: RFM scores (Recency, Frequency, Monetary)
   - Output: Customer segments (VIP, Loyal, Potential, At-Risk, Lost)

2. **Collaborative Filtering (SVD)** - Product recommendations
   - Input: User-item purchase matrix
   - Output: Top 5 recommended products per customer

3. **FP-Growth** - Market basket analysis
   - Input: Product co-purchases
   - Output: Association rules with lift/confidence

4. **Prophet/Exponential Smoothing** - Demand forecasting
   - Input: Monthly historical revenue
   - Output: 3-month revenue forecast with confidence bands

5. **Isolation Forest** - Anomaly detection + Churn prediction
   - Input: Transaction features + RFM scores
   - Output: Anomaly flags + churn probabilities

## File Structure

```
/d/httmtm/
├── data.csv                           # Original 542K transactions
├── ShopVN_Final_Project/
│   └── shopvn/
│       ├── server.py                  # FastAPI backend (36+ endpoints)
│       ├── database.py                # SQLAlchemy models + OTP
│       ├── email_service.py           # SMTP email for OTP
│       ├── data_processing.py         # ETL pipeline
│       ├── train_models.py            # ML model training
│       ├── dashboard/                 # Streamlit dashboards (6 pages)
│       ├── tests/                     # 35+ unit tests
│       └── requirements.txt           # Python dependencies
├── web/
│   ├── seller/                        # Seller Dashboard (React)
│   └── buyer/                         # Buyer Portal (React)
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.seller
├── Dockerfile.buyer
└── README.md
```

## Testing

### API Tests
```bash
cd ShopVN_Final_Project/shopvn
pytest tests/test_api.py -v
```

### Manual E2E Flow
```
1. Register Seller → Create Products
2. Register Buyer → Browse Products
3. Add to Cart → Checkout with OTP
4. View Order in Seller Dashboard
5. Check Recommendations & Analytics
```

## Deployment

### Local Docker
```bash
docker-compose up --build
```

### Production Considerations
- Replace SQLite with PostgreSQL
- Set real SMTP credentials for email
- Use HTTPS/SSL certificates
- Deploy on cloud (AWS, GCP, Azure)
- Enable caching (Redis)
- Add monitoring (Prometheus, Grafana)

## Environment Variables

```bash
SMTP_USER=your-email@gmail.com           # For OTP emails
SMTP_PASSWORD=your-app-password          # Gmail App Password
DATABASE_URL=sqlite:///./data/shop.db   # Database connection
```

## Support & Documentation

- **API Docs:** http://localhost:8000/docs
- **Data Schema:** See database.py
- **ML Models:** See train_models.py
- **Dashboard:** See dashboard/ folder

## Project Timeline

| Week | Phase | Status |
|------|-------|--------|
| Week 1 | Backend + Data + OTP | ✅ Complete |
| Week 2 | Frontend (Seller + Buyer) | ✅ Complete |
| Week 2 | Docker + Documentation | ✅ Complete |

## Contact

For questions or issues, refer to deployment documentation or API docs.

---

**ShopVN Final Project - Intelligent E-Commerce Platform**
Built with Python, React, and Machine Learning
