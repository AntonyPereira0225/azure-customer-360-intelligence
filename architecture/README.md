# Target Architecture

The Azure Enterprise Customer 360 & Revenue Intelligence Lakehouse will be implemented as a layered analytical platform. This document describes the target design for Phase 1; implementation status will be updated as each component is actually built.

> All data and systems in this project are synthetic.

## End-to-End Flow

```text
SOURCE SYSTEMS

CRM / customer files
Orders / order items / payments
Products / categories
Marketing campaigns / interactions
Web & app sessions
Customer support / returns
        |
        v
AZURE DATA FACTORY
- scheduled ingestion
- source metadata
- parameterised pipelines
- failure handling
        |
        v
ADLS GEN2 LANDING / RAW
- immutable source-aligned landing
- source / date / batch partitioning
        |
        v
AZURE DATABRICKS + DELTA LAKE
        |
        +--> BRONZE
        |    - source-aligned Delta tables
        |    - ingestion metadata
        |    - minimal transformation
        |
        +--> SILVER
        |    - standardisation
        |    - deduplication
        |    - referential integrity
        |    - type validation
        |    - business-rule checks
        |    - quarantine of invalid records
        |
        +--> GOLD
             - conformed dimensions
             - fact tables
             - Customer 360
             - revenue mart
             - campaign mart
             - customer-health mart
             - data-quality mart
        |
        v
POWER BI
- Executive Performance
- Customer 360
- Commercial & Marketing Intelligence
- Customer Experience
- Data Quality & Platform Health
```

## Cross-Cutting Controls

```text
Unity Catalog   -> table / schema governance and permissions
Key Vault       -> secrets and connection credentials
Microsoft Purview -> catalogue, lineage and governance evidence
Azure Monitor   -> operational monitoring where implemented
Git / GitHub    -> source control
Azure DevOps    -> CI/CD and deployment patterns
Terraform       -> infrastructure-as-code for selected resources
```

## Logical Storage Zones

The intended ADLS structure is:

```text
/landing
    /crm
    /sales
    /payments
    /products
    /marketing
    /digital
    /support

/bronze
/silver
/gold
/quarantine
/checkpoints
/audit
```

The exact physical paths will be updated once the Azure environment is created.

## Bronze Design

Bronze tables preserve source fidelity while attaching technical metadata such as:

- `ingestion_timestamp`
- `source_system`
- `source_file` or source object
- `batch_id`
- optional source modification timestamp

Bronze is not a reporting layer.

## Silver Design

Silver data represents trusted, standardised entity and event datasets. Core transformations will include:

- deterministic type conversion;
- null and domain validation;
- duplicate handling;
- customer and product key validation;
- status standardisation;
- currency standardisation where required;
- business-rule validation;
- late-arriving data handling where implemented;
- rejected-row quarantine with failure reason.

## Gold Design

Gold data products are designed for BI and downstream analytics rather than mirroring source systems.

Planned conformed dimensions:

- `dim_customer`
- `dim_product`
- `dim_date`
- `dim_channel`
- `dim_campaign`
- `dim_region`

Planned fact tables:

- `fact_sales`
- `fact_customer_activity`
- `fact_marketing`
- `fact_support`
- `fact_returns`

Planned marts:

- `gold_customer_360`
- `gold_revenue_performance`
- `gold_campaign_performance`
- `gold_customer_health`
- `gold_data_quality`

## Security and Privacy Principles

- synthetic surrogate identifiers only;
- no credentials stored in source code;
- least-privilege access patterns where practical;
- Key Vault for secrets once Azure integration is implemented;
- unnecessary demographic and sensitive attributes excluded from the model;
- role-based access and Power BI row-level security demonstrated where useful.

## Data Quality Architecture

Critical quality failures should be observable rather than silently corrected.

The intended pattern is:

```text
Source record
     |
     v
Validation rules
  /       \
PASS      FAIL
 |          |
Silver    Quarantine
 |          |
Gold     reason_code
         batch_id
         source metadata
```

A Gold data-quality mart will expose quality trends to Power BI.

## Orchestration Strategy

The initial implementation will be batch-oriented. Azure Data Factory will orchestrate source ingestion and Databricks workloads. Pipelines should be parameterised by environment, source and load date where appropriate.

Incremental loading and restartability will be implemented before the project is described as operationally complete.

## Deployment Strategy

The project will progressively separate:

```text
Development
Testing
Production-like portfolio environment
```

CI/CD and Terraform will be added only after core pipelines are validated. The repository will not claim production-grade deployment automation before those artefacts are implemented and tested.

## Architecture Acceptance Criteria

The final implementation should demonstrate that:

1. every Gold data product has traceable source lineage;
2. Power BI consumes curated data products rather than raw source extracts;
3. failed critical quality records are observable and auditable;
4. Azure secrets are not exposed in GitHub;
5. code and infrastructure artefacts are version controlled;
6. architecture documentation matches the implemented environment.
