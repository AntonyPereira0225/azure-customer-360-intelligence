"""Generate synthetic reference and CRM source data for the Azure Customer 360 project."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from config import (
    COUNTRIES,
    COUNTS,
    CRM_DIR,
    CUSTOMER_SEGMENTS,
    DATE_END,
    DEFECT_RATES,
    MARKETING_CHANNELS,
    PRODUCT_CATEGORIES,
    REFERENCE_DIR,
    SEED,
)


def _ensure_dirs() -> None:
    CRM_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)


def _random_dates(
    rng: np.random.Generator,
    n: int,
    start: str,
    end: str,
) -> pd.DatetimeIndex:
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    days = (end_ts - start_ts).days
    offsets = rng.integers(0, days + 1, size=n)
    return pd.DatetimeIndex(start_ts + pd.to_timedelta(offsets, unit="D"))


def build_countries() -> pd.DataFrame:
    df = pd.DataFrame(
        COUNTRIES,
        columns=[
            "country_code",
            "country_name",
            "region",
            "currency",
            "local_currency_per_eur",
            "customer_weight",
        ],
    )
    df["customer_weight"] = df["customer_weight"] / df["customer_weight"].sum()
    return df


def build_customers(rng: np.random.Generator, countries: pd.DataFrame) -> pd.DataFrame:
    n = COUNTS["customers"]
    country_p = countries["customer_weight"].to_numpy()
    segment_names = np.array(list(CUSTOMER_SEGMENTS))
    segment_p = np.array(list(CUSTOMER_SEGMENTS.values()), dtype=float)
    segment_p = segment_p / segment_p.sum()

    signup_dates = _random_dates(rng, n, "2019-01-01", DATE_END)
    customer_ids = np.array([f"C{i:08d}" for i in range(1, n + 1)], dtype=object)
    home_country = rng.choice(countries["country_code"].to_numpy(), size=n, p=country_p)
    segment = rng.choice(segment_names, size=n, p=segment_p)
    preferred_channel = np.where(
        segment == "Digital First",
        rng.choice(["app", "web"], size=n, p=[0.62, 0.38]),
        rng.choice(["store", "web", "app"], size=n, p=[0.42, 0.38, 0.20]),
    )

    df = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "synthetic_email": [f"customer{i:08d}@example.test" for i in range(1, n + 1)],
            "customer_segment": segment,
            "signup_date": signup_dates,
            "home_country": home_country,
            "preferred_channel": preferred_channel,
            "marketing_consent": rng.random(n) < 0.72,
            "service_tier": np.where(
                segment == "Premium",
                "priority",
                rng.choice(["standard", "enhanced"], size=n, p=[0.82, 0.18]),
            ),
            "source_system": "crm",
            "source_updated_at": _random_dates(rng, n, "2026-01-01", DATE_END),
        }
    )

    # Deliberate raw CRM defects for later Bronze-to-Silver cleansing.
    missing_country_n = max(1, int(n * DEFECT_RATES["customer_missing_country"]))
    invalid_email_n = max(1, int(n * DEFECT_RATES["customer_invalid_email"]))
    duplicate_n = max(1, int(n * DEFECT_RATES["customer_duplicate"]))

    missing_idx = rng.choice(df.index, size=missing_country_n, replace=False)
    df.loc[missing_idx, "home_country"] = None

    invalid_idx = rng.choice(df.index, size=invalid_email_n, replace=False)
    df.loc[invalid_idx, "synthetic_email"] = "invalid-email-format"

    duplicates = df.loc[rng.choice(df.index, size=duplicate_n, replace=False)].copy()
    duplicates["source_updated_at"] = pd.Timestamp(DATE_END)
    df = pd.concat([df, duplicates], ignore_index=True)
    return df


def build_products(rng: np.random.Generator) -> pd.DataFrame:
    n = COUNTS["products"]
    categories = rng.choice(PRODUCT_CATEGORIES, size=n)
    median_price = {
        "Electronics": 240,
        "Home & Living": 90,
        "Fashion": 65,
        "Beauty": 35,
        "Sports & Outdoors": 80,
        "Books & Media": 22,
        "Grocery": 18,
        "Health & Wellness": 42,
        "Travel Accessories": 55,
        "Office & Technology": 120,
    }
    base = pd.Series(categories).map(median_price).to_numpy(dtype=float)
    unit_price = np.maximum(2.0, rng.lognormal(np.log(base), 0.45)).round(2)
    unit_cost = (unit_price * rng.uniform(0.42, 0.72, size=n)).round(2)

    df = pd.DataFrame(
        {
            "product_id": [f"P{i:06d}" for i in range(1, n + 1)],
            "product_name": [f"Synthetic Product {i:06d}" for i in range(1, n + 1)],
            "category": categories,
            "brand_tier": rng.choice(["value", "core", "premium"], size=n, p=[0.25, 0.60, 0.15]),
            "unit_price_eur": unit_price,
            "unit_cost_eur": unit_cost,
            "active_flag": rng.random(n) < 0.96,
            "source_system": "product_master",
        }
    )

    missing_n = max(1, int(n * DEFECT_RATES["product_missing_category"]))
    negative_n = max(1, int(n * DEFECT_RATES["product_negative_price"]))
    df.loc[rng.choice(df.index, size=missing_n, replace=False), "category"] = None
    negative_idx = rng.choice(df.index, size=negative_n, replace=False)
    df.loc[negative_idx, "unit_price_eur"] *= -1
    return df


def build_campaigns(rng: np.random.Generator) -> pd.DataFrame:
    n = COUNTS["campaigns"]
    start_dates = _random_dates(rng, n, "2024-09-01", "2026-06-30")
    duration_days = rng.integers(7, 61, size=n)
    end_dates = start_dates + pd.to_timedelta(duration_days, unit="D")
    end_dates = pd.DatetimeIndex(np.minimum(end_dates.values, np.datetime64(DATE_END)))

    return pd.DataFrame(
        {
            "campaign_id": [f"CMP{i:05d}" for i in range(1, n + 1)],
            "campaign_name": [f"Synthetic Campaign {i:03d}" for i in range(1, n + 1)],
            "marketing_channel": rng.choice(MARKETING_CHANNELS, size=n),
            "objective": rng.choice(
                ["acquisition", "retention", "reactivation", "cross_sell"],
                size=n,
                p=[0.34, 0.30, 0.16, 0.20],
            ),
            "start_date": start_dates,
            "end_date": end_dates,
            "budget_eur": rng.lognormal(np.log(45_000), 0.75, size=n).round(2),
            "source_system": "marketing_platform",
        }
    )


def main() -> None:
    _ensure_dirs()
    rng = np.random.default_rng(SEED)

    countries = build_countries()
    customers = build_customers(rng, countries)
    products = build_products(rng)
    campaigns = build_campaigns(rng)

    countries.to_csv(REFERENCE_DIR / "countries.csv", index=False)
    products.to_csv(REFERENCE_DIR / "products.csv", index=False)
    campaigns.to_csv(REFERENCE_DIR / "campaigns.csv", index=False)
    customers.to_csv(CRM_DIR / "customers.csv", index=False)

    manifest = {
        "countries_rows": len(countries),
        "customers_rows_raw": len(customers),
        "products_rows": len(products),
        "campaigns_rows": len(campaigns),
    }
    (REFERENCE_DIR / "reference_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print("Reference and CRM source data generated.")
    for key, value in manifest.items():
        print(f"  {key}: {value:,}")


if __name__ == "__main__":
    main()
