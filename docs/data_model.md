# Target Data Model

This document defines the initial logical data model for the Azure Enterprise Customer 360 & Revenue Intelligence Lakehouse. It is a Phase 1 design artefact and will be updated as the synthetic source data and Azure implementation are built.

All records and entities are synthetic.

## 1. Source Domains

The planned source domains are:

- Customer / CRM
- Orders
- Order Items
- Payments
- Returns
- Products
- Product Categories
- Marketing Campaigns
- Campaign Interactions
- Web / App Sessions
- Support Cases
- Case Interactions
- Geography / Market Reference

## 2. Core Entity Relationships

```text
Customer
   |
   +----< Order >---- Order Item >---- Product >---- Category
   |        |
   |        +---- Payment
   |        +---- Return
   |
   +----< Campaign Interaction >---- Campaign
   |
   +----< Digital Session
   |
   +----< Support Case >---- Case Interaction
```

## 3. Bronze Layer

Bronze tables will preserve source-aligned schemas and technical metadata.

Planned Bronze tables include:

- `bronze_customers`
- `bronze_customer_addresses`
- `bronze_orders`
- `bronze_order_items`
- `bronze_payments`
- `bronze_returns`
- `bronze_products`
- `bronze_categories`
- `bronze_campaigns`
- `bronze_campaign_interactions`
- `bronze_digital_sessions`
- `bronze_support_cases`
- `bronze_case_interactions`

Technical metadata will include fields such as:

- `ingestion_timestamp`
- `source_system`
- `source_object`
- `batch_id`
- `source_record_id` where applicable

## 4. Silver Layer

Silver tables will represent standardised, validated business entities and events.

### `silver_customers`

**Grain:** one mastered current customer record per synthetic customer key.

Planned fields:

- `customer_id`
- `customer_segment`
- `signup_date`
- `country_code`
- `preferred_channel`
- `customer_status`
- `account_tenure_months`
- `record_effective_from`
- `record_effective_to`
- `is_current`

Where SCD Type 2 is implemented, historical customer attribute changes will be retained in the analytical dimension rather than overwritten silently.

### `silver_orders`

**Grain:** one row per order.

Planned fields:

- `order_id`
- `customer_id`
- `order_timestamp`
- `channel_code`
- `country_code`
- `order_status`
- `currency_code`
- `gross_order_amount`
- `discount_amount`
- `net_order_amount`

### `silver_order_items`

**Grain:** one row per product line in an order.

Planned fields:

- `order_item_id`
- `order_id`
- `product_id`
- `quantity`
- `unit_price`
- `discount_amount`
- `net_line_revenue`
- `unit_cost`
- `line_margin`

### `silver_payments`

**Grain:** one row per payment attempt / event.

Planned fields:

- `payment_id`
- `order_id`
- `payment_timestamp`
- `payment_method`
- `payment_status`
- `payment_amount`
- `currency_code`

### `silver_returns`

**Grain:** one row per returned order item event.

Planned fields:

- `return_id`
- `order_id`
- `order_item_id`
- `return_timestamp`
- `return_quantity`
- `return_reason`
- `refund_amount`

### `silver_products`

**Grain:** one row per current product record.

Planned fields:

- `product_id`
- `product_name`
- `category_id`
- `brand`
- `standard_cost`
- `list_price`
- `product_status`

### `silver_campaigns`

**Grain:** one row per campaign.

Planned fields:

- `campaign_id`
- `campaign_name`
- `campaign_channel`
- `start_date`
- `end_date`
- `campaign_cost`
- `campaign_objective`

### `silver_campaign_interactions`

**Grain:** one row per customer-campaign interaction event.

Planned fields:

- `interaction_id`
- `campaign_id`
- `customer_id`
- `interaction_timestamp`
- `interaction_type`
- `converted_flag`
- `attributed_order_id` where the synthetic attribution rule links an order

### `silver_digital_sessions`

**Grain:** one row per web or app session.

Planned fields:

- `session_id`
- `customer_id` when authenticated
- `session_timestamp`
- `digital_channel`
- `device_type`
- `traffic_source`
- `pages_or_events`
- `session_duration_seconds`
- `conversion_flag`

### `silver_support_cases`

**Grain:** one row per support case.

Planned fields:

- `case_id`
- `customer_id`
- `opened_timestamp`
- `closed_timestamp`
- `case_category`
- `case_priority`
- `case_status`
- `resolution_hours`
- `satisfaction_score` where simulated

## 5. Gold Dimensions

### `dim_customer`

**Grain:** one row per effective customer dimension record.

Planned fields:

- `customer_key` - surrogate warehouse key
- `customer_id` - synthetic business key
- `customer_segment`
- `country_code`
- `region`
- `preferred_channel`
- `customer_status`
- `signup_date`
- `account_tenure_months`
- SCD2 effective-date fields where implemented

The model intentionally avoids unnecessary demographic or directly identifying personal attributes.

### `dim_product`

- `product_key`
- `product_id`
- `product_name`
- `category`
- `brand`
- `product_status`

### `dim_date`

- `date_key`
- `date`
- `day`
- `week`
- `month`
- `month_name`
- `quarter`
- `year`
- `day_of_week`
- `is_weekend`

### `dim_channel`

- `channel_key`
- `channel_code`
- `channel_name`
- `channel_group`

### `dim_campaign`

- `campaign_key`
- `campaign_id`
- `campaign_name`
- `campaign_channel`
- `campaign_objective`
- `start_date`
- `end_date`

### `dim_region`

- `region_key`
- `country_code`
- `country_name`
- `region_name`
- `currency_code`

## 6. Gold Facts

### `fact_sales`

**Grain:** one row per valid order item.

Measures may include:

- quantity
- gross revenue
- discount
- net revenue
- cost
- margin
- returned quantity
- refund amount

Foreign keys:

- customer key
- product key
- order date key
- channel key
- region key

### `fact_customer_activity`

**Grain:** one customer activity event at a defined event timestamp.

May consolidate analytical event types such as purchase, session, marketing engagement and support interaction where useful, while retaining source event lineage.

### `fact_marketing`

**Grain:** one customer-campaign interaction.

Measures / flags may include:

- engagement flag
- conversion flag
- attributed revenue
- attributed margin

### `fact_support`

**Grain:** one support case.

Measures may include:

- resolution hours
- reopen count
- satisfaction score
- case count

### `fact_returns`

**Grain:** one return event per order item.

Measures may include:

- return quantity
- refund amount
- days to return

## 7. Gold Business Marts

### `gold_customer_360`

**Grain:** one row per current customer.

Planned derived measures:

- lifetime gross revenue
- lifetime net revenue
- lifetime margin
- total orders
- average order value
- purchase frequency
- days since last purchase
- return rate
- preferred channel
- digital sessions
- marketing engagements
- campaign conversions
- support-case count
- average support resolution time
- RFM scores and segment
- customer-value segment
- customer-health indicators

### `gold_revenue_performance`

Business-ready revenue and margin measures by date, product, category, channel and geography.

### `gold_campaign_performance`

Campaign cost, reach, engagement, conversion and synthetic attributed revenue / margin measures.

### `gold_customer_health`

Customer-level behavioural and service indicators designed for descriptive retention analysis and later ML extension.

### `gold_data_quality`

Quality metrics by source, table, rule, batch and processing layer.

Planned fields / measures include:

- processing date
- batch id
- source system
- dataset
- quality rule id
- evaluated rows
- failed rows
- pass rate
- severity
- freshness indicator

## 8. Key Modelling Principles

- define a clear grain for every table;
- use surrogate keys in analytical dimensions;
- maintain business keys for lineage;
- keep measures in facts and descriptive attributes in dimensions;
- use conformed dimensions across business marts;
- do not mix raw ingestion columns into business-facing Gold tables without purpose;
- document SCD behaviour explicitly;
- reconcile Gold aggregates to validated Silver/source totals;
- preserve rejected-record reasons in the quarantine layer;
- avoid unsupported causal claims from descriptive data.

## 9. Open Design Decisions

The following will be finalised during Phase 2 and Azure implementation:

- exact country / market set;
- currency standardisation approach;
- SCD2 attributes for customer and product dimensions;
- campaign attribution rule;
- precise customer-health definition;
- partition strategy for large Delta tables;
- incremental-load watermark fields;
- exact Gold mart physical schemas.
