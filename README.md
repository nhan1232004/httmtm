# 🛍️ ShopVN - Intelligent E-Commerce Platform

**AI-Driven E-Commerce System with Machine Learning**

> Complete, production-ready platform with 1M+ transactions, 5 ML algorithms, Seller Dashboard, and Buyer Portal.

---

## 📋 Quick Overview

| Feature | Status | Details |
|---------|--------|---------|
| **Dataset** | ✅ | 1M+ transactions (845K cleaned) |
| **Backend** | ✅ | FastAPI with 36+ endpoints |
| **Seller Dashboard** | ✅ | React SPA (6 pages) |
| **Buyer Portal** | ✅ | React SPA (8 pages) |
| **ML Algorithms** | ✅ | 5 models (recommendations, segmentation, forecasting) |
| **Authentication** | ✅ | JWT + OTP via email |
| **Database** | ✅ | SQLite (8 tables) |
| **Deployment** | ✅ | Docker ready |

---

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Docker & Docker Compose
- 4GB RAM
- Port availability: 8000, 3001, 3002

### Step 1: Clone/Enter Project
```bash
cd ShopVN-Complete
```

### Step 2: Setup Environment (Optional)
```bash
chmod +x setup-env.sh
./setup-env.sh
# Or copy .env.example to .env
```

### Step 3: Start Services
```bash
chmod +x start.sh
./start.sh
```

### Step 4: Access Applications
```
Backend API:       http://localhost:8000
API Swagger Docs:  http://localhost:8000/docs
Seller Dashboard:  http://localhost:3001
Buyer Portal:      http://localhost:3002
```

---

## 📁 Project Structure

```
ShopVN-Complete/
├── backend/                    # FastAPI Backend
│   ├── server.py              # Main API server (36+ endpoints)
│   ├── database.py            # SQLAlchemy models + OTP
│   ├── email_service.py       # SMTP for OTP emails
│   ├── data_processing.py     # ETL pipeline
│   ├── train_models.py        # ML model training
│   ├── augment_data.py        # Data augmentation script
│   ├── requirements.txt       # Python dependencies
│   ├── tests/                 # Unit tests (35+)
│   ├── data/                  # Data files
│   │   ├── data_augmented.csv         # 1M transactions
│   │   ├── data_original.csv          # Original 542K rows
│   │   └── *.parquet                  # Cached data
│   └── models/                # Pickled ML models
│
├── frontend/                   # React Applications
│   ├── seller_app/            # Seller Dashboard
│   │   ├── src/
│   │   │   ├── App.jsx               # Main router
│   │   │   ├── pages/                # 6 dashboard pages
│   │   │   ├── api/client.js         # HTTP client
│   │   │   └── App.css               # Styling
│   │   ├── package.json
│   │   └── vite.config.js
│   │
│   └── buyer_app/             # Buyer Portal
│       ├── src/
│       │   ├── App.jsx               # Main router
│       │   ├── pages/                # 8 portal pages
│       │   ├── store/                # Zustand state
│       │   ├── api/client.js         # HTTP client
│       │   └── App.css               # Styling
│       ├── package.json
│       └── vite.config.js
│
├── docker/                     # Docker Configuration
│   ├── Dockerfile.backend     # Backend container
│   ├── Dockerfile.seller      # Seller frontend container
│   ├── Dockerfile.buyer       # Buyer frontend container
│   ├── docker-compose.yml     # Full orchestration
│   └── nginx.conf             # Nginx web server config
│
├── docs/                       # Documentation
│   ├── README.md              # This file
│   ├── SETUP.md               # Detailed setup guide
│   ├── PROJECT_COMPLETION.md  # Project report
│   └── PROJECT_SUMMARY.txt    # Quick reference
│
├── .env.example               # Environment template
├── start.sh                   # Startup script (Main)
├── setup-env.sh              # Environment setup
└── stop.sh                   # Shutdown script
```

---

## 🎯 7 Requirements Delivered

### ✅ 1. Large Dataset (>1M Transactions)
- **Source:** UCI Online Retail II Dataset
- **Size:** 1,000,000 transactions (augmented)
- **Cleaned:** 845,403 valid transactions
- **File:** `backend/data/data_augmented.csv`
- **Customers:** 8,440 | **Products:** 3,910

### ✅ 2. Problem Identification
**Topic:** AI-Driven E-Commerce Analytics & Personalization

### ✅ 3. Algorithms (5 ML Models)
- K-Means Clustering (Customer segmentation)
- SVD Collaborative Filtering (Recommendations)
- FP-Growth (Market basket analysis)
- Prophet (Demand forecasting)
- Isolation Forest (Anomaly detection)

### ✅ 4. Dashboard Interface
- Seller Dashboard: 6 interactive pages
- Real-time KPIs and analytics
- Order management & product control

### ✅ 5. User Interactivity
- Full CRUD operations for sellers
- OTP-based authentication
- Real-time data updates

### ✅ 6. Customer Interface
- Buyer Portal: 8 complete pages
- Product browsing & recommendations
- Shopping cart & checkout with OTP

### ✅ 7. Data Consistency
- Unified SQLite schema
- OTP verification system
- Bcrypt password hashing
- Token expiration (7 days)

---

## 🔐 Demo Users

### Seller Account
```
Email:    seller@demo.com
Password: SellerPass123!
Role:     Seller
```

### Buyer Accounts
```
Email:    buyer1@demo.com
Password: BuyerPass123!
Role:     Buyer
```

**Or register new accounts** using OTP verification!

---

## 📡 API Endpoints (36+)

### Authentication
```
POST   /api/auth/register              - Register account
POST   /api/auth/login                 - Login
POST   /api/auth/register/send-otp     - Send OTP
POST   /api/auth/register/verify-otp   - Verify OTP & create account
GET    /api/auth/me                    - Get profile
```

### Products
```
GET    /api/products                   - List products (with filters)
GET    /api/products/{id}              - Get product details
POST   /api/seller/products            - Create product
PUT    /api/seller/products/{id}       - Update product
DELETE /api/seller/products/{id}       - Delete product
```

### Shopping & Orders
```
GET    /api/cart                       - View cart
POST   /api/cart/add                   - Add to cart
PUT    /api/cart/{item_id}             - Update quantity
POST   /api/orders/checkout            - Place order
GET    /api/orders                     - View orders
```

### Analytics & ML
```
GET    /api/analytics/overview         - Dashboard KPIs
GET    /api/analytics/segments         - Customer segments
GET    /api/analytics/forecast         - Revenue forecast
GET    /api/recommend/{customer_id}    - Recommendations
GET    /api/basket/suggest             - Basket recommendations
```

**Full API Docs:** http://localhost:8000/docs (when running)

---

## 🛠️ Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
```

### Seller Dashboard Development
```bash
cd frontend/seller_app
npm install
npm run dev  # Opens http://localhost:5173
```

### Buyer Portal Development
```bash
cd frontend/buyer_app
npm install
npm run dev  # Opens http://localhost:5174
```

---

## 🐳 Docker Commands

### Start All Services
```bash
cd docker
docker-compose up --build
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f seller
docker-compose logs -f buyer
```

### Stop Services
```bash
docker-compose down
```

### Rebuild Images
```bash
docker-compose down
docker-compose up --build
```

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest tests/test_api.py -v
```

### Manual E2E Testing
```
1. Register seller account → http://localhost:3001
2. Create products
3. Register buyer account → http://localhost:3002
4. Browse products & add to cart
5. Checkout with OTP verification
6. View order in seller dashboard
```

---

## 📊 Technical Details

### Backend Stack
- **Framework:** FastAPI (Python 3.11)
- **Database:** SQLite + SQLAlchemy
- **Auth:** JWT Bearer + OTP (Email SMTP)
- **Security:** Bcrypt password hashing
- **ML:** Scikit-learn, Pandas, NumPy
- **Testing:** Pytest (35+ tests)

### Frontend Stack
- **Framework:** React 18 + Vite
- **Routing:** React Router v6
- **State:** Zustand (buyer cart)
- **HTTP:** Axios with interceptors
- **Charts:** Recharts
- **Styling:** Inline CSS + Tailwind utilities

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Web Server:** Nginx
- **Ports:** 8000 (API), 3001 (seller), 3002 (buyer)
- **Volumes:** Persistent data in ./backend/data/

---

## 🔧 Troubleshooting

### Issue: Containers won't start
```bash
# Check logs
docker-compose logs backend

# Rebuild
docker-compose down
docker-compose up --build --force-recreate
```

### Issue: Port already in use
Edit `docker/docker-compose.yml` and change ports:
```yaml
backend:
  ports:
    - "8001:8000"  # Change from 8000 to 8001

seller:
  ports:
    - "3011:80"    # Change from 3001 to 3011
```

### Issue: OTP emails not sending
1. Configure Gmail credentials in `.env`
2. Or check backend logs for OTP codes
3. OTP codes print to console for testing

### Issue: Database errors
```bash
rm backend/data/shop.db
docker-compose restart backend
```

---

## 📈 Performance

Expected response times:
- **API Endpoints:** 50-200ms
- **ML Inference:** 100-500ms
- **Page Load:** 1-3s
- **Checkout:** 2-5s

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `docs/README.md` | Full project documentation |
| `docs/SETUP.md` | Step-by-step setup guide |
| `docs/PROJECT_COMPLETION.md` | Detailed project report |
| `docs/PROJECT_SUMMARY.txt` | Quick reference |
| `.env.example` | Environment variables template |

---

## 🚀 Production Deployment

### Before Going Live
1. ✅ Set real Gmail/SMTP credentials
2. ✅ Update security keys in `.env`
3. ✅ Configure domain and SSL
4. ✅ Scale database (SQLite → PostgreSQL)
5. ✅ Add monitoring and logging

### Cloud Deployment Options
- **AWS:** ECS + RDS + CloudFront
- **GCP:** Cloud Run + Cloud SQL
- **Azure:** App Service + SQL Database
- **DigitalOcean:** App Platform
- **Heroku:** Heroku Dynos + PostgreSQL

---

## 📞 Support

For issues or questions:
1. Check `docs/SETUP.md` (Troubleshooting section)
2. Review API docs: http://localhost:8000/docs
3. Check backend logs: `docker-compose logs backend`
4. Read code comments in backend and frontend

---

## 📝 License & Credits

**ShopVN Final Project**
- Built: April 2026
- Dataset: UCI Online Retail II
- Tech: Python, FastAPI, React, Docker

---

## 🎉 Summary

Complete, production-ready e-commerce platform with:
- ✅ 1M+ transaction dataset
- ✅ 5 ML algorithms
- ✅ Admin/seller dashboard
- ✅ Customer portal
- ✅ Full authentication (OTP)
- ✅ Docker deployment ready

**Ready to use! Start with:**
```bash
./start.sh
```

Enjoy! 🚀
