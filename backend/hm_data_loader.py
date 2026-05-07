"""
hm_data_loader.py
=================
H&M Fashion Dataset Loader for CEO Executive Dashboard

Dataset: https://huggingface.co/datasets/einrafh/hnm-fashion-recommendations-data
Columns (transactions): t_dat, customer_id, article_id, price, sales_channel_id
Columns (articles):     article_id, prod_name, product_type_name, product_group_name,
                        colour_group_name, department_name, detail_desc
Columns (customers):    customer_id, FN, Active, club_member_status, age, postal_code

Modes:
  use_demo=True  → Generates realistic 150K-transaction synthetic H&M dataset
  use_demo=False → Loads real CSV from backend/data/hm/
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "hm")
os.makedirs(DATA_DIR, exist_ok=True)

# ── H&M Real product categories (from actual dataset) ──────────────────────
HM_PRODUCT_TYPES = [
    "Trousers", "Dress", "T-shirt", "Sweater", "Jacket", "Skirt",
    "Shorts", "Top", "Blouse", "Shirt", "Jeans", "Coat", "Cardigan",
    "Leggings", "Vest", "Bra", "Underwear", "Swimwear", "Socks",
    "Shoes", "Boots", "Sneakers", "Sandals", "Accessories", "Bag",
    "Hat", "Scarf", "Belt", "Pyjamas", "Nightwear"
]

HM_PRODUCT_GROUPS = [
    "Garment Upper body", "Garment Lower body", "Garment Full body",
    "Underwear", "Swimwear", "Shoes", "Accessories", "Nightwear"
]

HM_DEPARTMENTS = ["Womens", "Mens", "Divided", "Kids", "H&M Home", "Sport"]

HM_COLOURS = [
    "Black", "White", "Dark Blue", "Light Blue", "Beige", "Grey", "Red",
    "Pink", "Green", "Yellow", "Brown", "Orange", "Purple", "Navy"
]

HM_CLUB_STATUS = ["ACTIVE", "PRE-CREATE", "INACTIVE", "LEFT CLUB"]


class HMDataLoader:
    """Load and prepare H&M data for CEO Dashboard analytics"""

    @staticmethod
    def load_transactions(filepath=None, sample_size=500_000):
        """Load real H&M transaction CSV"""
        if filepath is None:
            filepath = os.path.join(DATA_DIR, "transactions_train.csv")

        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Transactions file not found: {filepath}\n"
                f"Download from: https://huggingface.co/datasets/einrafh/hnm-fashion-recommendations-data\n"
                f"Place at: {filepath}"
            )

        print(f"[LOAD] Loading transactions from {filepath}...")
        if sample_size:
            df = pd.read_csv(filepath, nrows=sample_size)
        else:
            df = pd.read_csv(filepath)

        df['t_dat'] = pd.to_datetime(df['t_dat'])
        df = df.dropna(subset=['customer_id', 'article_id', 'price'])
        df = df[df['price'] > 0]
        print(f"  [OK] Loaded {len(df):,} transactions")
        return df

    @staticmethod
    def load_articles(filepath=None):
        """Load real H&M articles CSV"""
        if filepath is None:
            filepath = os.path.join(DATA_DIR, "articles.csv")

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Articles file not found: {filepath}")

        print(f"[LOAD] Loading articles from {filepath}...")
        df = pd.read_csv(filepath, dtype={'article_id': str})
        df = df.fillna({
            'prod_name': 'Unknown Product',
            'product_type_name': 'Garment Upper body',
            'product_group_name': 'Apparel',
            'colour_group_name': 'Black',
            'department_name': 'Womens',
            'detail_desc': ''
        })
        print(f"  [OK] Loaded {len(df):,} articles")
        return df

    @staticmethod
    def load_customers(filepath=None):
        """Load real H&M customers CSV"""
        if filepath is None:
            filepath = os.path.join(DATA_DIR, "customers.csv")

        if not os.path.exists(filepath):
            print("  [WARN] Customers file not found, will use synthetic demographics")
            return None

        print(f"[LOAD] Loading customers from {filepath}...")
        df = pd.read_csv(filepath)
        print(f"  [OK] Loaded {len(df):,} customers")
        return df

    @staticmethod
    def create_demo_dataset(n_transactions=150_000, random_seed=42):
        """
        Generate realistic synthetic H&M dataset (150K transactions over 2 years)
        Mirrors the real H&M dataset structure and statistics.

        Returns:
            transactions_df, articles_df, customers_df
        """
        np.random.seed(random_seed)
        print(f"\n[INFO] Generating H&M synthetic dataset ({n_transactions:,} transactions)...")

        # ── Time range: Sep 2018 → Sep 2020 (real H&M period) ──
        end_date   = pd.Timestamp("2020-09-22")
        start_date = pd.Timestamp("2018-09-20")
        n_days = (end_date - start_date).days  # 732 days

        # ── Customers ──────────────────────────────────────────
        n_customers = 8_000  # ~5% of transactions
        customer_ids = [f"c{i:06d}" for i in range(n_customers)]

        # Age distribution matching H&M target market
        ages = np.random.choice(
            range(18, 80),
            n_customers,
            p=_age_distribution(range(18, 80))
        )

        club_status_weights = [0.55, 0.25, 0.15, 0.05]
        customers_df = pd.DataFrame({
            'customer_id':       customer_ids,
            'age':               ages,
            'club_member_status': np.random.choice(HM_CLUB_STATUS, n_customers, p=club_status_weights),
            'FN':                np.random.choice([0, 1], n_customers, p=[0.3, 0.7]),
            'Active':            np.random.choice([0, 1], n_customers, p=[0.2, 0.8]),
        })

        # ── Articles ───────────────────────────────────────────
        n_articles = 5_000
        article_ids = [f"{100000 + i:09d}" for i in range(n_articles)]

        # Realistic product type distribution
        prod_type_weights = _product_type_weights()
        product_types = np.random.choice(
            HM_PRODUCT_TYPES, n_articles, p=prod_type_weights
        )

        # Department distribution (H&M is ~60% Womens)
        dept_weights = [0.60, 0.18, 0.10, 0.07, 0.03, 0.02]
        departments = np.random.choice(HM_DEPARTMENTS, n_articles, p=dept_weights)

        # Price per product type (realistic H&M pricing in GBP equivalents)
        base_prices = _base_price_by_type(product_types)

        articles_df = pd.DataFrame({
            'article_id':         article_ids,
            'prod_name':          [f"{d} {t} #{i}" for i, (d, t) in enumerate(zip(departments, product_types))],
            'product_type_name':  product_types,
            'product_group_name': [_type_to_group(t) for t in product_types],
            'colour_group_name':  np.random.choice(HM_COLOURS, n_articles),
            'department_name':    departments,
            'base_price':         base_prices,
        })

        # ── Transactions ───────────────────────────────────────
        # Seasonal buying pattern (H&M peaks: Oct-Dec, Mar-May)
        dates = _generate_seasonal_dates(start_date, end_date, n_transactions)

        # Customer selection with power-law (few heavy buyers)
        cust_probs = np.random.power(0.3, n_customers)
        cust_probs /= cust_probs.sum()
        chosen_customers = np.random.choice(customer_ids, n_transactions, p=cust_probs)

        # Article selection with power-law (few bestsellers)
        art_probs = np.random.power(0.35, n_articles)
        art_probs /= art_probs.sum()
        chosen_articles = np.random.choice(article_ids, n_transactions, p=art_probs)

        # Price = base_price × seasonal_factor × random noise
        article_price_map = articles_df.set_index('article_id')['base_price'].to_dict()
        base_prices_trans = np.array([article_price_map[a] for a in chosen_articles])
        price_noise = np.random.lognormal(0, 0.12, n_transactions)
        prices = (base_prices_trans * price_noise).round(4)

        # Channel: 70% online (1), 30% store (2) — matching real H&M
        channels = np.random.choice([1, 2], n_transactions, p=[0.70, 0.30])

        transactions_df = pd.DataFrame({
            't_dat':            pd.to_datetime(dates),
            'customer_id':      chosen_customers,
            'article_id':       chosen_articles,
            'price':            prices,
            'sales_channel_id': channels,
        }).sort_values('t_dat').reset_index(drop=True)

        print(f"  [OK] Transactions: {len(transactions_df):,} rows")
        print(f"  [OK] Articles:     {len(articles_df):,} products")
        print(f"  [OK] Customers:    {len(customers_df):,} customers")
        print(f"  [OK] Date range:   {transactions_df['t_dat'].min().date()} → {transactions_df['t_dat'].max().date()}")

        return transactions_df, articles_df, customers_df


# ── Helper functions ────────────────────────────────────────────────────────

def _age_distribution(age_range):
    """H&M target: young adults peak 20-35"""
    ages = np.array(list(age_range), dtype=float)
    weights = np.exp(-0.5 * ((ages - 28) / 12) ** 2)  # Peak at 28
    weights /= weights.sum()
    return weights


def _product_type_weights():
    """Realistic H&M product type distribution"""
    n = len(HM_PRODUCT_TYPES)
    # T-shirts, Trousers, Dresses most popular
    weights = np.array([
        3.0, 3.5, 5.0, 2.5, 2.0, 2.5, 1.5, 3.0, 2.0, 2.5,  # Trousers→Jeans
        2.0, 1.5, 2.0, 2.0, 1.5, 2.5, 2.5, 1.0, 2.0,        # Coat→Socks
        1.5, 1.5, 2.0, 1.0, 1.5, 1.0,                        # Shoes→Bag
        0.8, 0.8, 0.5, 1.0, 1.0                               # Hat→Nightwear
    ])
    weights = weights[:n]
    weights /= weights.sum()
    return weights


def _type_to_group(product_type):
    """Map product type to product group"""
    mapping = {
        "Trousers": "Garment Lower body", "Shorts": "Garment Lower body",
        "Skirt": "Garment Lower body", "Jeans": "Garment Lower body",
        "Leggings": "Garment Lower body",
        "T-shirt": "Garment Upper body", "Sweater": "Garment Upper body",
        "Jacket": "Garment Upper body", "Top": "Garment Upper body",
        "Blouse": "Garment Upper body", "Shirt": "Garment Upper body",
        "Coat": "Garment Upper body", "Cardigan": "Garment Upper body",
        "Vest": "Garment Upper body",
        "Dress": "Garment Full body",
        "Bra": "Underwear", "Underwear": "Underwear",
        "Swimwear": "Swimwear",
        "Socks": "Socks & Tights",
        "Shoes": "Shoes", "Boots": "Shoes", "Sneakers": "Shoes", "Sandals": "Shoes",
        "Accessories": "Accessories", "Bag": "Accessories",
        "Hat": "Accessories", "Scarf": "Accessories", "Belt": "Accessories",
        "Pyjamas": "Nightwear", "Nightwear": "Nightwear",
    }
    return mapping.get(product_type, "Garment Upper body")


def _base_price_by_type(product_types):
    """Realistic H&M pricing (in SEK/100 → approx GBP equivalent)"""
    price_map = {
        "T-shirt": 0.025, "Top": 0.025, "Socks": 0.008,
        "Vest": 0.020, "Underwear": 0.015, "Bra": 0.025,
        "Shorts": 0.030, "Leggings": 0.030, "Skirt": 0.035,
        "Trousers": 0.045, "Jeans": 0.050, "Shirt": 0.040,
        "Blouse": 0.040, "Sweater": 0.055, "Cardigan": 0.055,
        "Dress": 0.065, "Jacket": 0.080, "Coat": 0.120,
        "Shoes": 0.070, "Boots": 0.090, "Sneakers": 0.075,
        "Sandals": 0.050, "Swimwear": 0.045, "Pyjamas": 0.040,
        "Nightwear": 0.035, "Accessories": 0.025,
        "Bag": 0.080, "Hat": 0.020, "Scarf": 0.025, "Belt": 0.030,
    }
    return np.array([price_map.get(t, 0.035) for t in product_types])


def _generate_seasonal_dates(start_date, end_date, n_transactions):
    """
    Generate dates with H&M seasonal patterns:
      - Peak: Oct–Dec (holiday season), Mar–May (spring collection)
      - Low:  Jan (post-holiday), Jul–Aug (summer lull)
    """
    days_range = (end_date - start_date).days
    day_indices = np.arange(days_range)

    # Monthly weight function
    month_weights = np.array([0.7, 0.7, 0.9, 1.0, 1.0, 0.8,
                               0.7, 0.7, 0.9, 1.1, 1.3, 1.4])

    # Build daily weights
    daily_weights = np.array([
        month_weights[(start_date + timedelta(days=int(d))).month - 1]
        for d in day_indices
    ], dtype=float)
    daily_weights /= daily_weights.sum()

    chosen_days = np.random.choice(day_indices, n_transactions, p=daily_weights)
    hours = np.random.choice(range(7, 23), n_transactions,
                             p=_hour_distribution())

    dates = [start_date + timedelta(days=int(d), hours=int(h))
             for d, h in zip(chosen_days, hours)]
    return dates


def _hour_distribution():
    """H&M online shopping peaks: lunch (12-14), evening (19-22)"""
    hours = np.arange(7, 23)
    weights = np.array([
        0.5, 0.6, 0.8, 1.0, 1.2, 1.5,   # 7-12
        1.8, 1.5, 1.3, 1.2, 1.0, 1.0,   # 13-18
        1.5, 1.8, 1.6, 1.2               # 19-22
    ], dtype=float)
    weights /= weights.sum()
    return weights


# ── Public API ──────────────────────────────────────────────────────────────

def load_hm_data(use_demo=True, sample_size=500_000):
    """
    Load H&M data and prepare for CEO Dashboard analytics.

    Args:
        use_demo:    True = synthetic 150K rows; False = real CSVs from data/hm/
        sample_size: How many rows to load from real data (ignored in demo mode)

    Returns:
        transactions_df, articles_df, customers_df, analytics_df
    """
    if use_demo:
        trans_df, articles_df, cust_df = HMDataLoader.create_demo_dataset(
            n_transactions=150_000,
            random_seed=42
        )
    else:
        # Real H&M data mode
        trans_df    = HMDataLoader.load_transactions(sample_size=sample_size)
        articles_df = HMDataLoader.load_articles()
        try:
            cust_df = HMDataLoader.load_customers()
        except Exception:
            cust_df = None

    analytics_df = _prepare_analytics_dataset(trans_df, articles_df, cust_df)
    return trans_df, articles_df, cust_df, analytics_df


def _prepare_analytics_dataset(transactions_df, articles_df, customers_df=None):
    """Merge and enrich data for analytics"""
    print("\n[SYNC] Preparing analytics dataset...")

    article_cols = ['article_id', 'prod_name', 'product_type_name',
                    'product_group_name', 'colour_group_name', 'department_name']
    article_cols = [c for c in article_cols if c in articles_df.columns]

    df = transactions_df.merge(articles_df[article_cols], on='article_id', how='left')

    if customers_df is not None:
        cust_cols = ['customer_id']
        for c in ['age', 'club_member_status', 'FN', 'Active']:
            if c in customers_df.columns:
                cust_cols.append(c)
        df = df.merge(customers_df[cust_cols], on='customer_id', how='left')

    # Date features
    df['t_dat']      = pd.to_datetime(df['t_dat'])
    df['year_month'] = df['t_dat'].dt.to_period('M')
    df['weekday']    = df['t_dat'].dt.day_name()
    df['hour']       = df['t_dat'].dt.hour
    df['month']      = df['t_dat'].dt.month
    df['year']       = df['t_dat'].dt.year

    print(f"  [OK] Analytics dataset: {len(df):,} rows, {len(df.columns)} columns")
    return df
