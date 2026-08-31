"""Profile structural integrity and deliberate raw-source defects.

This validator distinguishes critical generation failures from expected raw-source
quality issues. The latter are intentionally retained so the Databricks Silver
layer can demonstrate cleansing, quarantine and quality-monitoring logic.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from config import (
    COMMERCE_DIR,
    COUNTS,
    CRM_DIR,
    DIGITAL_DIR,
    MARKETING_DIR,
    REFERENCE_DIR,
    REPORT_DIR,
    SCALE_PROFILE,
    SERVICE_DIR,
)


def _count_parquet(directory: Path, prefix: str) -> int:
    total = 0
    for path in sorted(directory.glob(f"{prefix}_part_*.parquet")):
        total += pq.ParquetFile(path).metadata.num_rows
    return total


def _count_condition(directory: Path, prefix: str, column: str, predicate) -> int:
    total = 0
    for path in sorted(directory.glob(f"{prefix}_part_*.parquet")):
        df = pd.read_parquet(path, columns=[column])
        total += int(predicate(df[column]).sum())
    return total


def _record(
    checks: list[dict[str, object]],
    name: str,
    passed: bool,
    detail: str,
    severity: str,
) -> None:
    checks.append(
        {
            "check": name,
            "passed": bool(passed),
            "severity": severity,
            "detail": detail,
        }
    )


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    checks: list[dict[str, object]] = []

    required_files = {
        "customers": CRM_DIR / "customers.csv",
        "countries": REFERENCE_DIR / "countries.csv",
        "products": REFERENCE_DIR / "products.csv",
        "campaigns": REFERENCE_DIR / "campaigns.csv",
    }
    for name, path in required_files.items():
        _record(checks, f"{name}: source exists", path.exists(), str(path), "critical")

    if not all(path.exists() for path in required_files.values()):
        output = {"status": "FAIL", "scale_profile": SCALE_PROFILE, "checks": checks}
        (REPORT_DIR / "raw_generation_validation.json").write_text(
            json.dumps(output, indent=2), encoding="utf-8"
        )
        raise SystemExit("Critical source files are missing. Run reference generation first.")

    customers = pd.read_csv(required_files["customers"])
    products = pd.read_csv(required_files["products"])
    campaigns = pd.read_csv(required_files["campaigns"])

    expected_activity = {
        "orders": (COMMERCE_DIR, "orders", COUNTS["orders"]),
        "order_items": (COMMERCE_DIR, "order_items", COUNTS["order_items"]),
        "payments": (COMMERCE_DIR, "payments", COUNTS["payments"]),
        "returns": (COMMERCE_DIR, "returns", COUNTS["returns"]),
        "sessions": (DIGITAL_DIR, "sessions", COUNTS["web_sessions"]),
        "marketing_interactions": (
            MARKETING_DIR,
            "interactions",
            COUNTS["marketing_interactions"],
        ),
        "support_cases": (SERVICE_DIR, "support_cases", COUNTS["support_cases"]),
    }
    row_counts: dict[str, int] = {}
    for name, (directory, prefix, expected) in expected_activity.items():
        count = _count_parquet(directory, prefix)
        row_counts[name] = count
        _record(
            checks,
            f"{name}: expected row count",
            count == expected,
            f"rows={count:,}; expected={expected:,}",
            "critical",
        )

    unique_customers = customers["customer_id"].nunique()
    _record(
        checks,
        "customers: unique base population",
        unique_customers == COUNTS["customers"],
        f"unique={unique_customers:,}; expected={COUNTS['customers']:,}; raw_rows={len(customers):,}",
        "critical",
    )
    _record(
        checks,
        "products: base population",
        products["product_id"].nunique() == COUNTS["products"],
        f"unique={products['product_id'].nunique():,}; expected={COUNTS['products']:,}",
        "critical",
    )
    _record(
        checks,
        "campaigns: base population",
        campaigns["campaign_id"].nunique() == COUNTS["campaigns"],
        f"unique={campaigns['campaign_id'].nunique():,}; expected={COUNTS['campaigns']:,}",
        "critical",
    )

    # Expected raw-source defect profile. These checks do not fail the run.
    quality_profile = {
        "customer_duplicate_rows": int(customers.duplicated("customer_id", keep=False).sum()),
        "customer_missing_country": int(customers["home_country"].isna().sum()),
        "customer_invalid_email": int(
            (~customers["synthetic_email"].str.contains("@", na=False)).sum()
        ),
        "product_missing_category": int(products["category"].isna().sum()),
        "product_negative_price": int((products["unit_price_eur"] < 0).sum()),
        "order_orphan_customer": _count_condition(
            COMMERCE_DIR, "orders", "customer_id", lambda s: s.eq("C_ORPHAN")
        ),
        "order_missing_timestamp": _count_condition(
            COMMERCE_DIR, "orders", "order_timestamp", lambda s: s.isna()
        ),
        "order_negative_value": _count_condition(
            COMMERCE_DIR, "orders", "order_value_eur", lambda s: s < 0
        ),
        "order_item_orphan_product": _count_condition(
            COMMERCE_DIR, "order_items", "product_id", lambda s: s.eq("P_ORPHAN")
        ),
        "payment_missing_method": _count_condition(
            COMMERCE_DIR, "payments", "payment_method", lambda s: s.isna()
        ),
        "session_missing_timestamp": _count_condition(
            DIGITAL_DIR, "sessions", "session_start", lambda s: s.isna()
        ),
        "marketing_orphan_campaign": _count_condition(
            MARKETING_DIR,
            "interactions",
            "campaign_id",
            lambda s: s.eq("CMP_ORPHAN"),
        ),
        "support_negative_resolution": _count_condition(
            SERVICE_DIR, "support_cases", "resolution_minutes", lambda s: s < 0
        ),
    }

    for name, count in quality_profile.items():
        _record(
            checks,
            f"raw quality profile: {name}",
            count > 0,
            f"identified_rows={count:,}; expected deliberate raw-source issue",
            "warning",
        )

    critical_failures = [
        c for c in checks if c["severity"] == "critical" and not c["passed"]
    ]
    output = {
        "status": "PASS" if not critical_failures else "FAIL",
        "scale_profile": SCALE_PROFILE,
        "critical_failures": len(critical_failures),
        "row_counts": row_counts,
        "raw_quality_profile": quality_profile,
        "checks": checks,
    }
    report_path = REPORT_DIR / "raw_generation_validation.json"
    report_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"Validation status: {output['status']}")
    print(f"Scale profile: {SCALE_PROFILE}")
    for name, count in row_counts.items():
        print(f"  {name}: {count:,}")
    print("Deliberate raw-source defects detected:")
    for name, count in quality_profile.items():
        print(f"  {name}: {count:,}")
    print(f"Report: {report_path}")

    if critical_failures:
        raise SystemExit("Critical generation checks failed.")


if __name__ == "__main__":
    main()
