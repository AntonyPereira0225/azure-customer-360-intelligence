# Portfolio-Scale Generation Validation

## Status

**PASS**

The full deterministic `portfolio` profile completed successfully on Windows CMD using:

```cmd
set DATA_SCALE=portfolio
python src\run_generation.py
```

The pipeline was executed twice and produced the same validated row counts and deliberate raw-source defect counts, providing an additional reproducibility check for the generator configuration.

## Validated row counts

| Dataset | Rows |
|---|---:|
| Customers (unique base population) | 250,000 |
| Customers (raw rows including duplicate records) | 250,500 |
| Countries | 12 |
| Products | 5,000 |
| Campaigns | 100 |
| Orders | 2,500,000 |
| Order items | 7,000,000 |
| Payments | 2,500,000 |
| Returns | 200,000 |
| Digital sessions | 5,000,000 |
| Marketing interactions | 2,000,000 |
| Support cases | 350,000 |

This represents approximately 19.8 million generated source rows across CRM, reference, commerce, marketing, digital and service domains.

## Deliberate raw-source defects

The validation framework detected the expected synthetic defects used later for Bronze-to-Silver cleansing, quarantine and data-quality monitoring:

| Quality issue | Detected rows |
|---|---:|
| Duplicate customer rows | 1,000 |
| Missing customer country | 375 |
| Invalid synthetic email | 250 |
| Missing product category | 5 |
| Negative product price | 2 |
| Orphan customer key in orders | 1,250 |
| Missing order timestamp | 1,000 |
| Negative order value | 750 |
| Orphan product key in order items | 3,500 |
| Missing payment method | 1,250 |
| Missing session timestamp | 2,500 |
| Orphan campaign key | 1,000 |
| Negative support resolution time | 175 |

These records are intentionally retained in the raw source layer. They are not treated as accidental generator failures. The Silver layer will apply explicit quality rules, standardisation, deduplication, referential-integrity checks and quarantine handling.

## Validation conclusion

The portfolio-scale source-data generation phase is complete. Structural checks passed, expected row counts were reconciled, and the designed quality-defect profile was present. Generated data remains excluded from Git because it is reproducible and too large for source control.
