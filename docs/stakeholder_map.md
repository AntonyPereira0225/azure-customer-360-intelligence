# Stakeholder Map

This document defines the primary fictional stakeholders for the Azure Enterprise Customer 360 & Revenue Intelligence Lakehouse and the decisions each group expects the platform to support.

All stakeholders and business scenarios are synthetic and exist only for portfolio demonstration.

## Stakeholder Groups

| Stakeholder | Key questions | Primary outputs | Priority |
|---|---|---|---|
| Executive Leadership | Are revenue, margin and customer value improving? Where are the biggest risks and opportunities? | Executive Power BI page, monthly KPI scorecard | High |
| Commercial / Sales | Which products, channels, markets and customer segments drive performance? | Revenue and commercial mart, product/channel views | High |
| Marketing | Which campaigns engage, convert and generate profitable revenue? | Campaign performance mart, conversion and ROI reporting | High |
| Customer Experience | Which customers experience high support demand, returns or deteriorating engagement? | Customer-health mart, service and returns dashboard | High |
| Finance | Are revenue, returns and margin metrics consistent and reconcilable? | Controlled metric definitions, reconciliation checks | High |
| Data / BI Team | Can analysts access trusted, reusable and documented data products? | Gold facts/dimensions, semantic model, data dictionary | High |
| Data Engineering | Are ingestion, transformations and quality controls repeatable and supportable? | ADF pipelines, Databricks notebooks/jobs, monitoring | High |
| Governance / Risk | Is lineage understood, access controlled and unnecessary customer data minimised? | Purview/Unity Catalog evidence, access design, quality controls | Medium/High |

## Stakeholder Decision Matrix

### Executive Leadership

**Decisions supported**
- investment focus by market, channel or category;
- performance review against commercial targets;
- identification of deteriorating customer or service indicators;
- prioritisation of management attention.

**Required characteristics**
- concise KPIs;
- consistent definitions;
- trend and variance visibility;
- drill-down capability;
- confidence in freshness and data quality.

### Commercial / Sales

**Decisions supported**
- product and category prioritisation;
- channel strategy;
- regional opportunity analysis;
- customer-segment targeting.

**Required characteristics**
- product/customer/channel detail;
- net revenue rather than gross-only reporting;
- margin visibility;
- returns impact;
- customer contribution analysis.

### Marketing

**Decisions supported**
- campaign investment allocation;
- audience targeting;
- channel optimisation;
- campaign continuation or redesign.

**Required characteristics**
- common campaign IDs;
- customer-level interaction history;
- documented attribution assumptions;
- conversion and revenue linkage;
- cost and ROI measures.

### Customer Experience

**Decisions supported**
- service capacity and issue prioritisation;
- identification of customers with repeated support problems;
- returns/service root-cause investigation;
- customer-health intervention design.

**Required characteristics**
- case type and resolution measures;
- customer/order linkage;
- support and returns history;
- descriptive associations clearly distinguished from causal claims.

### Finance

**Decisions supported**
- KPI sign-off;
- commercial reconciliation;
- margin and returns analysis.

**Required characteristics**
- transparent calculation logic;
- source-to-target lineage;
- reconciled totals;
- controlled metric definitions.

### Data / BI Team

**Decisions supported**
- dashboard development;
- self-service analysis;
- semantic-model reuse.

**Required characteristics**
- conformed dimensions;
- stable Gold tables;
- data dictionary;
- measure definitions;
- quality and freshness metadata.

### Data Engineering

**Decisions supported**
- pipeline operations;
- transformation maintenance;
- quality-rule enforcement;
- deployment planning.

**Required characteristics**
- source metadata;
- deterministic pipelines;
- Bronze/Silver/Gold separation;
- quarantine patterns;
- monitoring and logging;
- Git-based version control.

### Governance / Risk

**Decisions supported**
- data access approval;
- lineage review;
- policy and retention design;
- data minimisation.

**Required characteristics**
- synthetic identifiers only;
- no secrets committed to Git;
- catalogued data products;
- role-based access design;
- unnecessary attributes excluded.

## Initial Reporting Cadence Assumptions

These are design assumptions to be tested during implementation rather than claims about a real organisation:

- executive and commercial reporting: daily refresh;
- marketing reporting: daily refresh;
- customer-service reporting: daily refresh;
- data-quality dashboard: per pipeline run;
- source ingestion: scheduled batch initially;
- streaming / near-real-time processing: out of scope unless later implemented.

## UAT Ownership

| Area | Primary UAT owner |
|---|---|
| Executive KPIs | Executive / Finance proxy |
| Revenue and margin | Finance / Commercial proxy |
| Campaign measures | Marketing proxy |
| Customer 360 | BI / Customer Experience proxy |
| Data quality | Data Engineering / BI proxy |
| Security and lineage | Governance proxy |

Because this is a portfolio project, the project author will execute the UAT scenarios while preserving the stakeholder perspective defined above.
