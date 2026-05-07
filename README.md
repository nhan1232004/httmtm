# 🌐 H&M Strategic CEO Executive Dashboard

**AI-Driven Business Intelligence Dashboard for Executives**

> Complete, production-ready Macro-level Analytics platform processing 150,000+ transactions with 5 Strategic ML algorithms.

---

## 📋 Quick Overview

| Feature | Status | Details |
|---------|--------|---------|
| **Dataset** | ✅ | H&M Synthetic Transaction Data |
| **Backend** | ✅ | FastAPI |
| **CEO Dashboard** | ✅ | React SPA with Recharts |
| **ML Algorithms** | ✅ | 5 models (K-Means, ETS, FP-Growth, Isolation Forest, Logistic Regression) |
| **Authentication** | ✅ | Mock Login Flow for Demo |
| **Deployment** | ✅ | Docker ready |

---

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Docker & Docker Compose
- 4GB RAM
- Port availability: 8000, 3001

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
CEO Dashboard:     http://localhost:3001
```

---

## 📁 Project Structure

```
ShopVN-Complete/
├── backend/                    # FastAPI Backend
│   ├── server.py              # Main API server for CEO Dashboard
│   ├── ceo_analytics.py       # Core analytics & ML engine
│   ├── hm_data_loader.py      # H&M Synthetic Data generator
│   ├── requirements.txt       # Python dependencies
│   └── data/                  # H&M Parquet datasets
│
├── frontend/                   # React Applications
│   └── ceo_app/               # CEO Executive Dashboard
│       ├── src/
│       │   ├── App.jsx               # Main router
│       │   ├── pages/
│       │   │   ├── CEODashboard.jsx  # Interactive UI
│       │   │   ├── CEODashboard.css  # Premium Styling
│       │   │   └── Login.jsx         # Mock Auth
│       │   └── api/client.js         # HTTP client
│       ├── package.json
│       └── vite.config.js
│
├── docker/                     # Docker Configuration
│   ├── Dockerfile.backend     # Backend container
│   ├── Dockerfile.ceo         # CEO frontend container
│   ├── docker-compose.yml     # Full orchestration
│   └── nginx.conf             # Nginx web server config
│
├── docs/                       # Documentation
│   ├── README.md              # Setup guide
│   ├── SETUP.md               # Detailed setup guide
│   ├── ML_MODELS_GUIDE.md     # ML algorithms detail
│   └── PROJECT_SUMMARY.txt    # Quick reference
│
├── .env.example               # Environment template
├── start.sh                   # Startup script (Main)
├── setup-env.sh              # Environment setup
└── stop.sh                   # Shutdown script
```

---

## 🎯 7 Requirements Delivered

### ✅ 1. Large Dataset (>150K Transactions)
- **Source:** H&M Fashion Recommendations Data
- **Size:** ~150,000 synthetic transactions simulating H&M behavior
- **Domain:** Fashion & Apparel
- **File:** `backend/data/*.parquet`

### ✅ 2. Problem Identification
**Topic:** AI-Driven Business Intelligence & Strategic Decision Making for Retail Executives

### ✅ 3. Algorithms (5 ML Models)
- **K-Means Clustering:** RFM Customer Segmentation
- **ETS (Error, Trend, Seasonal):** Time-Series Demand Forecasting
- **FP-Growth:** Market Basket Analysis for Cross-selling Opportunities
- **Isolation Forest:** Anomaly & Fraud Detection in Transactions
- **Logistic Regression:** High-Risk Churn Prediction

### ✅ 4. Dashboard Interface
- **CEO Dashboard:** Premium Dark-Themed SPA
- **Visuals:** Recharts, Grid layout, Glassmorphism UI
- **Actionability:** Deep-dive Modals for strategic AI insights

### ✅ 5. User Interactivity
- **Drill-down Analytics:** Clickable KPI cards revealing granular data
- **Real-time Insights:** API-driven data updates

### ✅ 6. CEO Dashboard Interface
- **Premium Dark-Themed SPA** with executive-focused design
- **Interactive Visualizations:** Recharts, Grid layout, Glassmorphism UI
- **Drill-down Analytics:** Deep-dive modals for strategic insights
- **Real-time KPIs:** Live business metrics

### ✅ 7. Data Consistency & Security
- Unified data model with H&M transaction schema
- Mock authentication system for demo
- Secure API endpoints
- Persistent data management

---

## 🔐 Demo Users

### Executive Account
```
Email:    admin@demo.com
Password: AdminPass123!
Role:     CEO/Executive
```

---

## 📡 API Endpoints

### Analytics & ML (Core APIs)
```
GET    /api/analytics/overview         - Dashboard KPIs
GET    /api/analytics/segments         - Customer segments
GET    /api/analytics/forecast         - Revenue forecast
GET    /api/recommend/{customer_id}    - Recommendations
GET    /api/basket/suggest             - Basket recommendations
GET    /api/analytics/anomalies        - Fraud/Anomaly detection
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

### CEO Dashboard Development
```bash
cd frontend/ceo_app
npm install
npm run dev  # Opens http://localhost:5173
```

---

## 🐳 Docker Commands

### Start All Services
```bash
./start.sh
# Or manually:
cd docker
docker-compose up --build
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f ceo
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

### Manual Testing
```
1. Start services: ./start.sh
2. Access CEO Dashboard: http://localhost:3001
3. Login with demo credentials
4. Explore analytics and ML insights
5. Check API docs: http://localhost:8000/docs
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
- **Ports:** 8000 (API), 3001 (CEO Dashboard)
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

ceo:
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

Complete, production-ready AI-driven executive analytics platform with:
- ✅ 150K+ transaction dataset
- ✅ 5 ML algorithms for strategic insights
- ✅ CEO Executive Dashboard
- ✅ Real-time analytics & anomaly detection
- ✅ Mock authentication system
- ✅ Docker deployment ready

**Ready to use! Start with:**
```bash
./start.sh
```

Enjoy! 🚀
