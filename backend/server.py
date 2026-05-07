"""
server.py — ShopVN FastAPI Backend (25+ endpoints)
===================================================
Serves:
  - Auth (register/login)
  - Product CRUD
  - Cart + Checkout
  - Seller order management
  - ML inference (segment, recommend, basket, forecast, anomaly)
  - Buyer SPA  → /buyer
  - Seller SPA → /seller

Run:  uvicorn server:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
from __future__ import annotations
import os, sys, joblib
from typing import Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses  import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import (
    create_tables, seed_demo_data, SessionLocal, get_db,
    User, Product, CartItem, Order, OrderItem, Review, Token,
    hash_password, verify_password, create_token, get_user_from_token,
)

# ────────────────────────────────────────
app = FastAPI(title="ShopVN API", version="2.0.0",
              description="E-Commerce Analytics Platform")

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

if os.path.exists("web/buyer"):
    app.mount("/buyer",  StaticFiles(directory="web/buyer",  html=True), name="buyer")
if os.path.exists("web/seller"):
    app.mount("/seller", StaticFiles(directory="web/seller", html=True), name="seller")

# ─ Load ML models ─
ML: dict = {}

def _load(key, path):
    if os.path.exists(path):
        ML[key] = joblib.load(path)

@app.on_event("startup")
def startup():
    create_tables()
    db = SessionLocal()
    seed_demo_data(db)
    db.close()
    for key, path in [
        ("kmeans",       "models/kmeans.pkl"),
        ("rfm_scaler",   "models/rfm_scaler.pkl"),
        ("label_map",    "models/cluster_label_map.pkl"),
        ("kmeans_meta",  "models/kmeans_meta.pkl"),
        ("svd",          "models/svd_model.pkl"),
        ("customer_history","models/customer_history.pkl"),
        ("product_map",  "models/product_map.pkl"),
        ("svd_meta",     "models/svd_meta.pkl"),
        ("assoc_rules",  "models/assoc_rules.pkl"),
        ("freq_items",   "models/freq_items.pkl"),
        ("fpgrowth_meta","models/fpgrowth_meta.pkl"),
        ("forecast",     "models/forecast.pkl"),
        ("analytics",    "models/analytics_cache.pkl"),
        ("anomaly",      "models/anomaly_detector.pkl"),
        ("churn_model",  "models/churn_model.pkl"),
        ("churn_scaler", "models/churn_scaler.pkl"),
        ("churn_meta",   "models/churn_meta.pkl"),
    ]:
        _load(key, path)

    try:
        import pandas as pd
        if os.path.exists("data/rfm_clustered.parquet"):
            ML["rfm_df"] = pd.read_parquet("data/rfm_clustered.parquet")
        if os.path.exists("data/anomalies.parquet"):
            ML["anomalies_df"] = pd.read_parquet("data/anomalies.parquet")
    except Exception:
        pass
    print(f"✅ Loaded {len(ML)} ML artifacts")


# ────────────────────────────────────────
#  Auth helpers
# ────────────────────────────────────────

def current_user(authorization: str = Header(default=""),
                 db: Session = Depends(get_db)) -> User:
    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(401, "Not authenticated")
    user = get_user_from_token(token, db)
    if not user or not user.is_active:
        raise HTTPException(401, "Invalid token")
    return user

def seller_only(user: User = Depends(current_user)) -> User:
    if user.role not in ("seller","admin"):
        raise HTTPException(403, "Seller/admin only")
    return user

def admin_only(user: User = Depends(current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(403, "Admin only")
    return user


# ────────────────────────────────────────
#  Schemas
# ────────────────────────────────────────

class RegisterIn(BaseModel):
    name: str; email: str; password: str; role: str = "buyer"

class SendOTPIn(BaseModel):
    email: str

class VerifyOTPIn(BaseModel):
    email: str; code: str; name: str; password: str; role: str = "buyer"

class VerifyCardOTPIn(BaseModel):
    otp_code: str

class LoginIn(BaseModel):
    email: str; password: str

class ProductIn(BaseModel):
    name: str; description: str = ""; price: float
    stock: int = 0; category: str = "General"; image_url: str = ""

class CartAddIn(BaseModel):
    product_id: str; quantity: int = 1

class CheckoutIn(BaseModel):
    address: str; payment_type: str = "credit_card"; note: str = ""

class ReviewIn(BaseModel):
    product_id: str; score: int; comment: str = ""

class StatusIn(BaseModel):
    status: str


# ────────────────────────────────────────
#  Serialisers
# ────────────────────────────────────────

def ser_user(u: User) -> dict:
    return {"id":u.id,"name":u.name,"email":u.email,
            "role":u.role,"created_at":str(u.created_at)}

def ser_product(p: Product, db: Session) -> dict:
    reviews = db.query(Review).filter(Review.product_id == p.id).all()
    avg = round(sum(r.score for r in reviews)/len(reviews),2) if reviews else 0
    return {"id":p.id,"name":p.name,"description":p.description,"price":p.price,
            "stock":p.stock,"category":p.category,"image_url":p.image_url,
            "is_active":p.is_active,"seller_id":p.seller_id,
            "seller_name":p.seller.name if p.seller else "",
            "avg_rating":avg,"n_reviews":len(reviews),
            "created_at":str(p.created_at)}

def ser_order(o: Order, db: Session) -> dict:
    items = [{"product_id":oi.product_id,
              "product_name":oi.product.name if oi.product else "?",
              "product_image":oi.product.image_url if oi.product else "",
              "quantity":oi.quantity,"price":oi.price,"seller_id":oi.seller_id}
             for oi in o.items]
    return {"id":o.id,"status":o.status,"total_amount":o.total_amount,
            "address":o.address,"payment_type":o.payment_type,"note":o.note,
            "created_at":str(o.created_at),"updated_at":str(o.updated_at),
            "buyer_name":o.buyer.name if o.buyer else "","items":items}


# ════════════════════════════════════════
#  ROUTES — Health
# ════════════════════════════════════════

@app.get("/", tags=["Health"])
def root():
    return {"status":"ok","docs":"/docs","buyer":"/buyer","seller":"/seller"}

@app.get("/api/health", tags=["Health"])
def health():
    return {"status":"healthy","ml_models":list(ML.keys())}


# ════════════════════════════════════════
#  ROUTES — Auth
# ════════════════════════════════════════

@app.post("/api/auth/register", tags=["Auth"])
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email already in use")
    if body.role not in ("buyer","seller"):
        raise HTTPException(400, "Role must be buyer or seller")
    u = User(name=body.name, email=body.email,
             password=hash_password(body.password), role=body.role)
    db.add(u); db.commit(); db.refresh(u)
    return {"token": create_token(u.id, db), "user": ser_user(u)}

@app.post("/api/auth/login", tags=["Auth"])
def login(body: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == body.email).first()
    if not u or not verify_password(body.password, u.password):
        raise HTTPException(401, "Invalid credentials")
    return {"token": create_token(u.id, db), "user": ser_user(u)}

@app.get("/api/auth/me", tags=["Auth"])
def me(user: User = Depends(current_user)):
    return ser_user(user)


# ════════════════════════════════════════
#  OTP Authentication
# ════════════════════════════════════════

@app.post("/api/auth/register/send-otp", tags=["Auth"])
def send_otp_register(body: SendOTPIn, db: Session = Depends(get_db)):
    """Send OTP to email for registration."""
    from email_service import send_otp_email
    from database import send_otp

    # Check if email already exists
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email already in use")

    # Generate and send OTP
    code = send_otp(body.email, purpose="register", db=db)
    email_sent = send_otp_email(body.email, code, purpose="register")

    return {"email": body.email, "status": "OTP sent", "email_sent": email_sent}


@app.post("/api/auth/register/verify-otp", tags=["Auth"])
def verify_otp_register(body: VerifyOTPIn, db: Session = Depends(get_db)):
    """Verify OTP and create user account."""
    from database import verify_otp, send_otp as send_otp_fn

    # Verify OTP
    is_valid = verify_otp(body.email, body.code, db=db)
    if not is_valid:
        raise HTTPException(400, "Invalid or expired OTP")

    # Check password strength (min 8 chars, uppercase, number)
    if len(body.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    if not any(c.isupper() for c in body.password):
        raise HTTPException(400, "Password must contain uppercase letter")
    if not any(c.isdigit() for c in body.password):
        raise HTTPException(400, "Password must contain number")

    # Create user
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email already registered")

    if body.role not in ("buyer", "seller"):
        raise HTTPException(400, "Role must be buyer or seller")

    u = User(name=body.name, email=body.email,
             password=hash_password(body.password), role=body.role)
    db.add(u)
    db.commit()
    db.refresh(u)

    # Send confirmation email
    from email_service import send_confirmation_email
    send_confirmation_email(body.email, body.name)

    return {"token": create_token(u.id, db), "user": ser_user(u), "status": "Account created"}


@app.post("/api/auth/card-verification/otp", tags=["Auth"])
def send_card_verification_otp(body: SendOTPIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    """Send OTP for payment card verification."""
    from email_service import send_otp_email
    from database import send_otp

    # Send OTP
    code = send_otp(user.email, purpose="verify_card", db=db)
    send_otp_email(user.email, code, purpose="verify_card")

    return {"email": user.email, "status": "OTP sent"}


@app.post("/api/auth/transaction/verify-otp", tags=["Auth"])
def verify_transaction_otp(body: VerifyCardOTPIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    """Verify OTP for transaction confirmation."""
    from database import verify_otp

    # Verify OTP
    is_valid = verify_otp(user.email, body.otp_code, db=db)
    if not is_valid:
        raise HTTPException(400, "Invalid or expired OTP")

    return {"status": "Transaction verified"}




@app.get("/api/products", tags=["Products"])
def list_products(
    q: str = Query(""), category: str = Query(""),
    min_price: float = Query(0), max_price: float = Query(999999),
    sort: str = Query("newest"), page: int = Query(1,ge=1),
    limit: int = Query(20,le=100), db: Session = Depends(get_db),
):
    qr = db.query(Product).filter(Product.is_active == True)
    if q:        qr = qr.filter(Product.name.ilike(f"%{q}%"))
    if category: qr = qr.filter(Product.category == category)
    qr = qr.filter(Product.price >= min_price, Product.price <= max_price)
    qr = qr.order_by(Product.price.asc() if sort=="price_asc"
                     else Product.price.desc() if sort=="price_desc"
                     else Product.created_at.desc())
    total = qr.count()
    items = qr.offset((page-1)*limit).limit(limit).all()
    return {"total":total,"page":page,"limit":limit,
            "products":[ser_product(p,db) for p in items]}

@app.get("/api/products/categories", tags=["Products"])
def categories(db: Session = Depends(get_db)):
    rows = db.query(Product.category).filter(Product.is_active==True).distinct().all()
    return {"categories": sorted(set(r[0] for r in rows if r[0]))}

@app.get("/api/products/{product_id}", tags=["Products"])
def get_product(product_id: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p: raise HTTPException(404, "Product not found")
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    d = ser_product(p, db)
    d["reviews"] = [{"user_name":r.user.name if r.user else "?","score":r.score,
                     "comment":r.comment,"created_at":str(r.created_at)} for r in reviews]
    return d


# ════════════════════════════════════════
#  ROUTES — Products (seller)
# ════════════════════════════════════════

@app.get("/api/seller/products", tags=["Seller"])
def seller_products(user: User = Depends(seller_only), db: Session = Depends(get_db)):
    return {"products":[ser_product(p,db) for p in
                        db.query(Product).filter(Product.seller_id==user.id).all()]}

@app.post("/api/seller/products", tags=["Seller"])
def create_product(body: ProductIn, user: User = Depends(seller_only), db: Session = Depends(get_db)):
    p = Product(seller_id=user.id, **body.dict())
    db.add(p); db.commit(); db.refresh(p)
    return ser_product(p, db)

@app.put("/api/seller/products/{pid}", tags=["Seller"])
def update_product(pid: str, body: ProductIn,
                   user: User = Depends(seller_only), db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id==pid, Product.seller_id==user.id).first()
    if not p: raise HTTPException(404, "Not found")
    for k, v in body.dict().items(): setattr(p, k, v)
    p.updated_at = datetime.utcnow()
    db.commit(); db.refresh(p)
    return ser_product(p, db)

@app.delete("/api/seller/products/{pid}", tags=["Seller"])
def delete_product(pid: str, user: User = Depends(seller_only), db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id==pid, Product.seller_id==user.id).first()
    if not p: raise HTTPException(404, "Not found")
    p.is_active = False; db.commit()
    return {"message":"Deleted"}


# ════════════════════════════════════════
#  ROUTES — Cart
# ════════════════════════════════════════

@app.get("/api/cart", tags=["Cart"])
def get_cart(user: User = Depends(current_user), db: Session = Depends(get_db)):
    items = db.query(CartItem).filter(CartItem.user_id==user.id).all()
    result, total = [], 0.0
    for ci in items:
        if ci.product and ci.product.is_active:
            sub = ci.product.price * ci.quantity
            total += sub
            result.append({"cart_item_id":ci.id,"product_id":ci.product_id,
                           "name":ci.product.name,"price":ci.product.price,
                           "image_url":ci.product.image_url,"quantity":ci.quantity,
                           "subtotal":round(sub,2),"stock":ci.product.stock})
    return {"items":result,"total":round(total,2),"count":len(result)}

@app.post("/api/cart/add", tags=["Cart"])
def add_to_cart(body: CartAddIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id==body.product_id, Product.is_active==True).first()
    if not p: raise HTTPException(404, "Product not found")
    if p.stock < body.quantity: raise HTTPException(400, f"Only {p.stock} in stock")
    existing = db.query(CartItem).filter(CartItem.user_id==user.id,
                                         CartItem.product_id==body.product_id).first()
    if existing:
        existing.quantity = min(existing.quantity + body.quantity, p.stock)
    else:
        db.add(CartItem(user_id=user.id, product_id=body.product_id, quantity=body.quantity))
    db.commit()
    return {"message":"Added to cart"}

@app.delete("/api/cart/{item_id}", tags=["Cart"])
def remove_from_cart(item_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    ci = db.query(CartItem).filter(CartItem.id==item_id, CartItem.user_id==user.id).first()
    if not ci: raise HTTPException(404, "Not found")
    db.delete(ci); db.commit()
    return {"message":"Removed"}

@app.put("/api/cart/{item_id}", tags=["Cart"])
def update_cart(item_id: str, quantity: int = Query(...,ge=1),
                user: User = Depends(current_user), db: Session = Depends(get_db)):
    ci = db.query(CartItem).filter(CartItem.id==item_id, CartItem.user_id==user.id).first()
    if not ci: raise HTTPException(404, "Not found")
    ci.quantity = quantity; db.commit()
    return {"message":"Updated"}


# ════════════════════════════════════════
#  ROUTES — Orders
# ════════════════════════════════════════

@app.post("/api/orders/checkout", tags=["Orders"])
def checkout(body: CheckoutIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    cart = db.query(CartItem).filter(CartItem.user_id==user.id).all()
    if not cart: raise HTTPException(400, "Cart is empty")
    total, order_items_data = 0.0, []
    for ci in cart:
        if not ci.product or not ci.product.is_active: continue
        if ci.product.stock < ci.quantity:
            raise HTTPException(400, f"Insufficient stock: {ci.product.name}")
        sub = ci.product.price * ci.quantity
        total += sub
        order_items_data.append((ci, sub))
    o = Order(buyer_id=user.id, total_amount=round(total,2),
              address=body.address, payment_type=body.payment_type, note=body.note)
    db.add(o); db.flush()
    for ci, _ in order_items_data:
        db.add(OrderItem(order_id=o.id, product_id=ci.product_id,
                         seller_id=ci.product.seller_id, quantity=ci.quantity, price=ci.product.price))
        ci.product.stock -= ci.quantity
        db.delete(ci)
    db.commit(); db.refresh(o)
    return ser_order(o, db)

@app.get("/api/orders", tags=["Orders"])
def my_orders(user: User = Depends(current_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.buyer_id==user.id).order_by(Order.created_at.desc()).all()
    return {"orders":[ser_order(o,db) for o in orders]}

@app.get("/api/orders/{order_id}", tags=["Orders"])
def get_order(order_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.id==order_id).first()
    if not o: raise HTTPException(404, "Not found")
    if o.buyer_id != user.id and user.role not in ("seller","admin"):
        raise HTTPException(403, "Forbidden")
    return ser_order(o, db)


# ════════════════════════════════════════
#  ROUTES — Seller orders
# ════════════════════════════════════════

@app.get("/api/seller/orders", tags=["Seller"])
def seller_orders(status: str = Query(""),
                  user: User = Depends(seller_only), db: Session = Depends(get_db)):
    q = db.query(Order).join(OrderItem).filter(OrderItem.seller_id==user.id).distinct()
    if status: q = q.filter(Order.status==status)
    orders = q.order_by(Order.created_at.desc()).all()
    result = []
    for o in orders:
        d = ser_order(o, db)
        d["items"] = [i for i in d["items"] if i["seller_id"]==user.id]
        d["seller_total"] = round(sum(i["price"]*i["quantity"] for i in d["items"]),2)
        result.append(d)
    return {"orders":result}

@app.put("/api/seller/orders/{order_id}/status", tags=["Seller"])
def update_order_status(order_id: str, body: StatusIn,
                        user: User = Depends(seller_only), db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.id==order_id).first()
    if not o: raise HTTPException(404, "Not found")
    valid = ["pending","confirmed","shipped","delivered","cancelled"]
    if body.status not in valid: raise HTTPException(400, f"Status must be one of {valid}")
    o.status = body.status; o.updated_at = datetime.utcnow()
    db.commit()
    return {"message":f"Updated → {body.status}"}


# ════════════════════════════════════════
#  ROUTES — Seller analytics
# ════════════════════════════════════════

@app.get("/api/seller/analytics", tags=["Seller"])
def seller_analytics(user: User = Depends(seller_only), db: Session = Depends(get_db)):
    from collections import defaultdict
    items    = db.query(OrderItem).filter(OrderItem.seller_id==user.id).all()
    products = db.query(Product).filter(Product.seller_id==user.id).all()
    reviews  = [r for p in products for r in p.reviews]

    total_rev = sum(i.price * i.quantity for i in items)
    monthly   = defaultdict(float)
    for i in items:
        o = db.query(Order).filter(Order.id==i.order_id).first()
        if o: monthly[o.created_at.strftime("%Y-%m")] += i.price * i.quantity

    prod_rev = defaultdict(float)
    prod_qty = defaultdict(int)
    for i in items:
        prod_rev[i.product_id] += i.price * i.quantity
        prod_qty[i.product_id] += i.quantity
    top_prods = sorted(prod_rev.items(), key=lambda x: x[1], reverse=True)[:5]
    top_prods_data = []
    for pid, rev in top_prods:
        p = db.query(Product).filter(Product.id==pid).first()
        top_prods_data.append({"product_id":pid,"name":p.name if p else "?",
                                "revenue":round(rev,2),"quantity":prod_qty[pid]})

    statuses = defaultdict(int)
    for i in items:
        o = db.query(Order).filter(Order.id==i.order_id).first()
        if o: statuses[o.status] += 1

    return {
        "summary":{
            "total_revenue":round(total_rev,2),
            "total_orders":len(set(i.order_id for i in items)),
            "total_products":len(products),
            "active_products":sum(1 for p in products if p.is_active),
            "avg_rating":round(sum(r.score for r in reviews)/len(reviews),2) if reviews else 0,
            "total_reviews":len(reviews),
        },
        "top_products":top_prods_data,
        "monthly_revenue":[{"month":k,"revenue":round(v,2)} for k,v in sorted(monthly.items())],
        "order_status_dist":dict(statuses),
    }


# ════════════════════════════════════════
#  ROUTES — Reviews
# ════════════════════════════════════════

@app.post("/api/reviews", tags=["Reviews"])
def add_review(body: ReviewIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if user.role != "buyer": raise HTTPException(403, "Buyers only")
    existing = db.query(Review).filter(Review.user_id==user.id,
                                        Review.product_id==body.product_id).first()
    if existing:
        existing.score = body.score; existing.comment = body.comment
        db.commit(); return {"message":"Review updated"}
    db.add(Review(user_id=user.id, product_id=body.product_id,
                  score=body.score, comment=body.comment))
    db.commit()
    return {"message":"Review added"}


# ════════════════════════════════════════
#  ROUTES — ML Analytics (public)
# ════════════════════════════════════════

@app.get("/api/analytics/overview", tags=["Analytics"])
def analytics_overview():
    if "analytics" not in ML: raise HTTPException(503, "Analytics not loaded. Run train_models.py")
    a = ML["analytics"]
    return {"kpi":a["kpi"],"monthly_revenue":a["monthly_revenue"],
            "top_products":a["top_products"][:10],"category_revenue":a["category_revenue"]}

@app.get("/api/analytics/geography", tags=["Analytics"])
def analytics_geography():
    if "analytics" not in ML: raise HTTPException(503, "Run train_models.py first")
    return {"data": ML["analytics"]["country_revenue"]}

@app.get("/api/analytics/heatmap", tags=["Analytics"])
def analytics_heatmap():
    if "analytics" not in ML: raise HTTPException(503, "Run train_models.py first")
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    data = [{"dow":r["DayOfWeek"],"hour":r["Hour"],"count":r["count"],
             "day_name":days[int(r["DayOfWeek"])]} for r in ML["analytics"]["heatmap"]]
    return {"data": data}

@app.get("/api/analytics/forecast", tags=["Analytics"])
def analytics_forecast():
    if "forecast" not in ML: raise HTTPException(503, "Run train_models.py first")
    return ML["forecast"]

@app.get("/api/analytics/segments", tags=["Analytics"])
def analytics_segments():
    if "analytics" not in ML: raise HTTPException(503, "Run train_models.py first")
    return {"segments": ML["analytics"]["segment_stats"]}

@app.get("/api/analytics/rules", tags=["Analytics"])
def analytics_rules(min_lift: float = Query(1.0), top_n: int = Query(20)):
    if "assoc_rules" not in ML: raise HTTPException(503, "Run train_models.py first")
    rules = ML["assoc_rules"]
    rules = rules[rules["lift"] >= min_lift]
    return {"rules": rules.head(top_n)[["antecedents_str","consequents_str",
                                         "support","confidence","lift"]].to_dict("records"),
            "total": len(rules)}

@app.get("/api/analytics/anomalies", tags=["Analytics"])
def analytics_anomalies(top_n: int = Query(50)):
    if "anomalies_df" not in ML: raise HTTPException(503, "Run train_models.py first")
    df  = ML["anomalies_df"].head(top_n)
    out = df.copy()
    out["InvoiceDate"] = out["InvoiceDate"].astype(str)
    return {"anomalies": out.to_dict("records"), "total": len(ML["anomalies_df"])}

@app.get("/api/analytics/churn-risk", tags=["Analytics"])
def churn_risk(top_n: int = Query(50)):
    if "rfm_df" not in ML: raise HTTPException(503, "Run train_models.py first")
    df = ML["rfm_df"].copy()
    if "churn_prob" not in df.columns:
        raise HTTPException(503, "Churn model not trained yet")
    df["last_purchase"] = df["last_purchase"].astype(str)
    top = df.sort_values("churn_prob", ascending=False).head(top_n)
    return {"customers": top[["CustomerID","segment","recency","frequency",
                               "monetary","churn_prob"]].round(3).to_dict("records")}


# ════════════════════════════════════════
#  ROUTES — ML Inference
# ════════════════════════════════════════

@app.get("/api/recommend/{customer_id}", tags=["ML Inference"])
def recommend(customer_id: str, top_n: int = Query(8, le=20), db: Session = Depends(get_db)):
    if "svd" not in ML:
        products = db.query(Product).filter(Product.is_active==True)\
                     .order_by(Product.created_at.desc()).limit(top_n).all()
        return {"products":[ser_product(p,db) for p in products],"source":"popular"}

    model_pkg = ML["svd"]
    u2i  = model_pkg["u2i"]
    it2i = model_pkg["it2i"]
    items = model_pkg["items"]
    R_hat = model_pkg["R_hat"]

    hist   = ML["customer_history"].get(customer_id, [])
    bought = set(hist)

    if customer_id in u2i:
        u_idx = u2i[customer_id]
        scores = [(item, float(R_hat[u_idx, it2i[item]]))
                  for item in items if item not in bought and item in it2i]
        scores.sort(key=lambda x: x[1], reverse=True)
    else:
        # Cold-start: return popular items
        prod_map = ML.get("product_map")
        if prod_map is not None:
            pm_sorted = prod_map.sort_values("avg_rating", ascending=False)
            scores = [(row["item"], float(row["avg_rating"]))
                      for _, row in pm_sorted.iterrows() if row["item"] not in bought]
        else:
            scores = [(item, 3.0) for item in items if item not in bought]

    result = []
    prod_map = ML.get("product_map")
    for item_name, score in scores[:top_n]:
        row = prod_map[prod_map["item"] == item_name] if prod_map is not None else None
        result.append({
            "description": item_name,
            "pred_score":  round(score, 3),
            "n_ratings":   int(row["n_ratings"].values[0]) if (row is not None and len(row)) else 0,
            "avg_rating":  round(float(row["avg_rating"].values[0]), 2) if (row is not None and len(row)) else 0,
        })
    return {"items": result, "source": "svd_truncated", "n_bought": len(bought)}

@app.get("/api/segment/{customer_id}", tags=["ML Inference"])
def get_segment(customer_id: str):
    if "rfm_df" not in ML: raise HTTPException(503, "Run train_models.py first")
    df = ML["rfm_df"]
    row = df[df["CustomerID"]==customer_id]
    if len(row) == 0: raise HTTPException(404, f"Customer {customer_id} not found")
    r = row.iloc[0]
    cols = ["CustomerID","segment","recency","frequency","monetary",
            "R_score","F_score","M_score","RFM_total"]
    cols = [c for c in cols if c in r.index]
    return {c: (str(r[c]) if hasattr(r[c],"item") is False else r[c]) for c in cols}

@app.get("/api/basket/suggest", tags=["ML Inference"])
def basket_suggest(product: str = Query(...), top_n: int = Query(5)):
    if "assoc_rules" not in ML: raise HTTPException(503, "Run train_models.py first")
    rules = ML["assoc_rules"]
    mask  = rules["antecedents_str"].str.contains(product, case=False, na=False)
    matched = rules[mask].head(top_n)
    return {"product":product,
            "suggestions":matched[["consequents_str","confidence","lift"]].to_dict("records")}

@app.get("/api/customers/sample", tags=["ML Inference"])
def sample_customers(n: int = Query(20, le=100)):
    if "rfm_df" not in ML: raise HTTPException(503, "Run train_models.py first")
    sample = ML["rfm_df"]["CustomerID"].sample(min(n, len(ML["rfm_df"]))).tolist()
    return {"customers": sample}


# ════════════════════════════════════════
#  SPA catch-alls
# ════════════════════════════════════════

@app.get("/buyer/{full_path:path}")
def buyer_spa(full_path: str):
    path = "web/buyer/index.html"
    return FileResponse(path) if os.path.exists(path) else {"error":"Buyer app not built"}

@app.get("/seller/{full_path:path}")
def seller_spa(full_path: str):
    path = "web/seller/index.html"
    return FileResponse(path) if os.path.exists(path) else {"error":"Seller app not built"}


# ????????????????????????????????????????????????????????????????????????????
#  CEO EXECUTIVE DASHBOARD ENDPOINTS (NEW)
# ????????????????????????????????????????????????????????????????????????????

@app.get("/api/ceo/dashboard", tags=["CEO Dashboard"])
def ceo_dashboard_summary():
    """Get complete CEO Dashboard with 15+ strategic KPIs"""
    try:
        from hm_data_loader import load_hm_data
        from ceo_analytics import compute_ceo_analytics
        
        # Load real data or demo data (demo handles its own size)
        trans_df, articles_df, cust_df, _ = load_hm_data(use_demo=True)
        dashboard_data = compute_ceo_analytics(trans_df, articles_df, cust_df)
        
        return dashboard_data
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(503, f"CEO Dashboard error: {str(e)}")

# ????????????????????????????????????????????????????????????????????????????
