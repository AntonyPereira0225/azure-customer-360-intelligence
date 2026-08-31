# Data Quality Rules

The raw synthetic source data deliberately contains a small number of quality defects so the project can demonstrate realistic Bronze-to-Silver controls in Azure Databricks.

## Quality dimensions

The Silver layer will monitor five dimensions:

- **Completeness** — required business fields are populated.
- **Validity** — values conform to permitted formats, domains and numeric ranges.
- **Uniqueness** — business keys do not contain unintended duplicate current records.
- **Consistency** — related values agree across source systems and derived fields.
- **Referential integrity** — foreign keys resolve to trusted parent entities.

## Initial rule catalogue

| Rule ID | Source | Rule | Severity | Planned Silver treatment |
|---|---|---|---|---|
| DQ-CUS-001 | CRM customer | `customer_id` must resolve to one current trusted customer record | High | Deduplicate using latest `source_updated_at`; preserve audit metadata |
| DQ-CUS-002 | CRM customer | `home_country` must be populated and exist in country reference | High | Quarantine unresolved rows |
| DQ-CUS-003 | CRM customer | synthetic email must contain a structurally valid `@` separator | Medium | Null invalid contact value and record quality flag |
| DQ-PRD-001 | Product master | `category` must be populated | Medium | Quarantine or map only where an approved business rule exists |
| DQ-PRD-002 | Product master | `unit_price_eur` must be greater than zero | High | Quarantine invalid product record |
| DQ-ORD-001 | Orders | `customer_id` must exist in trusted customer dimension | High | Quarantine orphan order |
| DQ-ORD-002 | Orders | `order_timestamp` must be populated and within the analytical window | High | Quarantine invalid order |
| DQ-ORD-003 | Orders | `order_value_eur` must be non-negative | High | Quarantine and reconcile to line-item total |
| DQ-ITM-001 | Order items | `product_id` must exist in trusted product dimension | High | Quarantine orphan line |
| DQ-PAY-001 | Payments | `payment_method` must be populated and in the approved domain | Medium | Quarantine or map to `unknown` depending on reporting use |
| DQ-MKT-001 | Marketing | `campaign_id` must exist in campaign master | High | Quarantine orphan interaction |
| DQ-DIG-001 | Digital | `session_start` must be populated | Medium | Exclude from time-series metrics and quarantine for remediation |
| DQ-SVC-001 | Support | `resolution_minutes` must be zero or positive | High | Quarantine invalid service record |

## Quarantine design

Silver processing will separate accepted and rejected rows rather than silently deleting invalid data. Quarantine records should retain:

- source table
- source file or batch
- ingestion timestamp
- business key
- rule ID
- rejection reason
- original source values where appropriate

This supports traceability, root-cause analysis and a Power BI Data Quality & Platform Health page.

## Quality KPIs planned for the Gold layer

- valid-row rate
- rejected-row rate
- duplicate rate
- completeness rate
- orphan-key rate
- records quarantined by source and rule
- data freshness
- latest successful batch
- pipeline success/failure status

The project will not present arbitrary quality thresholds as industry standards. Thresholds used later will be documented as project-specific operating rules.
