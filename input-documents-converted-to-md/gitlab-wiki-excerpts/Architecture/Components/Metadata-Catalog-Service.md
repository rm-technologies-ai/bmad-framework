# Metadata Catalog Service

The **Metadata Catalog Service (MCS)** is the authoritative system of record for all metadata inside Project Lion.  
It runs the OpenMetadata server backed by Aurora PostgreSQL/PostGIS and exposes rich REST & GraphQL APIs that power search, governance, lineage, and access‑control flows across the platform.

## 1. Core Responsibilities

| #   | Capability          | What it does                                                                                                                                                                       |
| --- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Ingest**          | Receives UPSERT calls from the **Enrichment & Indexer** via the OpenMetadata API, recording assets, tags, lineage, policies, and versions.                                         |
| 2   | **Persist**         | Stores structured metadata in **Aurora PostgreSQL** (JSONB + PostGIS extensions for spatial fields).                                                                               |
| 3   | **Index**           | Publishes change notifications to an internal hook that updates **OpenSearch** indices within < 1 s for sub‑second discovery.                                                      |
| 4   | **Serve**           | Exposes REST / GraphQL / WebSocket APIs for UIs, CLIs, SDKs, and other services (Policy Engine, Lineage Graph, Access Broker).                                                     |
| 5   | **Govern**          | Enforces entity‑level RBAC and attribute‑based rules, delegating final allow/deny decisions to the Policy Engine but acting as the source of tags, classifications, and ownership. |
| 6   | **Version & Audit** | Keeps full change history per asset (spec diff + user context) for time‑travel queries and audit reports.                                                                          |

## 2. Technology Stack

| Concern        | Choice                                     | Notes                                                          |
| -------------- | ------------------------------------------ | -------------------------------------------------------------- |
| Catalog engine | **OpenMetadata 1.8**                       | Community‑backed, extensible via custom entities & properties. |
| Database       | **Aurora PostgreSQL 17 + PostGIS**         | JSONB for flexible schema, spatial types for geodata.          |
| Search         | **OpenSearch 2.x**                         | Fed by MCS notification hooks.                                 |
| Lineage proxy  | **Amazon Neptune**                         | MCS emits edge events that the Lineage Graph ingests.          |
| Runtime        | ECS Fargate or K8s (prod) / Docker (local) | Stateless containers.                                          |
| API Auth       | JWT + API Keys + service‑to‑service IAM    | Fine‑grained scopes map to OpenMetadata roles.                 |

---

## 3. Data Model Primer

Project Lion reuses the native OpenMetadata hierarchy - **Domain -> Data Product -> Container -> Asset** - with tenant (Organisation Unit) at the root.  
Custom entities and properties extend the standard model to capture spatial footprint, compliance tags, and rich audit/version data.

```mermaid
classDiagram
%% Core hierarchy %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    class OrganisationUnit{
        +uuid id
        +string name
    }
    class Domain{
        +uuid id
        +string name
        +string description
        +map~string,string~ tags
    }
    class DataProduct{
        +uuid id
        +string name
        +uuid domainId
        +SLA sla
        +Owner owner
        +map tags
    }
    class Container{
        +uuid id
        +string name
        +uuid dataProductId
        +string physicalLocation
        +jsonb customProps
        +map tags
    }
    class Asset{
    +uuid id
    +string name
    +uuid containerId
    +string type
    +string version
    +string uriOrPath
    +bigint sizeBytes
    +jsonb schema
    +jsonb customProps
    +jsonb classification
    +timestamp createdAt
    +timestamp updatedAt
}

%% Governance & lineage %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    class Tag{
        +uuid id
        +string name
        +string color
        +string description
    }
    class Classification{
        +uuid id
        +string name
        +float score
        +uuid tagId
    }
    class LineageEdge{
        +uuid fromAssetId
        +uuid toAssetId
        +string relationType
        +timestamp createdAt
    }
    class Policy{
        +uuid id
        +string name
        +text expression
        +string enforcementPoint
    }
    class Version{
        +uuid assetId
        +int versionNum
        +jsonb diff
        +string changedBy
        +timestamp changedAt
    }

%% Relationships %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    OrganisationUnit "1" --> "*" Domain
    Domain "1" --> "*" DataProduct
    DataProduct "1" --> "*" Container
    Container "1" --> "*" Asset
    Asset "1" --> "*" Tag : has
    Asset "1" --> "*" Classification : classifiedAs
    Asset "1" --> "*" Version : history
    Asset "1" --> "*" LineageEdge : source
    Asset "1" <-- "*" LineageEdge : target
    Policy "1" --> "*" Domain : appliesTo
    Policy "1" --> "*" Asset : appliesTo
```

## 4. High‑Level Sequence - **Detailed Flows**

### 4.1 Asset Ingestion & Indexing

```mermaid
sequenceDiagram
    autonumber
    participant ENR as Enrichment & Indexer Λ
    participant MCS as Metadata Catalog Service
    participant PG  as Aurora PostgreSQL
    participant OS  as OpenSearch
    participant NP  as Neptune (Lineage)
    participant CW  as CloudWatch Logs

    ENR->>MCS: 1 POST /api/v1/assets (asset JSON)
    activate MCS
    MCS->>MCS: 2 validate JSON • resolve ID's • apply policies (pre‑write)
    MCS->>PG: 3 INSERT/UPSERT asset, tags, lineage edges, version row
    PG-->>MCS: 4 commit OK
    MCS-->>CW: 5 write AuditEvent(type="UPSERT", actor="ENR", assetId)
    MCS->>OS: 6 _bulk index document
    MCS->>NP: 7 MERGE lineage edges (if any)
    deactivate MCS
    MCS-->>ENR: 8 200 OK (assetId)
```

*The write finishes only after both indexing calls succeed, ensuring search consistency.*

### 4.2 Interactive Search & Retrieve

```mermaid
sequenceDiagram
    autonumber
    participant UI as Web UI / CLI
    participant MCS as Metadata Catalog Service
    participant OS as OpenSearch
    participant PG as Aurora PostgreSQL
    participant PE as Policy Engine
    participant CW as CloudWatch Logs

    UI->>MCS: 1 GET /search?q=sales_data*&bbox=...
    MCS->>OS: 2 DSL query + geo filter
    OS-->>MCS: 3 hits (ids, score)
    MCS->>PE: 4 isAllowed(user, assetIds)?
    PE-->>MCS: 5 allow/deny list
    MCS->>PG: 6 SELECT assets WHERE id IN allowedIds
    PG-->>MCS: 7 rows
    MCS-->>UI: 8 JSON results
    MCS-->>CW: 9 AuditEvent(type="SEARCH", actor=user, query="sales_data*")
```

### 4.3 Lineage Exploration

```mermaid
sequenceDiagram
    autonumber
    participant UI as Web UI
    participant MCS as Metadata Catalog Service
    participant NP as Neptune

    UI->>MCS: 1 GET /assets/{id}/lineage?depth=2
    MCS->>NP: 2 Gremlin query (outE,inV .. depth=2)
    NP-->>MCS: 3 subgraph JSON
    MCS-->>UI: 4 lineage graph
```

> **Note**: MCS enforces access checks *before* returning any lineage node not owned by the caller's domain.

---

## 5. Deployment Footprint & Scaling

| Environment           | Topology                                                                          |
| --------------------- | --------------------------------------------------------------------------------- |
| **Prod**              | 3 × Fargate tasks (OpenMetadata), Aurora PostgreSQL cluster. (Or pachaget in k8s) |
| **Dev**               | Single Docker Compose (`om + pg + os`)                                            |
| **Disaster Recovery** | Cross‑Region read replica + nightly S3 snapshot of JSON export                    |

---

## 6. Failure Handling

| Failure                    | Behaviour                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| **DB write fails**         | API returns 5xx; Enrichment retries (at‑least‑once).                                        |
| **OpenSearch unreachable** | Catalog write still commits; hook retries with exponential back‑off until index consistent. |
| **Neptune unavailable**    | Lineage edge persistence is retried; asset remains browsable.                               |
