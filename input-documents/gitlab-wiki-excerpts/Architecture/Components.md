# Components

The Project Lion Platform is composed of several key components that work together to discover, catalog, govern, and broker access to data.

## Edge Connector

- **Purpose:** A lightweight agent deployed in the customer's cloud VPC that monitors data sources and sends metadata events to the Project Lion Platform.
- **How it talks to others:**
  - Reads data from customer data stores (S3, relational DBs, event streams).
  - Sends metadata event bundles to the Ingestion Gateway.
- **Key Tech:** Stateless side-car, Lambda, or Fargate task.

## Ingestion Gateway

- **Purpose:** Provides a secure entry point for all metadata events coming from Edge Connectors into the Project Lion Platform.
- **How it talks to others:**
  - Receives event bundles from Edge Connectors (REST).
  - Validates, de-duplicates, and forwards events to the Metadata Catalog Service (typically via an internal event stream like Kinesis).
- **Key Tech:** Node.js/Fastify/Express, Kinesis, SQS.

## Enrichment & Indexer

- **Purpose:** Enriches raw ingestion events and immediately writes the
  canonical asset to **OpenMetadata** (REST API) and **OpenSearch** ( `_bulk` ).
- **How it talks to others:**
  - Consumes batches from **Kinesis `events_raw`**.
  - Calls **OpenMetadata API** to upsert assets, tags, lineage.
  - Sends the same JSON into **OpenSearch** for sub-second discovery.
- **Key Tech:** AWS Lambda.

## Metadata Catalog Service

- **Purpose:** The central repository and source of truth for all discovered metadata, including schemas, tags, lineage, and policies.
- **How it talks to others:**
  - Receives enriched events from the Ingestion Gateway stream.
  - Persists metadata to its underlying database (e.g., Aurora PostgreSQL).
  - Provides metadata to the Search & Discovery index, Lineage Graph, and Policy Engine.
  - Serves metadata to UIs, CLIs, and SDKs via its API.
- **Key Tech:** PostgreSQL, OpenMetadata, OpenSearch, Neptune.

## Search & Discovery

- **Purpose:** Enables users to easily find and understand data assets through a powerful search interface with full-text capabilities and faceted filtering.
- **How it talks to others:**
  - Receives metadata updates from the Metadata Catalog Service.
  - Provides search query capabilities to UIs, CLIs, and SDKs.
- **Key Tech:** OpenSearch.

## Policy Engine

- **Purpose:** Enforces data governance rules and policies, determining who can access what data under which conditions.
- **How it talks to others:**
  - Hydrates rules from policy definitions stored/linked in the Metadata Catalog.
  - Evaluates access requests from UIs/CLIs/SDKs (often via the Access Broker or other services).
  - Instructs the Access Broker on whether to grant or deny access.
- **Key Tech:** OPA / Cedar (Open Policy Agent).

## Lineage Graph

- **Purpose:** Captures and visualizes the relationships between data assets, showing how data is created, transformed, and consumed across platform.
- **How it talks to others:**
  - Receives lineage information as metadata from the Ingestion Gateway and Metadata Catalog Service.
  - Provides lineage data to UIs, CLIs, and SDKs for visualization and analysis.
- **Key Tech:** Graph database (e.g., Amazon Neptune), OpenLineage standard.

## Access Broker

- **Purpose:** Securely provides time-limited access to data assets once the Policy Engine has authorized a request, without copying the data itself.
- **How it talks to others:**
  - Receives authorization decisions from the Policy Engine.
  - Generates signed URLs, temporary credentials, or proxies for direct access to customer data stores.
  - Returns these access mechanisms to the requesting UI/CLI/SDK.
- **Key Tech:** AWS STS, S3 presigned URLs, JDBC authentications.

## UI/CLI/SDKs

- **Purpose:** Provide human and programmatic interfaces for interacting with all aspects of the Project Lion Platform.
- **How it talks to others:**
  - Interact with the Search & Discovery service for finding data.
  - Fetch detailed metadata and lineage from the Metadata Catalog Service and Lineage Graph.
  - Send access requests that are evaluated by the Policy Engine and fulfilled by the Access Broker.
  - Configure connections, view audit logs, and manage policies.
- **Key Tech:** React/Next.js (UI), TypeScript/Python (SDKs), GraphQL.
