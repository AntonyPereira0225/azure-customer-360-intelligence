# Synthetic Enterprise Source Data

This project uses synthetic data only. No real customer, employee, merchant, marketing or payment records are used.

The generator creates heterogeneous source-system extracts that will later be ingested into Azure Data Lake Storage Gen2 and processed through Bronze, Silver and Gold layers in Azure Databricks.

## Scale profiles

The generator supports two deterministic profiles through the `DATA_SCALE` environment variable.

### `sample` — default local development profile

- 25,000 customers
- 1,000 products
- 40 campaigns
- 250,000 orders
- 600,000 order items
- 250,000 payments
- 500,000 digital sessions
- 200,000 marketing interactions
- 35,000 support cases
- 20,000 returns

### `portfolio` — full portfolio scale

- 250,000 customers
- 5,000 products
- 100 campaigns
- 2,500,000 orders
- 7,000,000 order items
- 2,500,000 payments
- 5,000,000 digital sessions
- 2,000,000 marketing interactions
- 350,000 support cases
- 200,000 returns

The analysis window is 1 September 2024 through 31 August 2026.

## Source-system layout

```text
data/generated/
├── crm/
│   └── customers.csv
├── reference/
│   ├── countries.csv
│   ├── products.csv
│   ├── campaigns.csv
│   └── reference_manifest.json
├── commerce/
│   ├── orders_part_*.parquet
│   ├── order_items_part_*.parquet
│   ├── payments_part_*.parquet
│   └── returns_part_*.parquet
├── marketing/
│   └── interactions_part_*.parquet
├── digital/
│   └── sessions_part_*.parquet
├── service/
│   └── support_cases_part_*.parquet
└── validation/
    └── raw_generation_validation.json
```

## Deliberate raw-source quality issues

Small deterministic defect rates are introduced to create realistic Bronze-to-Silver transformation work, including duplicate CRM customers, missing customer country, malformed synthetic email values, missing product categories, negative product prices, orphan customer/product/campaign keys, missing timestamps, negative order values, missing payment methods and invalid support resolution times.

These issues are **not accidental generator failures**. The raw validation layer profiles them as warnings while treating missing files or incorrect row counts as critical failures. Later Databricks Silver transformations will standardise valid records and route invalid records to quarantine tables.

## Running locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the default sample profile:

```bash
python src/run_generation.py
```

On Windows PowerShell, run the full portfolio profile with:

```powershell
$env:DATA_SCALE="portfolio"
python src/run_generation.py
```

Generated outputs are deliberately excluded from Git because they are reproducible and may be large.
