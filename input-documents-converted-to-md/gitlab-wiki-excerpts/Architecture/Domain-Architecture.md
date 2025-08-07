The Project Lion must handle multiple clients, several product lines, and strict information‑classification rules.

---

## OpenMetadata Domain Model

Based on the [Architectural decision](/Architecture-Decisions/ADR-002-adopt-core-metadata-catalog) to adopt OpenMetadata as our cataloging solution we will use reuse their domain model. OpenMetadata have 'Domain' entity that sits above datasets, dashboards, pipelines, etc. It is deliberately simple:

| Level | Purpose | OpenMetadata entity | Key attributes |
|-------|---------|--------------------|----------------|
| **Domain** | Highest logical boundary (business line, portfolio, customer) | `Domain` | `name`, `owner`, `description`, `tags` |
| **Sub‑Domain** | Nested partition within a domain | `Domain` (child) | inherits parent, can override `owner` or `policy` |
| **Data Product** | Cohesive set of assets that deliver value | `DataProduct` | rich docs, owners, delivery SLA |
| **Asset container** | Physical bucket, folder, or table | `Container` / `Table` | native lineage, storage path |
| **Service** | API or pipeline that exposes or transforms data | `Service` | type, connection, lineage edges |

OpenMetadata allows **unlimited nesting of domains**, so we can model Company → Program → Project if needed. Domains own policies, glossary terms, and default classifications; children inherit unless overridden. Custom properties and classifications attach at any level.

---

## What is the Project Lion Domain Model?

![domain_model](uploads/1e42a18355f8960b5430ab2ee8dd5031/domain_model.png)

Source Draw.io XML chart: [omd-relationships.drawio.xml](uploads/c0486a27a10ca4ae4fca6b883abfd92f/omd-relationships.drawio.xml)

How Project Lion partitions data:

* **Organisation Unit (OU)** - top‑level client or internal business line.
* **Sub OU** - program, contract, or environment (dev, prod).
* **Domain 1, Domain 2 ...** - functional or product area inside a Sub OU, often aligned with a sensor or dataset family.
* **Data Product** - a release‑ready bundle that analysts or downstream systems consume.
* **Containers** - S3 prefixes or Azure paths that store raw assets and mapping specs.
* **Supporting Services** - GeoSpatial APIs, tiling engines, QC test suites.
* **ETL / Ingestion** - normalises geometry, computes hashes, enriches metadata, writes to catalog.

## Example on how to extend Project Lion with new properties 

Project Lion adds two domain‑wide custom properties:

```json
{
"geoEnabled": true,
"classification": { "ICSM": "Official Use Only" }
}
```

At asset level:

```json
{
"location": { "geom": "POINT(-76 39)" },
"classification": { "CUI": "NOFORN" }
}
```

These are implemented as OpenMetadata custom properties, no schema patching.

---

## Mapping OpenMetadata and Project Lion

| Project Lion concept | OpenMetadata entity | Notes |
|----------------------|---------------------|-------|
| **OU** | `Domain` (root) | One per client or internal BU. |
| **Sub OU** | `Domain` (child) | Hierarchical; can nest further. |
| **Domain 1 / 2** | `Domain` (grand‑child) | Optional layer if we need three tiers. |
| **Data Product** | `DataProduct` | Owns docs, owners, SLAs. |
| **Container (Assets)** | `Container` (Fileset) | Physical storage, inherits tags. |
| **Container (Mappings)** | `Container` | Stores schema or CRS mapping files. |
| **GeoSpatial API** | `Service` (Pipeline or Custom HTTP) | Registers lineage from table → API. |
| **Datatable / Schema** | `Table`, `DatabaseSchema` | If data is materialized in RDS/PostGIS. |
| **ETL Pipeline** | `IngestionPipeline` | Ingestion Pipeline. |
