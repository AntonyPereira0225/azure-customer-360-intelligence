# Business Requirements Document

## 1. Purpose

This document defines the business requirements for the **Azure Enterprise Customer 360 & Revenue Intelligence Lakehouse**, a synthetic portfolio implementation of an enterprise analytics platform.

The fictional organisation operates across Ireland and other European markets and currently holds customer and commercial data across multiple disconnected source systems. The proposed platform will consolidate these sources into a governed Azure lakehouse and provide trusted data products for Customer 360, revenue intelligence, marketing analytics, customer experience and data-quality monitoring.

All entities, transactions and outcomes in this project are synthetic.

## 2. Business Problem

The organisation currently experiences the following analytical challenges:

1. Customer records are fragmented across CRM, sales, marketing and customer-service systems.
2. Revenue and customer KPIs require manual reconciliation across multiple sources.
3. Marketing teams cannot consistently connect campaign activity to customer and revenue outcomes.
4. Customer-service data is analysed separately from commercial behaviour.
5. Duplicate and incomplete customer records create inconsistent reporting.
6. Management dashboards do not expose the freshness or quality of underlying data.
7. Analytical definitions are not standardised across business functions.
8. Existing reporting processes are difficult to scale as data volumes and source systems increase.

## 3. Business Objectives

The platform should:

- establish a governed single analytical view of customers across source systems;
- provide consistent revenue, customer, campaign and service KPIs;
- enable drill-down from executive metrics to customer, product, channel and regional detail;
- standardise and validate source data before it is promoted to business-ready reporting layers;
- support incremental ingestion and repeatable transformation pipelines;
- expose data-quality and freshness indicators to analytical users;
- create reusable Gold-layer data products for Power BI and future machine-learning use cases;
- document requirements, data lineage, business rules, metric definitions and UAT evidence.

## 4. Stakeholders

| Stakeholder | Primary need |
|---|---|
| Executive Leadership | Trusted view of revenue, customers, growth, margin and major risks |
| Commercial / Sales | Product, category, channel and regional performance |
| Marketing | Campaign performance, engagement, conversion and attributed revenue |
| Customer Experience | Support demand, resolution performance, returns and customer health |
| Finance | Consistent revenue and margin measures with traceable definitions |
| Data / BI Team | Reusable curated datasets, semantic models and controlled KPI logic |
| Data Engineering | Reliable ingestion, transformation, quality and orchestration patterns |
| Governance / Risk | Data lineage, controlled access, quality evidence and minimised customer attributes |

## 5. In-Scope Source Domains

The synthetic source landscape will include:

- CRM customer master data;
- customer address / market information;
- products and categories;
- orders and order items;
- payments;
- returns;
- marketing campaigns and customer interactions;
- web and app sessions;
- support cases and case interactions.

## 6. In-Scope Analytical Domains

### 6.1 Customer 360

The platform should support a consolidated analytical customer profile containing measures such as:

- customer tenure;
- lifetime orders;
- lifetime gross and net revenue;
- lifetime margin;
- average order value;
- purchase frequency;
- recency;
- return rate;
- preferred sales channel;
- digital engagement;
- marketing engagement;
- support-case volume;
- customer-value segment;
- RFM segment;
- customer-health / retention indicators.

### 6.2 Revenue and Commercial Intelligence

Required analytical capability includes:

- gross revenue;
- net revenue;
- gross margin;
- average order value;
- order volume;
- revenue growth;
- revenue by country / region;
- revenue by product / category;
- revenue by channel;
- customer contribution to revenue and margin;
- returns and refunds impact.

### 6.3 Marketing Intelligence

Required analytical capability includes:

- campaign reach;
- customer engagement;
- conversion rate;
- campaign-attributed orders and revenue;
- campaign cost;
- cost per acquisition;
- campaign ROI;
- performance by customer segment and channel.

### 6.4 Customer Experience

Required analytical capability includes:

- support case volume;
- case category;
- resolution time;
- reopened cases where simulated;
- customer-support intensity;
- return behaviour;
- relationship between service interactions and customer activity.

No causal conclusion will be claimed solely from descriptive associations.

### 6.5 Data Quality and Platform Health

The platform should expose:

- row counts by source and layer;
- duplicate counts;
- null / completeness rates;
- referential-integrity failures;
- invalid business values;
- quarantined records;
- schema-change detection where implemented;
- data freshness;
- pipeline execution status.

## 7. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | Ingest data from multiple synthetic source types into an Azure landing zone. |
| FR-02 | Preserve source-aligned Bronze data with ingestion metadata. |
| FR-03 | Standardise, validate and deduplicate data before Silver promotion. |
| FR-04 | Quarantine records that fail defined critical quality rules. |
| FR-05 | Maintain auditable transformation logic between Bronze, Silver and Gold. |
| FR-06 | Create conformed dimensions and fact tables for BI consumption. |
| FR-07 | Create a reusable Gold Customer 360 data product. |
| FR-08 | Create business marts for revenue, campaign, customer-health and data-quality reporting. |
| FR-09 | Support incremental / repeatable pipeline execution. |
| FR-10 | Publish business-ready data to Power BI using controlled semantic logic. |
| FR-11 | Implement row-level or role-based access patterns where appropriate for the portfolio scope. |
| FR-12 | Document source-to-target mappings, metric definitions and data-quality rules. |
| FR-13 | Provide UAT scenarios demonstrating reconciliation and business-rule validation. |
| FR-14 | Maintain Git-based version control for code, notebooks and configuration artefacts. |

## 8. Non-Functional Requirements

### NFR-01 Reproducibility

The synthetic dataset and transformations should be reproducible from code and configuration.

### NFR-02 Scalability

The implementation should use partitioned / distributed processing patterns appropriate for multi-million-row data without claiming enterprise-scale performance unless measured.

### NFR-03 Security

No credentials, access keys or secrets may be committed to GitHub. Azure secrets should be managed through environment-safe mechanisms such as Key Vault where implemented.

### NFR-04 Privacy by Design

The dataset will contain synthetic surrogate identifiers only. The project will avoid unnecessary demographic or directly identifying attributes.

### NFR-05 Data Quality

Critical data-quality checks should fail or quarantine records rather than silently accepting invalid data.

### NFR-06 Observability

Pipeline status, row counts and quality metrics should be measurable and documented.

### NFR-07 Maintainability

Transformations should be separated into reusable Bronze, Silver, Gold and utility components with clear naming and documentation.

## 9. Initial Business Rules

Examples of rules to be refined during data modelling:

- every order must map to a valid customer;
- every order item must map to a valid order and product;
- payment amounts must not be negative;
- fulfilled orders should contain at least one valid order item;
- return quantities cannot exceed purchased quantities for the same order item;
- campaign interactions must map to valid campaigns;
- customer keys must be unique within the mastered customer dataset;
- revenue and margin calculations must use documented business definitions;
- critical rejected records must retain failure reason and source lineage.

## 10. Success Criteria

Phase completion will require evidence that:

1. the synthetic sources are reproducible and validated;
2. Azure ingestion successfully lands the required source domains;
3. Bronze, Silver and Gold layers are implemented with documented lineage;
4. critical quality failures are detectable and auditable;
5. Gold facts, dimensions and Customer 360 marts reconcile to validated source totals;
6. Power BI reports use controlled business definitions;
7. UAT checks demonstrate consistency between source, lakehouse and BI outputs;
8. governance and deployment artefacts accurately reflect what was actually implemented.

## 11. Out of Scope for Initial Release

The first implementation will not claim:

- real customer or company data;
- production-grade security certification;
- real-time streaming unless subsequently implemented and evidenced;
- causal marketing attribution beyond the synthetic attribution rules;
- production ML decisioning;
- real-world churn prediction performance.

ML and MLOps will be treated as a later extension built on top of the completed lakehouse.
