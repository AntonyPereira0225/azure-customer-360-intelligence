# Azure Enterprise Customer 360 & Revenue Intelligence Lakehouse

An enterprise-style Azure analytics portfolio project demonstrating how fragmented customer, sales, payment, marketing, digital and service data can be integrated into a governed lakehouse for Customer 360, revenue intelligence, data quality monitoring and executive reporting.

> **Portfolio note:** All data used in this project is synthetic. The project is not affiliated with any real company, customer, cloud client or financial institution.

## Business Objective

A fictional multinational consumer business operates across Ireland and other European markets. Customer and commercial data is distributed across CRM extracts, transactional systems, marketing platforms, web/app activity and customer-support systems.

The objective is to design and build a trusted Azure analytics platform that enables decision-makers to answer questions such as:

- Which customers and segments generate the most revenue and margin?
- Which products, channels and regions drive commercial performance?
- Which customers show declining engagement or potential churn signals?
- Which campaigns generate measurable conversion and revenue?
- How do returns and support interactions relate to customer value and experience?
- Can management trust the completeness, freshness and consistency of the data feeding Power BI?

## Planned Technology Stack

Azure Data Lake Storage Gen2 · Azure Data Factory · Azure Databricks · PySpark · Spark SQL · Delta Lake · Databricks SQL · Unity Catalog · Azure Key Vault · Microsoft Purview · Power BI · DAX · Python · SQL · Git/GitHub · Azure DevOps · Terraform

## Target Architecture

```text
Synthetic source systems
        |
        +-- CRM / flat files
        +-- orders & payments
        +-- product data
        +-- marketing events
        +-- web/app sessions
        +-- customer support
        |
        v
Azure Data Factory
        |
        v
ADLS Gen2 - landing/raw
        |
        v
Azure Databricks
        |
        +-- Bronze: source-aligned Delta data
        +-- Silver: validated, standardised and deduplicated data
        +-- Gold: business-ready dimensional models and marts
        |
        v
Power BI semantic model
        |
        +-- Executive Performance
        +-- Customer 360
        +-- Commercial & Marketing Intelligence
        +-- Customer Experience
        +-- Data Quality & Platform Health
```

Governance, security and deployment controls will be added through Unity Catalog, Key Vault, Purview, Azure DevOps and infrastructure-as-code patterns.

## Synthetic Enterprise Source Layer

Phase 2 introduces a deterministic Python generator for heterogeneous source-system data covering CRM, reference/master data, commerce, payments, marketing, digital analytics and customer service.

Two scale profiles are supported:

- `sample` — approximately 1.9 million generated rows for rapid local development and testing
- `portfolio` — approximately 19.8 million generated rows, including 250,000 customers, 2.5 million orders, 7 million order items and 5 million digital sessions

The raw source layer intentionally includes small rates of duplicates, missing fields, orphan keys, malformed values and invalid business measures. These are profiled rather than hidden so later Databricks Silver processing can demonstrate data-quality rules, quarantine handling and observability.

The first complete `sample` run passed structural validation with the expected row counts: 250,000 orders, 600,000 order items, 250,000 payments, 500,000 digital sessions, 200,000 marketing interactions, 35,000 support cases and 20,000 returns. Deliberate raw-source defects were also detected as expected, confirming that the quality framework distinguishes critical generation failures from issues intended for later Silver-layer cleansing and quarantine.

See [`data/README.md`](data/README.md), [`docs/data_quality_rules.md`](docs/data_quality_rules.md) and [`docs/sample_generation_validation.md`](docs/sample_generation_validation.md).

## Planned Analytical Domains

### Customer 360

Customer value, tenure, engagement, purchasing behaviour, preferred channel, service history, returns, RFM segmentation and retention indicators.

### Revenue & Commercial Intelligence

Revenue, net revenue, gross margin, average order value, product/category performance, geographic performance and channel contribution.

### Marketing Intelligence

Campaign reach, engagement, conversion, attributed revenue, acquisition efficiency and campaign ROI.

### Customer Experience

Support demand, resolution performance, return behaviour and experience-related customer signals.

### Data Quality & Platform Health

Completeness, validity, duplicates, failed records, quarantined records, freshness and pipeline execution status.

## Target Data Model

The Gold layer will use business-ready facts and dimensions such as:

```text
Dimensions
- dim_customer
- dim_product
- dim_date
- dim_channel
- dim_campaign
- dim_region

Facts
- fact_sales
- fact_customer_activity
- fact_marketing
- fact_support
- fact_returns

Business marts
- gold_customer_360
- gold_revenue_performance
- gold_campaign_performance
- gold_customer_health
- gold_data_quality
```

## Project Phases

- **Phase 1 - Business requirements and architecture: complete**
- **Phase 2 - Synthetic enterprise dataset: in progress (sample profile validated)**
- Phase 3 - Azure environment and ADLS Gen2
- Phase 4 - Azure Data Factory ingestion
- Phase 5 - Databricks Bronze layer
- Phase 6 - Silver transformations and data quality
- Phase 7 - Gold dimensional model and business marts
- Phase 8 - Power BI semantic model and dashboards
- Phase 9 - Governance, Unity Catalog, Purview and Key Vault
- Phase 10 - CI/CD, Azure DevOps and Terraform
- Phase 11 - Final validation and portfolio documentation

## Repository Structure

```text
azure-customer-360-intelligence/
├── README.md
├── architecture/
├── docs/
├── data/
│   └── generated/
├── src/
├── adf/
├── databricks/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── utilities/
├── sql/
├── powerbi/
├── terraform/
└── devops/
```

## Design Principles

- business requirements before tooling
- synthetic data only
- reproducible generation and validation
- explicit data-quality controls
- separation of raw, validated and business-ready layers
- dimensional modelling for BI consumption
- documented lineage and governance
- no production-readiness claims without evidence
- implementation status documented accurately throughout the project

## Author

**Antony Pereira George**  
Data Analyst | Business Analyst | SQL | Power BI | Python | Business Intelligence
