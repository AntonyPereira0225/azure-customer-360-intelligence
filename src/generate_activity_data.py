"""Generate chunked synthetic commerce, digital, marketing and service source data."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from config import (
    CHUNK_SIZE,
    COMMERCE_DIR,
    COUNTS,
    CRM_DIR,
    DATE_END,
    DATE_START,
    DEFECT_RATES,
    DIGITAL_DIR,
    MARKETING_DIR,
    PAYMENT_METHODS,
    REFERENCE_DIR,
    SALES_CHANNELS,
    SEED,
    SERVICE_DIR,
    SUPPORT_CATEGORIES,
)


def _ensure_dirs() -> None:
    for path in [COMMERCE_DIR, DIGITAL_DIR, MARKETING_DIR, SERVICE_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def _clear_parts(directory: Path, prefix: str) -> None:
    for path in directory.glob(f"{prefix}_part_*.parquet"):
        path.unlink()


def _random_timestamps(rng: np.random.Generator, n: int) -> pd.DatetimeIndex:
    start = pd.Timestamp(DATE_START)
    end = pd.Timestamp(DATE_END) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    seconds = int((end - start).total_seconds())
    offsets = rng.integers(0, seconds + 1, size=n)
    return pd.DatetimeIndex(start + pd.to_timedelta(offsets, unit="s"))


def _inject_values(
    rng: np.random.Generator,
    df: pd.DataFrame,
    column: str,
    rate: float,
    value: object,
) -> None:
    n = int(len(df) * rate)
    if n <= 0:
        return
    idx = rng.choice(df.index.to_numpy(), size=n, replace=False)
    df.loc[idx, column] = value


def _load_source_keys() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers = pd.read_csv(CRM_DIR / "customers.csv")
    customers = customers.drop_duplicates("customer_id", keep="last")
    products = pd.read_csv(REFERENCE_DIR / "products.csv")
    campaigns = pd.read_csv(REFERENCE_DIR / "campaigns.csv")
    return customers, products, campaigns


def generate_order_items(
    rng: np.random.Generator,
    products: pd.DataFrame,
) -> np.ndarray:
    """Write order-item parts and return exact per-order line revenue totals."""
    _clear_parts(COMMERCE_DIR, "order_items")
    n_orders = COUNTS["orders"]
    n_items = COUNTS["order_items"]
    if n_items < n_orders:
        raise ValueError("order_items must be >= orders so every order has at least one line")

    product_ids = products["product_id"].to_numpy()
    product_prices = np.abs(products["unit_price_eur"].fillna(10.0).to_numpy(dtype=float))
    order_totals = np.zeros(n_orders, dtype=np.float64)

    written = 0
    part = 1
    while written < n_items:
        n = min(CHUNK_SIZE, n_items - written)
        row_numbers = np.arange(written, written + n)
        base_mask = row_numbers < n_orders
        order_ids = np.empty(n, dtype=np.int64)
        order_ids[base_mask] = row_numbers[base_mask] + 1
        extra_n = int((~base_mask).sum())
        if extra_n:
            order_ids[~base_mask] = rng.integers(1, n_orders + 1, size=extra_n)

        product_idx = rng.integers(0, len(products), size=n)
        quantity = rng.choice([1, 2, 3, 4], size=n, p=[0.68, 0.22, 0.08, 0.02])
        discount = rng.choice([0.0, 0.05, 0.10, 0.15, 0.20], size=n, p=[0.56, 0.12, 0.16, 0.10, 0.06])
        unit_price = product_prices[product_idx]
        line_revenue = np.round(quantity * unit_price * (1 - discount), 2)

        df = pd.DataFrame(
            {
                "order_item_id": np.arange(written + 1, written + n + 1, dtype=np.int64),
                "order_id": [f"O{i:09d}" for i in order_ids],
                "product_id": product_ids[product_idx],
                "quantity": quantity,
                "unit_price_eur": unit_price,
                "discount_pct": discount,
                "line_revenue_eur": line_revenue,
                "source_system": "commerce_db",
            }
        )
        _inject_values(
            rng,
            df,
            "product_id",
            DEFECT_RATES["order_item_orphan_product"],
            "P_ORPHAN",
        )

        np.add.at(order_totals, order_ids - 1, line_revenue)
        df.to_parquet(COMMERCE_DIR / f"order_items_part_{part:03d}.parquet", index=False)
        written += n
        part += 1
        print(f"Order items: {written:,}/{n_items:,}")

    return np.round(order_totals, 2)


def generate_orders_and_payments(
    rng: np.random.Generator,
    customers: pd.DataFrame,
    order_totals: np.ndarray,
) -> None:
    _clear_parts(COMMERCE_DIR, "orders")
    _clear_parts(COMMERCE_DIR, "payments")

    customer_ids = customers["customer_id"].to_numpy()
    customer_countries = customers["home_country"].fillna("IE").to_numpy()
    n_orders = COUNTS["orders"]
    written = 0
    part = 1

    while written < n_orders:
        n = min(CHUNK_SIZE, n_orders - written)
        order_nums = np.arange(written + 1, written + n + 1, dtype=np.int64)
        customer_idx = rng.integers(0, len(customers), size=n)
        timestamps = _random_timestamps(rng, n)
        channel = rng.choice(SALES_CHANNELS, size=n, p=[0.43, 0.27, 0.24, 0.06])
        order_status = rng.choice(
            ["completed", "cancelled", "refunded"], size=n, p=[0.936, 0.040, 0.024]
        )
        values = order_totals[written : written + n].copy()

        orders = pd.DataFrame(
            {
                "order_id": [f"O{i:09d}" for i in order_nums],
                "customer_id": customer_ids[customer_idx],
                "order_timestamp": timestamps,
                "sales_channel": channel,
                "order_country": customer_countries[customer_idx],
                "order_status": order_status,
                "order_value_eur": values,
                "source_system": "commerce_db",
            }
        )
        _inject_values(
            rng, orders, "customer_id", DEFECT_RATES["order_orphan_customer"], "C_ORPHAN"
        )
        _inject_values(
            rng, orders, "order_timestamp", DEFECT_RATES["order_missing_timestamp"], pd.NaT
        )
        negative_n = int(len(orders) * DEFECT_RATES["order_negative_value"])
        if negative_n:
            negative_idx = rng.choice(orders.index.to_numpy(), size=negative_n, replace=False)
            orders.loc[negative_idx, "order_value_eur"] *= -1

        payments = pd.DataFrame(
            {
                "payment_id": [f"PAY{i:09d}" for i in order_nums],
                "order_id": orders["order_id"],
                "payment_timestamp": timestamps + pd.to_timedelta(rng.integers(1, 600, size=n), unit="s"),
                "payment_method": rng.choice(PAYMENT_METHODS, size=n, p=[0.38, 0.31, 0.24, 0.07]),
                "payment_status": np.where(
                    order_status == "cancelled",
                    "voided",
                    np.where(order_status == "refunded", "refunded", "captured"),
                ),
                "payment_amount_eur": values,
                "source_system": "payments_platform",
            }
        )
        _inject_values(
            rng, payments, "payment_method", DEFECT_RATES["payment_missing_method"], None
        )

        orders.to_parquet(COMMERCE_DIR / f"orders_part_{part:03d}.parquet", index=False)
        payments.to_parquet(COMMERCE_DIR / f"payments_part_{part:03d}.parquet", index=False)
        written += n
        part += 1
        print(f"Orders/payments: {written:,}/{n_orders:,}")


def generate_sessions(rng: np.random.Generator, customers: pd.DataFrame) -> None:
    _clear_parts(DIGITAL_DIR, "sessions")
    customer_ids = customers["customer_id"].to_numpy()
    n_total = COUNTS["web_sessions"]
    written = 0
    part = 1
    while written < n_total:
        n = min(CHUNK_SIZE, n_total - written)
        known_customer = rng.random(n) < 0.72
        ids = np.full(n, None, dtype=object)
        ids[known_customer] = rng.choice(customer_ids, size=int(known_customer.sum()))
        starts = _random_timestamps(rng, n)
        duration = np.clip(rng.lognormal(np.log(240), 0.8, size=n), 5, 7200).round().astype(int)
        df = pd.DataFrame(
            {
                "session_id": [f"S{i:010d}" for i in range(written + 1, written + n + 1)],
                "customer_id": ids,
                "session_start": starts,
                "digital_channel": rng.choice(["web", "app"], size=n, p=[0.58, 0.42]),
                "device_type": rng.choice(["mobile", "desktop", "tablet"], size=n, p=[0.62, 0.31, 0.07]),
                "traffic_source": rng.choice(
                    ["direct", "organic", "paid_search", "paid_social", "email", "affiliate"],
                    size=n,
                    p=[0.24, 0.27, 0.18, 0.11, 0.13, 0.07],
                ),
                "duration_seconds": duration,
                "pages_or_screens": np.maximum(1, rng.poisson(5, size=n)),
                "converted_flag": rng.random(n) < 0.045,
                "source_system": "digital_analytics",
            }
        )
        _inject_values(
            rng, df, "session_start", DEFECT_RATES["session_missing_timestamp"], pd.NaT
        )
        df.to_parquet(DIGITAL_DIR / f"sessions_part_{part:03d}.parquet", index=False)
        written += n
        part += 1
        print(f"Sessions: {written:,}/{n_total:,}")


def generate_marketing(
    rng: np.random.Generator,
    customers: pd.DataFrame,
    campaigns: pd.DataFrame,
) -> None:
    _clear_parts(MARKETING_DIR, "interactions")
    customer_ids = customers["customer_id"].to_numpy()
    campaign_ids = campaigns["campaign_id"].to_numpy()
    n_total = COUNTS["marketing_interactions"]
    written = 0
    part = 1
    while written < n_total:
        n = min(CHUNK_SIZE, n_total - written)
        df = pd.DataFrame(
            {
                "interaction_id": [f"MI{i:010d}" for i in range(written + 1, written + n + 1)],
                "customer_id": rng.choice(customer_ids, size=n),
                "campaign_id": rng.choice(campaign_ids, size=n),
                "interaction_timestamp": _random_timestamps(rng, n),
                "event_type": rng.choice(
                    ["impression", "open", "click", "conversion", "unsubscribe"],
                    size=n,
                    p=[0.47, 0.29, 0.17, 0.055, 0.015],
                ),
                "source_system": "marketing_platform",
            }
        )
        _inject_values(
            rng,
            df,
            "campaign_id",
            DEFECT_RATES["marketing_orphan_campaign"],
            "CMP_ORPHAN",
        )
        df.to_parquet(MARKETING_DIR / f"interactions_part_{part:03d}.parquet", index=False)
        written += n
        part += 1
        print(f"Marketing interactions: {written:,}/{n_total:,}")


def generate_support(rng: np.random.Generator, customers: pd.DataFrame) -> None:
    _clear_parts(SERVICE_DIR, "support_cases")
    customer_ids = customers["customer_id"].to_numpy()
    n_total = COUNTS["support_cases"]
    written = 0
    part = 1
    while written < n_total:
        n = min(CHUNK_SIZE, n_total - written)
        opened = _random_timestamps(rng, n)
        resolution = np.clip(rng.lognormal(np.log(720), 1.0, size=n), 5, 20_000).round().astype(int)
        df = pd.DataFrame(
            {
                "case_id": [f"CASE{i:09d}" for i in range(written + 1, written + n + 1)],
                "customer_id": rng.choice(customer_ids, size=n),
                "opened_at": opened,
                "case_category": rng.choice(SUPPORT_CATEGORIES, size=n),
                "priority": rng.choice(["low", "medium", "high", "critical"], size=n, p=[0.36, 0.45, 0.16, 0.03]),
                "resolution_minutes": resolution,
                "case_status": rng.choice(["resolved", "closed", "open"], size=n, p=[0.62, 0.34, 0.04]),
                "satisfaction_score": rng.choice([1, 2, 3, 4, 5], size=n, p=[0.05, 0.08, 0.18, 0.37, 0.32]),
                "source_system": "customer_service",
            }
        )
        negative_n = int(len(df) * DEFECT_RATES["support_negative_resolution"])
        if negative_n:
            idx = rng.choice(df.index.to_numpy(), size=negative_n, replace=False)
            df.loc[idx, "resolution_minutes"] *= -1
        df.to_parquet(SERVICE_DIR / f"support_cases_part_{part:03d}.parquet", index=False)
        written += n
        part += 1
        print(f"Support cases: {written:,}/{n_total:,}")


def generate_returns(rng: np.random.Generator) -> None:
    _clear_parts(COMMERCE_DIR, "returns")
    n_total = COUNTS["returns"]
    n_orders = COUNTS["orders"]
    written = 0
    part = 1
    while written < n_total:
        n = min(CHUNK_SIZE, n_total - written)
        order_nums = rng.choice(np.arange(1, n_orders + 1), size=n, replace=False if n <= n_orders else True)
        df = pd.DataFrame(
            {
                "return_id": [f"R{i:09d}" for i in range(written + 1, written + n + 1)],
                "order_id": [f"O{i:09d}" for i in order_nums],
                "return_timestamp": _random_timestamps(rng, n),
                "return_reason": rng.choice(
                    ["changed_mind", "damaged", "wrong_item", "not_as_described", "late_delivery"],
                    size=n,
                    p=[0.38, 0.19, 0.12, 0.20, 0.11],
                ),
                "refund_status": rng.choice(["processed", "pending", "rejected"], size=n, p=[0.88, 0.09, 0.03]),
                "source_system": "commerce_db",
            }
        )
        df.to_parquet(COMMERCE_DIR / f"returns_part_{part:03d}.parquet", index=False)
        written += n
        part += 1
        print(f"Returns: {written:,}/{n_total:,}")


def main() -> None:
    _ensure_dirs()
    customers, products, campaigns = _load_source_keys()
    rng = np.random.default_rng(SEED + 1)

    order_totals = generate_order_items(rng, products)
    generate_orders_and_payments(rng, customers, order_totals)
    generate_sessions(rng, customers)
    generate_marketing(rng, customers, campaigns)
    generate_support(rng, customers)
    generate_returns(rng)

    manifest = {
        "orders": COUNTS["orders"],
        "order_items": COUNTS["order_items"],
        "payments": COUNTS["payments"],
        "web_sessions": COUNTS["web_sessions"],
        "marketing_interactions": COUNTS["marketing_interactions"],
        "support_cases": COUNTS["support_cases"],
        "returns": COUNTS["returns"],
    }
    (COMMERCE_DIR.parent / "activity_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print("Activity source generation complete.")


if __name__ == "__main__":
    main()
