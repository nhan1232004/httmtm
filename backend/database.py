"""
database.py — SQLAlchemy models for ShopVN platform.
Tables: User, Product, CartItem, Order, OrderItem, Review, Token
"""
from __future__ import annotations
import os, uuid, secrets
import bcrypt
from datetime import datetime, timedelta
from sqlalchemy import (
    create_engine, Column, String, Float, Integer, Boolean,
    DateTime, ForeignKey, Text, Enum
)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker, Session
from sqlalchemy.pool import StaticPool

DB_PATH = "data/shop.db"
os.makedirs("data", exist_ok=True)

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email      = Column(String, unique=True, nullable=False)
    name       = Column(String, nullable=False)
    password   = Column(String, nullable=False)
    role       = Column(Enum("buyer", "seller", "admin"), default="buyer")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active  = Column(Boolean, default=True)

    products   = relationship("Product",  back_populates="seller",  cascade="all,delete")
    orders     = relationship("Order",    back_populates="buyer",   cascade="all,delete")
    reviews    = relationship("Review",   back_populates="user",    cascade="all,delete")
    cart_items = relationship("CartItem", back_populates="user",    cascade="all,delete")


class Product(Base):
    __tablename__ = "products"
    id          = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    seller_id   = Column(String, ForeignKey("users.id"), nullable=False)
    name        = Column(String, nullable=False)
    description = Column(Text,   default="")
    price       = Column(Float,  nullable=False)
    stock       = Column(Integer, default=0)
    category    = Column(String,  default="General")
    image_url   = Column(String,  default="")
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    seller      = relationship("User",      back_populates="products")
    reviews     = relationship("Review",    back_populates="product", cascade="all,delete")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items  = relationship("CartItem",  back_populates="product", cascade="all,delete")


class CartItem(Base):
    __tablename__ = "cart_items"
    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id    = Column(String, ForeignKey("users.id"),    nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, default=1)
    added_at   = Column(DateTime, default=datetime.utcnow)

    user    = relationship("User",    back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class Order(Base):
    __tablename__ = "orders"
    id           = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id     = Column(String, ForeignKey("users.id"), nullable=False)
    status       = Column(Enum("pending","confirmed","shipped","delivered","cancelled"), default="pending")
    total_amount = Column(Float,  default=0.0)
    address      = Column(Text,   default="")
    payment_type = Column(String, default="credit_card")
    note         = Column(Text,   default="")
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    buyer = relationship("User",      back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all,delete")


class OrderItem(Base):
    __tablename__ = "order_items"
    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id   = Column(String, ForeignKey("orders.id"),   nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    seller_id  = Column(String, nullable=False)
    quantity   = Column(Integer, default=1)
    price      = Column(Float,   default=0.0)

    order   = relationship("Order",   back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Review(Base):
    __tablename__ = "reviews"
    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id    = Column(String, ForeignKey("users.id"),    nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    score      = Column(Integer, default=5)
    comment    = Column(Text,    default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user    = relationship("User",    back_populates="reviews")
    product = relationship("Product", back_populates="reviews")


class Token(Base):
    __tablename__ = "tokens"
    token      = Column(String, primary_key=True)
    user_id    = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)


class OTP(Base):
    __tablename__ = "otps"
    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email      = Column(String, unique=True, nullable=False, index=True)
    code       = Column(String, nullable=False)  # 6-digit code
    expires_at = Column(DateTime, nullable=False)
    attempts   = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    purpose    = Column(String, default="register")  # register, verify_card, confirm_transaction


# ── Helpers ─────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(pw: str) -> str:
    """Hash password using bcrypt (salt included)."""
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(pw: str, hashed: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(pw.encode('utf-8'), hashed.encode('utf-8'))
    except (ValueError, TypeError):
        return False


def create_token(user_id: str, db: Session, expires_in_days: int = 7) -> str:
    """Create token with expiration (default 7 days)."""
    tok = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    db.add(Token(token=tok, user_id=user_id, expires_at=expires_at))
    db.commit()
    return tok


def get_user_from_token(token: str, db: Session):
    """Get user from token if valid and not expired."""
    t = db.query(Token).filter(Token.token == token).first()
    if not t or t.expires_at < datetime.utcnow():
        return None
    user = db.query(User).filter(User.id == t.user_id).first()
    return user


def send_otp(email: str, purpose: str = "register", db: Session = None) -> str:
    """Generate and store OTP for email (returns 6-digit code)."""
    if db is None:
        db = SessionLocal()

    # Delete any existing OTP for this email
    db.query(OTP).filter(OTP.email == email).delete()

    # Generate 6-digit code
    code = f"{secrets.randbelow(1000000):06d}"
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    otp = OTP(email=email, code=code, expires_at=expires_at, purpose=purpose)
    db.add(otp)
    db.commit()
    return code


def verify_otp(email: str, code: str, db: Session = None) -> bool:
    """Verify OTP code for email."""
    if db is None:
        db = SessionLocal()

    otp = db.query(OTP).filter(OTP.email == email).first()
    if not otp:
        return False

    # Check expiration
    if otp.expires_at < datetime.utcnow():
        db.delete(otp)
        db.commit()
        return False

    # Check attempts (max 3)
    if otp.attempts >= 3:
        db.delete(otp)
        db.commit()
        return False

    # Check code
    if otp.code != code:
        otp.attempts += 1
        db.commit()
        return False

    # Success - delete OTP
    db.delete(otp)
    db.commit()
    return True


def get_user_from_token(token: str, db: Session):
    t = db.query(Token).filter(Token.token == token).first()
    if not t:
        return None
    return db.query(User).filter(User.id == t.user_id).first()


def create_tables():
    Base.metadata.create_all(bind=engine)


def seed_demo_data(db: Session):
    if db.query(User).count() > 0:
        return

    import random
    random.seed(42)

    CATEGORIES = ["Electronics","Home Decor","Kitchen & Dining",
                  "Stationery & Gifts","Bags & Accessories","Fashion","Seasonal"]
    PRODUCTS_BY_CAT = {
        "Electronics":       [("Wireless Earbuds",45.99),("Smart Watch",89.99),
                               ("USB-C Hub",29.99),("Webcam HD",64.99),("Bluetooth Speaker",55.99)],
        "Home Decor":        [("Scented Candle Set",18.99),("Wall Clock",34.99),
                               ("Throw Pillow",22.99),("LED String Lights",16.99),("Picture Frame",12.99)],
        "Kitchen & Dining":  [("Coffee Mug Set",24.99),("Bamboo Cutting Board",19.99),
                               ("Knife Set",49.99),("Spice Rack",27.99),("Salad Bowl",21.99)],
        "Stationery & Gifts":[("Notebook Set",14.99),("Pen Collection",9.99),
                               ("Desk Organiser",32.99),("Gift Wrap Set",8.99),("Journal",16.99)],
        "Bags & Accessories":[("Tote Bag",28.99),("Backpack",59.99),
                               ("Purse",45.99),("Wallet",34.99),("Key Holder",12.99)],
        "Fashion":           [("Scarf",19.99),("Sunglasses",39.99),
                               ("Hat",22.99),("Belt",17.99),("Socks Set",11.99)],
        "Seasonal":          [("Christmas Ornament",8.99),("Advent Calendar",24.99),
                               ("Valentine Chocolates",15.99),("Easter Basket",18.99),("Party Decorations",22.99)],
    }
    IMAGES = {
        "Electronics":       "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        "Home Decor":        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400",
        "Kitchen & Dining":  "https://images.unsplash.com/photo-1556909172-54557c7e4fb7?w=400",
        "Stationery & Gifts":"https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",
        "Bags & Accessories":"https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400",
        "Fashion":           "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
        "Seasonal":          "https://images.unsplash.com/photo-1513519245088-0e12902e35a5?w=400",
    }

    buyers = []
    for name, email in [("Alice Johnson","buyer1@demo.com"),
                        ("Bob Smith","buyer2@demo.com"),
                        ("Carol White","buyer3@demo.com")]:
        u = User(name=name, email=email, password=hash_password("demo123"), role="buyer")
        db.add(u); buyers.append(u)

    sellers = []
    for name, email in [("Nguyen Huu Nhan","nguyenhuunhan2313@gmail.com"),
                        ("HomeStyle Store","seller2@demo.com"),
                        ("GiftWorld","seller3@demo.com")]:
        u = User(name=name, email=email, password=hash_password("demo123"), role="seller")
        db.add(u); sellers.append(u)

    admin = User(name="Admin", email="admin@demo.com",
                 password=hash_password("admin123"), role="admin")
    db.add(admin)
    db.flush()

    all_products = []
    for i, (cat, prods) in enumerate(PRODUCTS_BY_CAT.items()):
        seller = sellers[i % len(sellers)]
        for name, price in prods:
            p = Product(
                seller_id=seller.id, name=name, category=cat,
                price=price, stock=random.randint(10, 200),
                image_url=IMAGES.get(cat, ""),
                description=f"{name} — premium quality, fast delivery.",
            )
            db.add(p); all_products.append(p)

    db.flush()

    for product in random.sample(all_products, min(25, len(all_products))):
        for buyer in random.sample(buyers, random.randint(1, len(buyers))):
            db.add(Review(
                user_id=buyer.id, product_id=product.id,
                score=random.choices([3,4,5], weights=[1,3,6])[0],
                comment=random.choice(["Great product!","Really happy with this.",
                                        "Good value for money.","Excellent quality.",
                                        "Arrived quickly, well packaged."]),
            ))

    db.commit()
    print("✅ Demo data seeded.")


if __name__ == "__main__":
    create_tables()
    db = SessionLocal()
    seed_demo_data(db)
    db.close()
    print(f"Database ready: {DB_PATH}")
