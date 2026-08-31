# Sample Generation Validation

The local `sample` scale profile completed successfully before any portfolio-scale generation or Azure ingestion work.

> All records in this project are synthetic. The deliberate defects below are intentionally injected raw-source issues for later Bronze-to-Silver data-quality demonstrations; they are not accidental generation failures.

## Validation outcome

**Status:** PASS  
**Scale profile:** `sample`

### Generated activity row counts

| Dataset | Rows |
|---|---:|
| Orders | 250,000 |
| Order items | 600,000 |
| Payments | 250,000 |
| Returns | 20,000 |
| Digital sessions | 500,000 |
| Marketing interactions | 200,000 |
| Support cases | 35,000 |

### Reference and CRM source counts

| Dataset | Rows |
|---|---:|
| Countries | 12 |
| Raw CRM customer rows | 25,050 |
| Products | 1,000 |
| Campaigns | 40 |

The CRM source contains 25,000 unique base customers plus deliberately injected duplicate records.

## Deliberate raw-source defect profile

| Raw-source issue | Detected rows |
|---|---:|
| Customer duplicate rows | 100 |
| Customer missing country | 37 |
| Customer malformed synthetic email | 25 |
| Product missing category | 1 |
| Product negative price | 1 |
| Order orphan customer key | 125 |
| Order missing timestamp | 100 |
| Order negative value | 75 |
| Order-item orphan product key | 300 |
| Payment missing method | 125 |
| Session missing timestamp | 250 |
| Marketing orphan campaign key | 100 |
| Support negative resolution time | 17 |

## Interpretation

The sample run confirms that the generator produces the expected source volumes and that the validation framework distinguishes structural generation failures from intentionally introduced raw-data defects.

These defects will later be handled in the Azure Databricks Silver layer through cleansing, standardisation, referential-integrity checks, business-rule validation and quarantine tables. Data-quality metrics will also feed the planned Power BI Data Quality & Platform Health page.

## Next validation gate

The same framework will be run using the `portfolio` scale profile before the data is staged for Azure Data Lake Storage Gen2. Portfolio-scale row counts and quality metrics will be documented separately after that run succeeds.
