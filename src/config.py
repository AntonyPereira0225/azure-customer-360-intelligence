"""Configuration for the synthetic enterprise Customer 360 dataset."""

from __future__ import annotations

import os
from pathlib import Path

SEED = 20260831
DATE_START = "2024-09-01"
DATE_END = "2026-08-31"

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "generated"
REFERENCE_DIR = DATA_DIR / "reference"
CRM_DIR = DATA_DIR / "crm"
COMMERCE_DIR = DATA_DIR / "commerce"
MARKETING_DIR = DATA_DIR / "marketing"
DIGITAL_DIR = DATA_DIR / "digital"
SERVICE_DIR = DATA_DIR / "service"
REPORT_DIR = DATA_DIR / "validation"

SCALE_PROFILE = os.getenv("DATA_SCALE", "sample").strip().lower()

SCALE_PROFILES = {
    "sample": {
        "customers": 25_000,
        "products": 1_000,
        "campaigns": 40,
        "orders": 250_000,
        "order_items": 600_000,
        "payments": 250_000,
        "web_sessions": 500_000,
        "marketing_interactions": 200_000,
        "support_cases": 35_000,
        "returns": 20_000,
    },
    "portfolio": {
        "customers": 250_000,
        "products": 5_000,
        "campaigns": 100,
        "orders": 2_500_000,
        "order_items": 7_000_000,
        "payments": 2_500_000,
        "web_sessions": 5_000_000,
        "marketing_interactions": 2_000_000,
        "support_cases": 350_000,
        "returns": 200_000,
    },
}

if SCALE_PROFILE not in SCALE_PROFILES:
    raise ValueError(
        f"Unsupported DATA_SCALE={SCALE_PROFILE!r}. "
        f"Choose one of: {', '.join(SCALE_PROFILES)}"
    )

COUNTS = SCALE_PROFILES[SCALE_PROFILE]
CHUNK_SIZE = int(os.getenv("DATA_CHUNK_SIZE", "250000"))

COUNTRIES = [
    ("IE", "Ireland", "Northern Europe", "EUR", 1.00, 0.22),
    ("GB", "United Kingdom", "Northern Europe", "GBP", 0.86, 0.18),
    ("DE", "Germany", "Western Europe", "EUR", 1.00, 0.14),
    ("FR", "France", "Western Europe", "EUR", 1.00, 0.11),
    ("NL", "Netherlands", "Western Europe", "EUR", 1.00, 0.07),
    ("ES", "Spain", "Southern Europe", "EUR", 1.00, 0.07),
    ("IT", "Italy", "Southern Europe", "EUR", 1.00, 0.06),
    ("BE", "Belgium", "Western Europe", "EUR", 1.00, 0.04),
    ("PT", "Portugal", "Southern Europe", "EUR", 1.00, 0.03),
    ("SE", "Sweden", "Northern Europe", "SEK", 11.20, 0.03),
    ("DK", "Denmark", "Northern Europe", "DKK", 7.45, 0.025),
    ("PL", "Poland", "Central Europe", "PLN", 4.30, 0.025),
]

CUSTOMER_SEGMENTS = {
    "Core": 0.48,
    "Digital First": 0.20,
    "Premium": 0.12,
    "Value Seeker": 0.14,
    "Frequent Traveller": 0.06,
}

PRODUCT_CATEGORIES = [
    "Electronics",
    "Home & Living",
    "Fashion",
    "Beauty",
    "Sports & Outdoors",
    "Books & Media",
    "Grocery",
    "Health & Wellness",
    "Travel Accessories",
    "Office & Technology",
]

SALES_CHANNELS = ["web", "app", "store", "marketplace"]
PAYMENT_METHODS = ["credit_card", "debit_card", "digital_wallet", "bank_transfer"]
MARKETING_CHANNELS = ["email", "paid_search", "paid_social", "display", "affiliate", "push"]
SUPPORT_CATEGORIES = ["delivery", "payment", "product", "return", "account", "technical"]

# Deliberate raw-source defect rates. These are intentionally small enough to
# preserve business realism while creating meaningful Bronze-to-Silver work.
DEFECT_RATES = {
    "customer_duplicate": 0.0020,
    "customer_missing_country": 0.0015,
    "customer_invalid_email": 0.0010,
    "product_missing_category": 0.0010,
    "product_negative_price": 0.0005,
    "order_orphan_customer": 0.0005,
    "order_missing_timestamp": 0.0004,
    "order_negative_value": 0.0003,
    "order_item_orphan_product": 0.0005,
    "payment_missing_method": 0.0005,
    "session_missing_timestamp": 0.0005,
    "marketing_orphan_campaign": 0.0005,
    "support_negative_resolution": 0.0005,
}
