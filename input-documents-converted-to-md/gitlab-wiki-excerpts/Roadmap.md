## Development Roadmap

The development and release of Project Lion are planned in several phases:

**High-Level Roadmap (from Business Overview):**

| Phase                     | Timeline           | Highlights                                                             |
| ------------------------- | ------------------ | ---------------------------------------------------------------------- |
| Planning & Infrastructure | Underway → Q2 2025 | Finalize features, stand‑up cloud & DevOps                             |
| Core Catalog Build        | Q2–Q3 2025         | Establish Catalog Service (OpenMatadata), ingestion ETL, agile sprints |
| Ingestion & Dissemination | Q4 2025            | Connect pipelines, heavy testing                                       |
| **Pilot Launch (MVP)**    | **December 2025**  | Early adopter                                                          |
| **Version 1.0**           | **March 2026**     | Official Release                                                       |

**Detailed Phased Rollout:**

* **Phase 0: Setup (9 Jun - 18 Jun 2025)**
  
  * **Epics:**
    * Repository Setup: Create GitLab repos with folder skeletons.
    * Local Development Stack: Deliver docker‑compose.yml, Makefile, bootstrap scripts for core services (edge, ingestion, enrichment, catalog).
    * Continuous Integration Skeleton: Add lint, unit‑test; enforce branch protection.

* **Phase 1: Ingestion (19 Jun - 31 Jul 2025)**
  
  * **Epics:**
    * Edge Connector v1: TypeScript Lambda for S3 events, GDAL header parsing, send JSON to Ingestion Gateway.
    * Ingestion Gateway v1: API, JWT verification, Redis idempotency cache; batch events to Kinesis.
    * Event Enricher: Kinesis consumer to fuse dataset IDs, apply default tags, UPSERT messages to OpenMetadata by API.

* **Phase 2: Search & Discovery (1 Aug - 15 Sep 2025)**
  
  * **Epics:**
    * OpenSearch Cluster & Mapping: Setup OpenSearch Serverless, index geo data and keywords.
    * Bulk Loader Lambda: Load data into OpenSearch after catalog insertion.
    * Search API Adapter: Extend OpenMetadata search to expose API for text, tag, and geo search.
    * React Search Experience: Deliver React/Next.js page with filters and map search.

* **Phase 3: Policy & Access Control (16 Sep - 31 Oct 2025)**
  
  * **Epics:**
    * OPA Integration: Add OPA to Gateway, Broker, and Search.
    * Access Broker v1: Implement presigned‑URL, Proxies, AssumeRole issuance, Redis decision cache, logging.
    * Audit Pipeline: Store access audit logs.

* **Phase 4: Lineage (1 Nov - 30 Nov 2025)**
  
  * **Epics:**
    * OpenLineage Collector: To be defined.
    * Neptune Loader & Schema: To be defined.
    * Lineage GraphQL API & UI: To be defined.

* **Phase 5: Backfill, Testing, and Hardening (1 Dec - 30 Dec 2025)**
  
  * **Epics:**
    * Backfill any gaps.
    * Security & Compliance Checks: AWS CIS, Trivy scanning, npm‑audit.
    * Performance Monitoring & Cost Guards: Load tests, Grafana dashboards, alert rules.
    * Disaster Recovery: Snapshot Postgres & OpenSearch.
