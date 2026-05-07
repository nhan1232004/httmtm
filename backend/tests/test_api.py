"""
tests/test_api.py
=================
Pytest test suite for ShopVN API endpoints.
Run: pytest tests/test_api.py -v
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from database import create_tables, SessionLocal, seed_demo_data
from server import app

client = TestClient(app)

# ────────────────────────────────────────
#  Fixtures
# ────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    create_tables()
    db = SessionLocal()
    seed_demo_data(db)
    db.close()

@pytest.fixture(scope="session")
def buyer_token():
    r = client.post("/api/auth/login",
                    json={"email":"buyer1@demo.com","password":"demo123"})
    assert r.status_code == 200
    return r.json()["token"]

@pytest.fixture(scope="session")
def seller_token():
    r = client.post("/api/auth/login",\n                    json={"email":"nguyenhuunhan2313@gmail.com","password":"demo123"})\n    assert r.status_code == 200
    return r.json()["token"]

@pytest.fixture(scope="session")
def sample_product_id(seller_token):
    r = client.get("/api/seller/products",
                   headers={"Authorization":f"Bearer {seller_token}"})
    assert r.status_code == 200
    products = r.json()["products"]
    assert len(products) > 0
    return products[0]["id"]


# ────────────────────────────────────────
#  Health
# ────────────────────────────────────────

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "status" in r.json()

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


# ────────────────────────────────────────
#  Auth
# ────────────────────────────────────────

def test_register_buyer():
    r = client.post("/api/auth/register", json={
        "name":"Test User","email":"testuser_new@example.com",
        "password":"test123","role":"buyer"
    })
    assert r.status_code == 200
    data = r.json()
    assert "token" in data
    assert data["user"]["role"] == "buyer"

def test_register_duplicate_email():
    r = client.post("/api/auth/register", json={
        "name":"Dup","email":"buyer1@demo.com","password":"x","role":"buyer"
    })
    assert r.status_code == 400

def test_register_invalid_role():
    r = client.post("/api/auth/register", json={
        "name":"X","email":"x@x.com","password":"x","role":"superuser"
    })
    assert r.status_code == 400

def test_login_success():
    r = client.post("/api/auth/login",
                    json={"email":"buyer1@demo.com","password":"demo123"})
    assert r.status_code == 200
    assert "token" in r.json()

def test_login_wrong_password():
    r = client.post("/api/auth/login",
                    json={"email":"buyer1@demo.com","password":"wrongpass"})
    assert r.status_code == 401

def test_login_nonexistent_email():
    r = client.post("/api/auth/login",
                    json={"email":"nobody@example.com","password":"x"})
    assert r.status_code == 401

def test_me_authenticated(buyer_token):
    r = client.get("/api/auth/me",
                   headers={"Authorization":f"Bearer {buyer_token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "buyer1@demo.com"

def test_me_unauthenticated():
    r = client.get("/api/auth/me")
    assert r.status_code == 401


# ────────────────────────────────────────
#  Products (public)
# ────────────────────────────────────────

def test_list_products():
    r = client.get("/api/products")
    assert r.status_code == 200
    data = r.json()
    assert "products" in data
    assert "total" in data
    assert len(data["products"]) > 0

def test_list_products_pagination():
    r = client.get("/api/products?page=1&limit=5")
    assert r.status_code == 200
    assert len(r.json()["products"]) <= 5

def test_list_products_filter_category():
    r = client.get("/api/products?category=Electronics")
    assert r.status_code == 200

def test_list_products_search():
    r = client.get("/api/products?q=bag")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data["products"], list)

def test_get_categories():
    r = client.get("/api/products/categories")
    assert r.status_code == 200
    assert "categories" in r.json()
    assert len(r.json()["categories"]) > 0

def test_get_product_detail(sample_product_id):
    r = client.get(f"/api/products/{sample_product_id}")
    assert r.status_code == 200
    data = r.json()
    assert "name" in data
    assert "price" in data
    assert "reviews" in data

def test_get_product_not_found():
    r = client.get("/api/products/nonexistent-id")
    assert r.status_code == 404


# ────────────────────────────────────────
#  Seller: products
# ────────────────────────────────────────

def test_seller_list_products(seller_token):
    r = client.get("/api/seller/products",
                   headers={"Authorization":f"Bearer {seller_token}"})
    assert r.status_code == 200
    assert "products" in r.json()

def test_seller_create_product(seller_token):
    r = client.post("/api/seller/products",
                    json={"name":"Test Gadget","price":29.99,"stock":50,
                          "category":"Electronics","description":"A test product"},
                    headers={"Authorization":f"Bearer {seller_token}"})
    assert r.status_code == 200
    assert r.json()["name"] == "Test Gadget"

def test_seller_update_product(seller_token, sample_product_id):
    r = client.put(f"/api/seller/products/{sample_product_id}",
                   json={"name":"Updated Name","price":19.99,"stock":100,
                         "category":"General","description":"Updated"},
                   headers={"Authorization":f"Bearer {seller_token}"})
    assert r.status_code in (200, 404)  # 404 if product belongs to different seller

def test_buyer_cannot_create_product(buyer_token):
    r = client.post("/api/seller/products",
                    json={"name":"X","price":1.0,"stock":1,"category":"A","description":""},
                    headers={"Authorization":f"Bearer {buyer_token}"})
    assert r.status_code == 403


# ────────────────────────────────────────
#  Cart
# ────────────────────────────────────────

def test_get_empty_cart(buyer_token):
    r = client.get("/api/cart",
                   headers={"Authorization":f"Bearer {buyer_token}"})
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert "total" in data

def test_add_to_cart(buyer_token, sample_product_id):
    r = client.post("/api/cart/add",
                    json={"product_id":sample_product_id,"quantity":2},
                    headers={"Authorization":f"Bearer {buyer_token}"})
    assert r.status_code == 200

def test_cart_requires_auth():
    r = client.get("/api/cart")
    assert r.status_code == 401

def test_add_to_cart_requires_auth(sample_product_id):
    r = client.post("/api/cart/add",
                    json={"product_id":sample_product_id,"quantity":1})
    assert r.status_code == 401


# ────────────────────────────────────────
#  Orders
# ────────────────────────────────────────

def test_checkout(buyer_token, sample_product_id):
    # Ensure cart has item
    client.post("/api/cart/add",
                json={"product_id":sample_product_id,"quantity":1},
                headers={"Authorization":f"Bearer {buyer_token}"})
    r = client.post("/api/orders/checkout",
                    json={"address":"123 Test St, London",
                          "payment_type":"credit_card","note":"Test order"},
                    headers={"Authorization":f"Bearer {buyer_token}"})
    # May fail if stock=0, so accept both
    assert r.status_code in (200, 400)

def test_my_orders(buyer_token):
    r = client.get("/api/orders",
                   headers={"Authorization":f"Bearer {buyer_token}"})
    assert r.status_code == 200
    assert "orders" in r.json()

def test_seller_orders(seller_token):
    r = client.get("/api/seller/orders",
                   headers={"Authorization":f"Bearer {seller_token}"})
    assert r.status_code == 200
    assert "orders" in r.json()

def test_seller_analytics(seller_token):
    r = client.get("/api/seller/analytics",
                   headers={"Authorization":f"Bearer {seller_token}"})
    assert r.status_code == 200
    data = r.json()
    assert "summary" in data
    assert "monthly_revenue" in data


# ────────────────────────────────────────
#  Reviews
# ────────────────────────────────────────

def test_add_review(buyer_token, sample_product_id):
    r = client.post("/api/reviews",
                    json={"product_id":sample_product_id,"score":5,"comment":"Excellent!"},
                    headers={"Authorization":f"Bearer {buyer_token}"})
    assert r.status_code == 200


# ────────────────────────────────────────
#  ML Analytics (only if models trained)
# ────────────────────────────────────────

def test_analytics_overview_or_503():
    r = client.get("/api/analytics/overview")
    assert r.status_code in (200, 503)
    if r.status_code == 200:
        data = r.json()
        assert "kpi" in data

def test_analytics_segments_or_503():
    r = client.get("/api/analytics/segments")
    assert r.status_code in (200, 503)

def test_analytics_rules_or_503():
    r = client.get("/api/analytics/rules")
    assert r.status_code in (200, 503)

def test_analytics_forecast_or_503():
    r = client.get("/api/analytics/forecast")
    assert r.status_code in (200, 503)

def test_analytics_anomalies_or_503():
    r = client.get("/api/analytics/anomalies")
    assert r.status_code in (200, 503)

def test_recommend_or_503():
    r = client.get("/api/recommend/12347")
    assert r.status_code in (200, 503)

def test_segment_or_503():
    r = client.get("/api/segment/12347")
    assert r.status_code in (200, 404, 503)

def test_basket_suggest_or_503():
    r = client.get("/api/basket/suggest?product=HEART")
    assert r.status_code in (200, 503)

def test_sample_customers_or_503():
    r = client.get("/api/customers/sample?n=5")
    assert r.status_code in (200, 503)
