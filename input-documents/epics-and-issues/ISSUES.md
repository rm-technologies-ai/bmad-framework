## GitLab Issues - atlas-datascience/lion

### #44: Validate node-gdal-async bundled gdal version is approved software
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-25T16:06:33.204Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/44

One potential constraint of government environments is software scanning. If the bundled gdal of node-gdal-async is not approved software, it may require us to port the edge connector down the line to another language where we have more control over our biggest dependency for extraction (gdal).

---
### #43: Support GeoPDF Extraction with Python Lambda
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-25T16:04:07.250Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/43

# Problem:

Geopdf format embedded metadata exists is defined in multiple specifications. For each, specifications spread components of a CRS across 1 - N references, These references can be formatted in N ways. CRS is just one piece of metadata we may be interested in. 

The bundled gdal binary (our only option for lambda deployments), does not include the pdf driver required to parse geopdf metadata.

See:

https://github.com/mmomtchev/node-gdal-async?tab=readme-ov-file#using-in-amazon-linux-lambdas

https://github.com/mmomtchev/node-gdal-async/issues/230

Several approaches were discussed: 

* Node EC2 with custom GDAL
* eliminating/narrowing geopdf support
*  Porting the edge connector to python
* **Separate lambda for geo-pdf processing** 

**Solution**:

Create a lambda that will be invoked by the edge connector to handle the geo-pdf of metadata parsing.

---
### #42: Extend Enrichment Lambda to upsert Containers in OpenMetadata
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-22T14:11:37.073Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/42

The Enrichment service must turn each Kinesis record into a **Container** entity in OpenMetadata so downstream search, lineage, and policy flows work. Containers capture storage provider, region, lifecycle, and custom tags and map directly to the OpenMetadata `Container` entity.

Enhance the existing **Kinesis Receiver Lambda** by:

1. Parsing each event.
2. Calling **POST `/api/v1/containers`** (alias `createOrUpdateContainer`) when the container does not exist https://docs.open-metadata.org/swagger.html#operation/createOrUpdateContainer.
3. Calling **PATCH `/api/v1/containers/{id}`** (alias `patchContainer_1`) to add/update **custom properties** and tags defined in the schema (e.g. storageClass, region, geospatial) https://docs.open-metadata.org/swagger.html#operation/patchContainer_1.


## Definition of Done

* `npm run lint`, `npm run typecheck` pass.
* Unit tests coverage for the new client and handler.
* Local integration test against **OpenMetadata quick-start** shows a created container (screenshot in PR).


## Acceptance Criteria

| # | Scenario           | Success Condition                                                                                          |
| - | ------------------ | ---------------------------------------------------------------------------------------------------------- |
| 1 | New container      | Lambda receives record with bucket `my-data-bucket`, sends POST, receives `200/201`, logs `action=create`. |
| 2 | Existing container | Lambda sends POST, server returns `200 Updated`, logs `action=update`.                                     |
| 3 | Custom props       | PATCH request adds `storageClass`, `region`, `encryptionStatus`, `geospatial`, etc. from schema.                               |
| 4 | Error handling     | 5xx responses retried 3 Ã exponential back-off; still failing â push to DLQ.                               |
| 5 | Metrics hook       | Emits `ContainersCreated`, `ContainersUpdated`, `ContainerError`                  |


## Quick-Start Skeleton

```ts
import axios, { AxiosInstance } from 'axios';

export class OMClient {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.OM_BASE_URL,
      headers: { 'Authorization': `Bearer ${process.env.OM_API_TOKEN}` }
    });
  }

  async upsertContainer(dto: ContainerDTO): Promise<string> {
    const res = await this.api.post('/api/v1/containers', dto);
    return res.data.id;        // 200 or 201
  }

  async patchContainer(id: string, patch: Partial<ContainerDTO>) {
    await this.api.patch(`/api/v1/containers/${id}`, patch);
  }
}
```

```ts
for (const rec of events) {
  const dto = mapToContainerDTO(rec.containerMetadata); // helper maps schema â OM
  const id = await om.upsertContainer(dto);
  await om.patchContainer(id, dto.customProperties);
}
```

### Mapping Rules

| Schema field                               | OM Container field            |
| ------------------------------------------ | ----------------------------- |
| `containerIdentifier.bucketName`           | `name`                        |
| `storageProvider`                          | `service.type`                |
| `location.region`                          | `service.location`            |
| `storageClass`, `encryptionStatus`, `tags` | `customProperties`            |
| `containerIdentifier.accountId`            | `owner` (placeholder for MVP) |


## Environment Variables

| Name           | Example                        | Purpose                                 |
| -------------- | ------------------------------ | --------------------------------------- |
| `OM_BASE_URL`  | `https://metadata.example.com` | OpenMetadata server                     |
| `OM_API_TOKEN` | `xyz123`                       | Bearer token with `ContainerAdmin` role |

---
### #41: Instrument Ingestion Gateway Lambda with core CloudWatch metrics & alarms
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Adam Galyoon
- **Labels**: None
- **Created**: 2025-07-22T13:57:34.458Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/41


Add metric emission to the existing Lambda, create one alarm per critical metric, and surface a lightweight dashboard.


## Definition of Done

* `npm run lint`, `npm run typecheck` pass.
* Unit tests cover metric emission.

## Acceptance Criteria

1. **Metric Emission**

   * Use **AWS Lambda Powertools for TypeScript** (`metrics.addMetric`).
   * Namespace: `Lion/IGW`.
   * Emit metrics once per Lambda invocation (avoid per-record cost).

2. **Metrics (MVP list)**

   | Name                | Unit         | Notes                                                                |
   | ------------------- | ------------ | -------------------------------------------------------------------- |
   | `EventsReceived`    | Count        | Total records the handler attempted.                                 |
   | `EventsPublished`   | Count        | Records successfully written to Kinesis.                             |
   | `PublishLatencyMs`  | Milliseconds | Time from handler entry to `PutRecords` response. Emit as Histogram. |
   | `PublishErrorCount` | Count        | Records that still failed after all retries.                         |
   | `EventDrop`         | Count        | Records intentionally dropped (back-pressure, unrecoverable error).  |
   | `BatchSize`         | Count        | Size of batch sent to Kinesis.                                       |


3. **Dashboard**

   * Single CloudWatch dashboard with eight graphs: six custom metrics plus built-in Lambda `Duration` and `Errors`.


## Quick-Start Skeleton

```ts
// libs/igw/src/infra/metrics/metric-helper.ts
import { Metrics, MetricUnits } from '@aws-lambda-powertools/metrics';

export const igwMetrics = new Metrics({
  namespace: 'Lion/IGW',
  serviceName: 'ingestion-gateway',
});

export const recordMetrics = (result: PublishResult, latencyMs: number) => {
  igwMetrics.addMetric('EventsReceived', MetricUnits.Count, result.total);
  igwMetrics.addMetric('EventsPublished', MetricUnits.Count, result.success);
  igwMetrics.addMetric('PublishErrorCount', MetricUnits.Count, result.failure);
  igwMetrics.addMetric('PublishLatencyMs', MetricUnits.Milliseconds, latencyMs);
  igwMetrics.addMetric('BatchSize', MetricUnits.Count, result.total);
  if (result.dropped > 0) {
    igwMetrics.addMetric('EventDrop', MetricUnits.Count, result.dropped);
  }
};
```

Hook this helper at the end of `KinesisProducerService.publish()` (added in Kinesis Producer Ticket).

---

## Test Strategy

* **Unit:** Jest spies on `Metrics.prototype.addMetric` to assert correct names/units/values.
* **Integration:** Invoke Lambda in LocalStack, then query the CloudWatch stub to verify metrics surfaced.

---
### #40: Implement KinesisProducerHandler to push validated events to events-raw
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Adam Galyoon
- **Labels**: None
- **Created**: 2025-07-22T13:32:43.901Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/40

The Ingestion Gateway must take **Edge Connector events** (JSON) and forward each record into the raw Kinesis stream so downstream services can enrich and index the metadata.

## Scope

Create a service that:

* Accepts an array of pre-validated `IngestEvent` objects (one per extracted file).
* Publishes the array to **Kinesis Data Streams** `events-raw` using `PutRecords`.
* Handles partial failures and retries within Kinesis limits.


## Edge Connector Payload Schema (context for validation)

The Gateway receives a JSON body that looks like:

```jsonc
{
  "batchIdempotencyKey": "batch_20241215_142030_abc123",       // ensures batch-level dedupe
  "batchTimestamp": "2024-12-15T14:20:30Z",
  "batchSize": 3,
  "records": [
    {
      "correlationId": "3d3d6f1e-...",                          // trace across services
      "recordProcessingStatus": "Successful",
      "...": "other metadata"
    }
  ]
}
```

Key fields are defined in the schemas delivered by the Edge Connector:

* **Batch keys** â `batchIdempotencyKey`, `batchTimestamp`, `records[]`.
* **Record keys** â `correlationId` and `recordProcessingStatus`.

The existing controller validates the full batch against these schemas and flattens each `records[]` element into an `IngestEvent`.


## `IngestEvent` interface (used by this handler)

```ts
export interface IngestEvent {
  idempotencyKey: string;        // batchIdempotencyKey + index
  tenantId: string;              // derives from batchTenantId or auth context
  datasetId: string;             // logical dataset in Project Lion
  payload: ExtractorRecord;      // exact extraction record JSON
  timestamp: string;             // batchTimestamp
}
```

## Definition of Done

* `npm run lint`, `npm run typecheck` pass.
* **â¥ 50 %** line coverage on new unit tests (`npm test`).
* LocalStack integration test proves a successful `PutRecords` call (screenshot/link in PR).


## Acceptance Criteria

1. **Handler contract**

   ```ts
   publish(events: IngestEvent[]): Promise<PublishResult>;
   ```

   `PublishResult` returns per-record success / failure info.

2. Partition key is **`${tenantId}-${datasetId}`** to preserve order per dataset.

3. Batch meets Kinesis limits (â¤ 500 records, â¤ 5 MB).

4. On partial failure: retry failed records up to **3Ã exponential back-off**, then throw `PublishError`.

6. Unit tests cover happy path, throttling retry, and hard failure.

## Environment Variables

| Name             | Example      | Notes                     |
| ---------------- | ------------ | ------------------------- |
| `KINESIS_STREAM` | `events-raw` | Already in SSM Parameter. |
| `AWS_REGION`     | `us-east-1`  | Default region.           |

---
### #1: Publish Schema and Types package (lion/schema)
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-16T17:11:01.756Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/schemas/-/issues/1

Now that the schema repo is more defined, lets move type compilation (currently in edge-connector), generate types using the utility. And publish the schema repo as a package to our registry

Success Criteria

Exposes JSON for import 

Exposes type declaration files for import

---
### #39: Publish Schema and Types package (lion/schema)
- **State**: closed
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-16T17:11:01.756Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/39

Now that the schema repo is more defined, lets move type compilation (currently in edge-connector), generate types using the utility. And publish the schema repo as a package to our registry

Success Criteria

Exposes JSON for import 

Exposes type declaration files for import

---
### #38: Implement Process Flow for Edge Connector
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Ryan Cross
- **Labels**: None
- **Created**: 2025-07-16T17:08:59.602Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/38

The skeleton control flow is very tightly coupled and does not implement graceful error handling or processing of events. Create the external control flow that will manage the structure defined in this diagram:

![image.png](/uploads/b12ea6e91c3085a5f06e2025a4e6940b/image.png){width=591 height=382}

---
### #1: Pipeline for Typescript/NodeJS
- **State**: opened
- **Author**: Gregory Bosch
- **Assignee**: Alain Atemnkeng
- **Labels**: None
- **Created**: 2025-07-14T19:38:41.176Z
- **Web**: https://gitlab.com/atlas-datascience/lion/cicd/catalog/pipelines/-/issues/1

Development teams need a defined pipeline for evaluating Typescript/NodeJs code.

Success Criteria:
- Pipelines must utilize Gitlab Components strategy.
- Pipeline must build the application utilizing `node build` script contained within package.json
- Pipeline must run unit tests and produce code coverage that is integratabtle with Gitlab using `npm run test:cov`
- Pipeline must run linter using `npm run lint`
- Pipeline must run SAST and produce results that are published to Gitlab Security and Vulnerability dashboard
- Pipeline must run Secrets detection
- Pipeline must run Dependancy Checks
- Pipeline must produce CycloneDx compatible SBOM that can be published to Gitlab Security and Vulnerability dashboard
- NodeJs 22 must be used for the pipeline baseline
- Pipelines should be configurable to support more than one version of NodeJs
- Container pipeline must be integratabtle but only run container jobs when needed and jobs only run once dependencies have been met.

---
### #4: S3 Event Generator - Enqueue and Capture
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: John Mema
- **Labels**: Under Review
- **Created**: 2025-07-14T14:54:28.330Z
- **Web**: https://gitlab.com/atlas-datascience/lion/local-environment/-/issues/4

Building upon the events generated from the S3 operations in part one. Create mechanisms to capture all S3 events triggered (via SNS) from the test bucket to an SQS (Simple Queue System). Then build a script to receive and save these SQS Records. So that we can replay them for integration/end-to-end testing.

---
### #1: Dependency Dashboard
- **State**: opened
- **Author**: RENOVATE-RUNNER_TOKEN
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-12T02:41:45.249Z
- **Web**: https://gitlab.com/atlas-datascience/lion/test-project/-/issues/1

This issue lists Renovate updates and detected dependencies. Read the [Dependency Dashboard](https://docs.renovatebot.com/key-concepts/dashboard/) docs to learn more.

## Open

These updates have all been created already. Click a checkbox below to force a retry/rebase of any.

 - [ ] <!-- rebase-branch=renovate-aws-6.x -->[Update Terraform aws to v6](!2)

## Detected dependencies

<details><summary>gitlabci</summary>
<blockquote>

<details><summary>.gitlab-ci.yml</summary>


</details>

</blockquote>
</details>

<details><summary>terraform</summary>
<blockquote>

<details><summary>main.tf</summary>

 - `aws ~> 5.0`

</details>

</blockquote>
</details>

---
### #1: Dependency Dashboard
- **State**: opened
- **Author**: RENOVATE-RUNNER_TOKEN
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-11T12:39:13.272Z
- **Web**: https://gitlab.com/atlas-datascience/lion/renovate-runner/-/issues/1

This issue lists Renovate updates and detected dependencies. Read the [Dependency Dashboard](https://docs.renovatebot.com/key-concepts/dashboard/) docs to learn more.

## Awaiting Schedule

These updates are awaiting their schedule. Click on a checkbox to get an update now.

 - [ ] <!-- unschedule-branch=renovate-lock-file-maintenance -->chore(deps): lock file maintenance

## Open

These updates have all been created already. Click a checkbox below to force a retry/rebase of any.

 - [ ] <!-- rebase-branch=renovate-conventional-changelog-conventionalcommits-9.x -->[chore(deps): update dependency conventional-changelog-conventionalcommits to v9](!2)
 - [ ] <!-- rebase-branch=renovate-major-semantic-release-monorepo -->[chore(deps): update semantic-release monorepo (major)](!4) (`@semantic-release/gitlab`, `semantic-release`)
 - [ ] <!-- rebase-branch=renovate-ghcr.io-renovatebot-renovate-41.x -->[feat(deps): update ghcr.io/renovatebot/renovate docker tag to v41](!5)
 - [ ] <!-- rebase-branch=renovate-renovate-renovate-41.x -->[feat(deps): update renovate/renovate docker tag to v41](!6)
 - [ ] <!-- rebase-all-open-prs -->**Click on this checkbox to rebase all open MRs at once**

## Detected dependencies

<details><summary>gitlabci</summary>
<blockquote>

<details><summary>templates/renovate.gitlab-ci.yml</summary>


</details>

<details><summary>templates/renovate-dind.gitlab-ci.yml</summary>


</details>

<details><summary>templates/renovate-config-validator.gitlab-ci.yml</summary>


</details>

</blockquote>
</details>

<details><summary>npm</summary>
<blockquote>

<details><summary>package.json</summary>

 - `@semantic-release/gitlab 12.1.1`
 - `conventional-changelog-conventionalcommits 7.0.2`
 - `prettier 3.6.2`
 - `semantic-release 22.0.12`

</details>

</blockquote>
</details>

<details><summary>regex</summary>
<blockquote>

<details><summary>README.md</summary>


</details>

<details><summary>templates/renovate-config-validator.gitlab-ci.yml</summary>

 - `ghcr.io/renovatebot/renovate 37.440.7@sha256:1ee424e0ed4d8e64e5bb2d442d6bc72b3809bb9d0cf804f4b7180caa47d6002a`

</details>

<details><summary>templates/renovate-dind.gitlab-ci.yml</summary>

 - `renovate/renovate 37.440.7@sha256:42bedb4c35c5403faf50e82283f4f92f902addf9986a1f91281d9aa25d8a4a32`

</details>

<details><summary>templates/renovate.gitlab-ci.yml</summary>

 - `ghcr.io/renovatebot/renovate 37.440.7@sha256:1ee424e0ed4d8e64e5bb2d442d6bc72b3809bb9d0cf804f4b7180caa47d6002a`

</details>

</blockquote>
</details>

---
### #1: Establish Environment Networks
- **State**: opened
- **Author**: Gregory Bosch
- **Assignee**: Unassigned
- **Labels**: Backlog
- **Created**: 2025-07-10T15:29:27.273Z
- **Web**: https://gitlab.com/atlas-datascience/lion/infrastructure/aws/environment-networks/-/issues/1

Create the IaaC in Terraform that can be utilized through CICD to build out each of the environment networks.

Components:
- IaaC for Network in Terraform

Acceptance Criteria:
- IaaC reflects the agreed to design of the environment networks.
- Environment networks leverage configured route rules and peering to integrate VPCs across accounts.
- IaaC is validated and deployed through automation.

---
### #2: Establish Terraform Templates for Master Network
- **State**: opened
- **Author**: Gregory Bosch
- **Assignee**: Unassigned
- **Labels**: In Progress
- **Created**: 2025-07-10T15:26:29.935Z
- **Web**: https://gitlab.com/atlas-datascience/lion/infrastructure/aws/master-network/-/issues/2

Create the IaaC in Terraform that can be utilized through CICD to build out the network in the Master Account.

Components:
- IaaC for Network in Terraform

Acceptance Criteria:
- IaaC reflects the agreed to design of the master network.
- IaaC is validated and deployed through automation.

---
### #1: Master Network Design
- **State**: opened
- **Author**: Gregory Bosch
- **Assignee**: Oneil Lespierre
- **Labels**: In Progress
- **Created**: 2025-07-10T15:21:31.370Z
- **Web**: https://gitlab.com/atlas-datascience/lion/infrastructure/aws/master-network/-/issues/1

Need to develop a master network design that demonstrates a multi VPC, multi account strategy.

Components:
- Architecture Design documentation
- - network diagram
- - supporting documents defining concepts and strategy
Acceptance Criteria:
- Ensures minimal public exposure to private resources.
- Ensures AWS network protection mechanisms are employed.
- Provides singular access to AWS private VPC endpoints across all accounts .
- Configuration is pluggable with respect to environment accounts supporting development, stage and production.

---
### #37: Example-Datasets S3 Event Generator - Event Creation
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: John Mema
- **Labels**: Under Review
- **Created**: 2025-07-10T00:08:56.122Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/37

As a user I would like to be able to perform end-to-end testing of the Lion project with a robust, production-like event dataset. Step one is to generate those events for capture.

**Success Criteria:**

* Add a command to stand up a s3 Bucket: **_LionTestData_** in the LocalEnvironment repo using localstack (hint: this has been done in the LocalEnvironment Repo)
* Create a Typescript script in LocalEnvironment that will upload all files from any subdirectory in example-datasets and POST them into a LocalStack s3 bucket
* Using the object keys from a successful post, perform PUTs to update (create new versions) objects with new metadata.
* Perform a COPY of each uploaded item to another location in the same bucket
* Perform a mix of DELETE, SOFT DELETE on those copies

---
### #2: Create documentation and deployment guides
- **State**: opened
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: Backlog
- **Created**: 2025-07-08T19:57:02.997Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/data-ingestion-enrichment/ingestion-gateway/-/issues/2

Write comprehensive documentation for the system.

**Deliverables:**

- API documentation
- Deployment guide
- Configuration reference
- Operational runbooks

**Acceptance Criteria:**

- All APIs documented
- Deployment automated
- Runbooks cover common scenarios

Estimate: 1 week

---
### #10: Create documentation and deployment guides
- **State**: closed
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-08T19:57:02.997Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/10

Write comprehensive documentation for the system.

**Deliverables:**

- API documentation
- Deployment guide
- Configuration reference
- Operational runbooks

**Acceptance Criteria:**

- All APIs documented
- Deployment automated
- Runbooks cover common scenarios

Estimate: 1 week

---
### #1: Initialize ingestion-gateway repository
- **State**: opened
- **Author**: Adam Galyoon
- **Assignee**: Adam Galyoon
- **Labels**: In Progress
- **Created**: 2025-07-08T18:12:00.184Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/data-ingestion-enrichment/ingestion-gateway/-/issues/1

Create repository and set up NestJS TypeScript project for both API Gateway and Enrichment Lambda functions.

**Tasks:**

- Create feature branch on the ingestion-gateway repository
- Initialize NestJS project with TypeScript
- Configure ESLint, Prettier, and git hooks
- ~~Set up Docker for local development~~ Separate Ticket
- ~~Create basic CI/CD pipeline~~ Separate Ticket
- Add environment configuration

**Acceptance Criteria:**

- Repository created and accessible
- NestJS project runs locally
- Linting and formatting work
- Project Structure matches that of the Edge Connector
- ~~Docker compose starts all dependencies~~ Separate Ticket
- ~~Basic pipeline runs tests~~

Estimate: 2 days

---
### #36: Initialize ingestion-gateway repository
- **State**: closed
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-08T18:12:00.184Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/36

Create repository and set up NestJS TypeScript project for both API Gateway and Enrichment Lambda functions.

**Tasks:**

- Create feature branch on the ingestion-gateway repository
- Initialize NestJS project with TypeScript
- Configure ESLint, Prettier, and git hooks
- ~~Set up Docker for local development~~ Separate Ticket
- ~~Create basic CI/CD pipeline~~ Separate Ticket
- Add environment configuration

**Acceptance Criteria:**

- Repository created and accessible
- NestJS project runs locally
- Linting and formatting work
- Project Structure matches that of the Edge Connector
- ~~Docker compose starts all dependencies~~ Separate Ticket
- ~~Basic pipeline runs tests~~

Estimate: 2 days

---
### #3: (Platform) Configure AWS resources using Infrastructure as Code
- **State**: opened
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: Backlog
- **Created**: 2025-07-08T18:10:35.432Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/data-ingestion-enrichment/ingestion-gateway/-/issues/3

Set up AWS infrastructure including API Gateway, Lambda functions, Kinesis stream, and Redis cluster.

**Components:**

- API Gateway for ingestion endpoint - separate task
- Lambda functions (Ingestion and Enrichment)
- Kinesis Data Stream
- ElastiCache Redis cluster
- IAM roles and policies
- CloudWatch logging - expand

**Acceptance Criteria:**

- IaC templates deploy successfully
- All resources properly configured
- Security groups set up
- IAM set up
- Monitoring enabled - expand

Estimate: 1 week

---
### #35: (Platform) Configure AWS resources using Infrastructure as Code
- **State**: closed
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-08T18:10:35.432Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/35

Set up AWS infrastructure including API Gateway, Lambda functions, Kinesis stream, and Redis cluster.

**Components:**

- API Gateway for ingestion endpoint - separate task
- Lambda functions (Ingestion and Enrichment)
- Kinesis Data Stream
- ElastiCache Redis cluster
- IAM roles and policies
- CloudWatch logging - expand

**Acceptance Criteria:**

- IaC templates deploy successfully
- All resources properly configured
- Security groups set up
- IAM set up
- Monitoring enabled - expand

Estimate: 1 week

---
### #4: Implement Ingest Gateway API
- **State**: opened
- **Author**: Adam Galyoon
- **Assignee**: Adam Galyoon
- **Labels**: Backlog
- **Created**: 2025-07-08T14:30:03.246Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/data-ingestion-enrichment/ingestion-gateway/-/issues/4


Create API structure with authentication, logging, and error handling middleware.

**Acceptance Criteria:**

- API that handles HTTP POST for edge connector events
   * HTTP request body will contain an array of events from the edge connector
   * HTTP body must be validated
   * All Requests and Responses are logged
   * All Error Responses align with applicable HTTP Codes
   * Content Validation Errors will return HTTP 400 Error Code
   * Correlation ID tracking Errors will return:
      - HTTP 409 if the request is replayed while still being processed
      - HTTP 422 if the key is reused for a different request
   * Valid Requests will return an HTTP 202 response as there is not guarantee of completed processing.
   * All validated events are written to the Kenisis stream for down stream processing.
- 30% code coverage has been met or exceeded for Unit Tests
- All unit tests pass
- There are no critical Linting errors

- ~~JWT authentication~~ - Make its own issue
- ~~Health check endpoint~~ - If Lambda this may not be appropriate.  
- ~~Rate limiting~~ - Handled by infrastructure / API Gateway

Estimate: 1 week

---
### #34: Implement base API with middleware
- **State**: closed
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-08T14:30:03.246Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/34

Create API structure with authentication, logging, and error handling middleware.

**Requirements:**

- JWT authentication
- Request/response logging
- Error handling
- ~~Health check endpoint~~
- ~~Rate limiting~~ - Handled by infrastructure / API Gateway
- Correlation ID tracking

**Acceptance Criteria:**

- Authentication works with JWT
- All requests logged
- Errors return consistent format

Estimate: 1 week

---
### #5: Implement Redis-based event deduplication
- **State**: opened
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: Backlog
- **Created**: 2025-07-08T14:29:48.961Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/data-ingestion-enrichment/ingestion-gateway/-/issues/5

Add Redis integration to prevent duplicate event processing using idempotency keys.

**Requirements:**

- Check and set operations
- Configurable TTL
- Circuit breaker for failures
- Batch deduplication
- Fallback behavior

**Acceptance Criteria:**

- Duplicates detected and rejected
- Redis failures handled gracefully
- Performance meets requirements

Estimate: 1 week

---
### #32: Implement Redis-based event deduplication
- **State**: closed
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: Backlog
- **Created**: 2025-07-08T14:29:48.961Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/32

Add Redis integration to prevent duplicate event processing using idempotency keys.

**Requirements:**

- Check and set operations
- Configurable TTL
- Circuit breaker for failures
- Batch deduplication
- Fallback behavior

**Acceptance Criteria:**

- Duplicates detected and rejected
- Redis failures handled gracefully
- Performance meets requirements

Estimate: 1 week

---
### #31: Create Kinesis publishing service
- **State**: opened
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-08T14:29:42.979Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/31

Build service to publish validated events to Kinesis with batching and retry logic.
Features:

Single and batch publishing

Automatic batching for performance

Retry with backoff

Dead letter queue

Partition key strategies

Acceptance Criteria:

Events published to Kinesis

Batching improves throughput

Failed events go to DLQ

Estimate: 1 week

---
### #6: Implement Kinesis Event Receiver
- **State**: closed
- **Author**: Adam Galyoon
- **Assignee**: John Mema
- **Labels**: In Progress
- **Created**: 2025-07-08T14:29:37.223Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/data-ingestion-enrichment/ingestion-gateway/-/issues/6

Lambda that consumes from Kinesis, enriches events, and applies business rules and writes record back to Open Metadata.

Create API structure with authentication, logging, and error handling middleware.

**Acceptance Criteria:**

- API that handles Kinesis Data Stream Events
   * All invoking events are logged
   * All errors are logged with appropriate log levels
   * Records are written to OpenMetadata.
- 30% code coverage has been met or exceeded for Unit Tests
- All unit tests pass
- There are no critical Linting errors

**Components:**

- Kinesis event processing
- Enrichment pipeline
- Business rules validation
- Error handling
- Metrics collection

Estimate: 1.5 weeks

---
### #30: Create Lambda to process Kinesis events
- **State**: closed
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-08T14:29:37.223Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/30

Build Lambda that consumes from Kinesis, enriches events, and applies business rules.

**Components:**

- Kinesis event processing
- Enrichment pipeline
- Business rules validation
- Error handling
- Metrics collection

**Acceptance Criteria:**

- Lambda processes events from Kinesis
- Enrichment adds required metadata
- Business rules enforced
- Failed events handled properly

Estimate: 1.5 weeks

---
### #7: Implement OpenMetadata client
- **State**: opened
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: Backlog
- **Created**: 2025-07-08T14:29:31.803Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/data-ingestion-enrichment/ingestion-gateway/-/issues/7

Create integration layer for OpenMetadata to store enriched metadata.

**Features:**

- Entity creation and updates
- Bulk operations
- Lineage management
- Error handling and retries
- Search functionality

**Acceptance Criteria:**

- Entities created in OpenMetadata
- Bulk ingestion works
- Lineage relationships stored
- Errors handled gracefully

Estimate: 2 weeks

---
### #29: Implement OpenMetadata client
- **State**: closed
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: Backlog
- **Created**: 2025-07-08T14:29:31.803Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/29

Create integration layer for OpenMetadata to store enriched metadata.

**Features:**

- Entity creation and updates
- Bulk operations
- Lineage management
- Error handling and retries
- Search functionality

**Acceptance Criteria:**

- Entities created in OpenMetadata
- Bulk ingestion works
- Lineage relationships stored
- Errors handled gracefully

Estimate: 2 weeks

---
### #8: Implement comprehensive tests
- **State**: opened
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-08T14:29:25.024Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/data-ingestion-enrichment/ingestion-gateway/-/issues/8

Create unit, integration, and load tests for all components.


**Scope:**

- Unit tests for all services
- Integration tests for workflows
- Load testing for performance
- Security testing

**Acceptance Criteria:**

- Code coverage above 80%
- Integration tests pass
- Load tests meet performance targets

Estimate: 1.5 weeks

---
### #28: Implement comprehensive tests
- **State**: closed
- **Author**: Adam Galyoon
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-07-08T14:29:25.024Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/28

Create unit, integration, and load tests for all components.


**Scope:**

- Unit tests for all services
- Integration tests for workflows
- Load testing for performance
- Security testing

**Acceptance Criteria:**

- Code coverage above 80%
- Integration tests pass
- Load tests meet performance targets

Estimate: 1.5 weeks

---
### #27: Deploy to sandbox
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-30T16:03:16.192Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/27

Apply the module against the shared dev payer account (sandbox or dev) and run a manual smoke test via AWS CLI to issue a pre-signed S3 URL through the Access Broker.

**Acceptance criteria**

- curl -XPOST /v1/issue returns signed URL that downloads successfully (we do not have Access Broker yet, may be create Mock script with AWS CLI to request URL).
- CloudTrail shows AssumeRole event with correct ExternalId.

---
### #26: CI
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-30T16:02:33.877Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/26

Add CI to run tflint, tfsec and the tests from ticket #25 .

**Acceptance criteria**

- Workflow triggers on paths: ['modules/sts_cross_account/**'].
- Jobs: setup-terraform, tflint, tfsec, test.
- Fails the PR on any lint or test error.
- Uses GitLab OIDC to pull short-lived AWS creds (no static keys).

---
### #25: Test assume-role
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-30T16:02:10.089Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/25

Write test script (Terratest?) that deploys the module in a frash account, then calls aws sts assume-role and checks the credentials expire as expected.

**Acceptance criteria**

- Test spins up module via terraform.InitAndApply.
- AssumeRole call succeeds and returns JSON creds.
- Script waits until expiration - now < 60s and verifies expiry.
- Test fails fast if permissions mismatch (AccessDenied).
- Test tears down resources in defer block.

---
### #24: Attach least-privilege policies per datastore
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-30T16:01:24.538Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/24

Add conditional blocks so the module can attach S3, RDS, or other datasource (in the future) policies based on the datastore variable, keeping each as small as possible.

**Acceptance criteria**

- Separate JSON policies stored under policies/.
- for_each over var.datastores creates only necessary attachments.
- S3 policy limits resources to ${var.bucket_arns}/*.
- RDS auth policy uses rds-db:connect with ARN pattern for RDS Proxy.
- Policy ARNs shown in outputs.

---
### #23: Implement IAM role and ExternalId input
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-30T16:00:52.229Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/23

Add the actual aws_iam_role, trust policy JSON and aws_iam_policy resources inside the module, wiring them to module variables.

**Acceptance criteria**

- Role trust policy contains correct Principal and Condition StringEquals sts:ExternalId.
- max_session_duration hard-caps at 3600s.
- Outputs updated test to match created ARN.
- terraform plan with no warnings.

---
### #22: Terraform module
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-30T16:00:39.646Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/22

Create the modules/sts_cross_account directory with variables, outputs. Include role_name, external_id, allowed_actions, and tags variables.

**Acceptance criteria**

- main.tf, variables.tf, outputs.tf, README.md.
- Module passes terraform validate with empty/placeholder inputs.
- Outputs expose role_arn and external_id.
- README shows example usage snippet.
- Pre-commit hook runs terraform fmt -check.

---
### #21: Draft trust and permission policy
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-30T16:00:25.367Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/21

Design the IAM trust and inline permission policies that will live in each customer account. Focus on sts:AssumeRole trust with the Access Broker ARN and a unique ExternalId, plus a minimal action set per datastore type.

**Acceptance criteria**

- Trust policy limits Principal to the Access Broker role ARN.
- Condition block enforces customer-specific ExternalId.
- Permissions allow only scoped read/write (e.g., s3:GetObject, rds-db:connect).
- Session duration default set to 900s.

---
### #20: Edge Connector Terraform deploy template
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-30T15:34:15.592Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/20

**Edge Connector Terraform deploy template similar to **[**DataDog**](https://docs.datadoghq.com/integrations/guide/)**:**

* Lambda Function connected to S3 events
* SQS for buffering
* IAM Role and Policy with defined access
* Secret Manager credentials for JWT
* CloudWatch Log Group for logs

**Lambda Configurations:**

* GATEWAY_URL - Ingestion Gateway HTTPS endpoint
* TENANT_ID - Tenant scoping + idempotency key salt
* JWT_SECRET_ARN - Secrets Manager ARN for JWT
* MAX_RETRY_ATTEMPTS - max retries before DQL
* INCLUDE_PREFIXES - S3 include prefixes, comma separated
* EXCLUDE_PREFIXES - S3 exclude prefixes, comma separated
* ENABLE_GZIP - enable compression
* LOG_LEVEL - Log level for debugging

---
### #3: Add Flyway to local development environment
- **State**: opened
- **Author**: Robert Price
- **Assignee**: Robert Price
- **Labels**: None
- **Created**: 2025-06-30T13:37:24.029Z
- **Web**: https://gitlab.com/atlas-datascience/lion/local-environment/-/issues/3

Need to change local development environment to use Flyway to manage Postgres data structures. Flyway will be used to version Postgres database changes so that we can better track Postgres changes and rollback changes if needed. Flyway is used by OpenMetadata so using Flyway will allow us to use a similar database versioning scheme to keep database changes consistent.

https://documentation.red-gate.com/flyway/getting-started-with-flyway/quickstart-guides/quickstart-docker

---
### #19: Validate exif meets threshold for necessary geospatial extraction.
- **State**: closed
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-27T18:37:52.747Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/19

Robert has identified from this exhaustive list of supported filetypes the important ones to test, and has create associated datasets for that in example-datasets github repo.

```
        const gdalExtensions = [
            '.pdf', '.toc', '.ovr', '.nitf', '.ntf', '.vrt', '.tif', '.tiff', '.png', '.aux',
            '.i4a', '.i4c', '.i41', '.i21', '.i23', '.i1a', '.i11', '.i12', '.i13', '.i14',
            '.i15', '.i16', '.dt0', '.dt1', '.dt2', '.lf1', '.lf2', '.lf3', '.lf4', '.lf5',
            '.lf6', '.lf7', '.ln2', '.ln3', '.ln4', '.tf2', '.tf3', '.tf4', '.tf5', '.tf6'
        ];

        // GeoPDF files
        const geoPdfExtensions = ['.pdf'];

        // Picture files that can have geo data
        const picExtensions = ['.jpeg', '.jpg'];

        // Shapefile and vector formats
        const vectorExtensions = ['.shp'];

        // VPF files (Vector Product Format)
        const vpfExtensions = ['lht', 'dht', 'grt', 'dqt', 'cat', 'lat'];
```

Compare and contrast using exifr, (or whatever other node libraries may be appropriate) with gdal. We should be able to view the two side by side.

Minimum required data:
- Geometry data
- Coordinate System data

---
### #18: Replace Placeholder AssetEvent with JSON Schema Output Model
- **State**: closed
- **Author**: Ryan Cross
- **Assignee**: Ryan Cross
- **Labels**: None
- **Created**: 2025-06-27T17:26:04.255Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/18



---
### #1: Develop Terraform Codebase for Automated AWS Multi-Account Access Management
- **State**: opened
- **Author**: Alain Atemnkeng
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-25T15:26:31.277Z
- **Web**: https://gitlab.com/atlas-datascience/lion/infrastructure/aws/access-manager/-/issues/1

We need to develop a Terraform-based codebase responsible for managing and granting access across all AWS accounts within our organization. This includes defining who has access to which accounts, what roles or permissions they have, and which groups they belong to.

This project will include an automation pipeline, enabling faster and more consistent application of changes. Appropriate security controls must be in place to ensure only authorized personnel can trigger or approve the pipeline.

This codebase will serve as the single source of truth for AWS account access and permissions.

**Acceptance Criteria:**

	1.	**Terraform Codebase:**
	
	â¢	A standalone Terraform project exists for managing access across AWS accounts.
	â¢	Defines:
	â¢	All AWS accounts under management.
	â¢	Groups and users (via IAM Identity Center).
	â¢	Permission sets or IAM policies.
	â¢	Group-to-account assignments and permissions.
	â¢	Code structure supports easy onboarding and updates.

	2.	**Automation Pipeline:**
	â¢	A CI/CD pipeline is integrated (e.g., GitLab).
	â¢	The pipeline:
	â¢	Supports plan and apply stages.
	â¢	Enforces peer review and approval before apply is permitted.
	â¢	Limits execution to a secure environment (e.g., protected runners, access-controlled    credentials).
	â¢	Logs and artifacts are retained for auditing.

	3.	**Security & Governance:**
	â¢	Only authorized engineers (e.g., members of a devops-admins group) can trigger or approve pipeline executions.
	â¢	Role and permission assignments follow least-privilege principles.
	â¢	All access changes are version-controlled and auditable.
	â¢	Sensitive values (e.g., user emails) are stored securely.

	4.	**Documentation:**
	â¢	Includes a detailed README with:
	â¢	How the codebase works.
	â¢	How to add new users or groups.
	â¢	How to assign users to accounts and roles.
	â¢	How to run the pipeline or perform manual overrides if needed.
	â¢	A generated or manually maintained summary that includes:
	â¢	List of all AWS accounts.
	â¢	Defined groups and their descriptions.
	â¢	User/group-to-account mappings.
	â¢	Permission sets or policies per group/account.

	5.	**Testing & Validation:**
	â¢	Access provisioning is tested in a non-production environment.
	â¢	At least one access change is deployed through the pipeline as part of ticket closure.

---
### #1: Develop Terraform Codebase for AWS Account Creation and Organization Integration
- **State**: opened
- **Author**: Alain Atemnkeng
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-25T14:58:56.703Z
- **Web**: https://gitlab.com/atlas-datascience/lion/infrastructure/aws/aws-account-creation/-/issues/1

We need to develop a secure Terraform codebase that enables the creation of new AWS accounts and automatically adds them to our existing AWS Organization. This codebase should also support assigning baseline organizational-level permissions and configurations to the newly created accounts as needed (e.g., SCPs, IAM Identity Center permission sets, etc.).


Security Requirement:
This codebase should include an automation pipeline for automation. 

Acceptance Criteria:
	1.	A Terraform codebase exists that:
	â¢	Creates a new AWS account programmatically using the AWS Organizations API.
	â¢	Automatically adds the new account to the existing AWS Organization.
	â¢	Optionally attaches baseline organizational policies or permission sets to the new account.

	2.	The codebase is well-documented and includes:
	â¢	Clear, step-by-step instructions on how it works
	â¢	Input variables for account name, email address, and optional OU or policy attachments.

	3.	The codebase should contain:
	â¢	A CI/CD pipeline or automation triggers.
	â¢	Make sure to set up permissions for who can run this pipeline and what approvals are needed for this to run

	4.	Security and IAM roles used in the code follow least privilege principles and are reviewed by the security team.
	
	6.	The process is tested and validated with at least one successful account creation and organization attachment.
	7.	The project configuration and branching strategy need to adhere to standards.

---
### #1: Create Gitlab CICD pipeline template file
- **State**: opened
- **Author**: Gregory Bosch
- **Assignee**: Gregory Bosch
- **Labels**: In Progress
- **Created**: 2025-06-23T19:37:26.641Z
- **Web**: https://gitlab.com/atlas-datascience/lion/cicd/containers/utility/container-tools/-/issues/1

Create pipeline template file for container builds.

* Integrate with orchestrated pipeline for container builds ftsg/lion/cicd/pipelines/containers
* Add CICD variable values to customize build to container needs (e.g. artifact locations, etc.)

Success:

* All jobs complete successfully
* SBOM, Container Signature and Vulnerability findings are published to Security and Vulnerability Dashboard
* Container is tagged and registered in project Registry

---
### #9: Document Schema Extension Strategies
- **State**: closed
- **Author**: Robert Price
- **Assignee**: Robert Price
- **Labels**: None
- **Created**: 2025-06-20T22:39:57.632Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/9

Need to document the schema extension strategies that can be used in OpenMetadata and recommend a stragey to the development team. Strategies that will be compared and contrasted are below.

Custom Properties
Direct Schema Modification
Hybrid Approach

---
### #8: Spike - Investigate OPA
- **State**: closed
- **Author**: Robert Price
- **Assignee**: Robert Price
- **Labels**: None
- **Created**: 2025-06-20T22:37:26.687Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/8

Investigate the usage of OPA to implement attributed based access control in OpenSearch. Purpose is to determine if OPA can be used to implement ic-ism and other classification frameworks in OpenSearch

---
### #7: Spike - Investigate Apache Rancher
- **State**: closed
- **Author**: Robert Price
- **Assignee**: Robert Price
- **Labels**: None
- **Created**: 2025-06-20T22:35:45.928Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/7

Investigate the usage of apache rancher to implement attribute based access control in OpenSearch. Purpose is to determine if Apache Rancher will meet the abac requirements that are needed to implement ic-ism and other classification frameworks

---
### #1: Review and Validate Runner Manager Project Configuration and Best Practices
- **State**: opened
- **Author**: Alain Atemnkeng
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-19T13:56:14.001Z
- **Web**: https://gitlab.com/atlas-datascience/lion/infrastructure/gitlab-runner-manager-templates/-/issues/1

We currently have a GitLab runner manager deployed on AWS Fargate that is responsible for provisioning EC2-based runners across multiple AWS accounts. The associated project that defines and manages the runner manager and its provisioning logic needs to be reviewed to ensure everything is functioning as expected.

Objectives:
	â¢	Review the current implementation of the runner manager project
	â¢	Confirm that:
	â¢	All configurations follow GitLab and AWS best practices
	â¢	The setup properly provisions runners into the correct accounts
	â¢	Security principles (least privilege, isolation, etc.) have been applied
	â¢	The code and infrastructure are well-organized and modular
	â¢	Documentation is complete and up to date

Deliverables:
	â¢	A summary of findings and any gaps or improvements
	â¢	Confirmation that the current setup is production-ready
	â¢	Recommendations (if any) for enhancements or refactoring

---
### #1: Design Centralized Pipeline Architecture for New Projects
- **State**: opened
- **Author**: Alain Atemnkeng
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-19T13:50:37.240Z
- **Web**: https://gitlab.com/atlas-datascience/lion/infrastructure/pipeline-templates/-/issues/1

We are in the process of creating multiple new projects within this GitLab repository. Instead of defining separate pipelines for each project, we want to manage all CI/CD pipelines from a centralized location to simplify maintenance, improve consistency, and streamline updates across projects.

Requirements:
	â¢	Design a centralized pipeline architecture that can support multiple independent projects.
	â¢	Ensure the architecture supports:
	â¢	Clear separation of pipeline logic for each project
	â¢	Reusability of shared pipeline components (e.g., templates or includes)
	â¢	Parameterization or conditional logic as needed per project
	â¢	Easy onboarding of new projects into the centralized pipeline

Deliverables:
	â¢	A proposed architecture diagram and description
	â¢	A recommended folder and naming structure
	â¢	A proof-of-concept or initial skeleton pipeline implementation (if feasible)
	â¢	Guidelines on how new projects can integrate into the central pipeline going forward

---
### #17: Define Edge Connector Event JSON Schema v.01
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Robert Price
- **Labels**: None
- **Created**: 2025-06-18T14:20:10.212Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/17

Following the good practice of OpenMetadata's data model, let's define a standardized event schema in JSON Schema.


```JSON
# Input: S3 ObjectCreated event
{
  "bucket": "client-data",
  "key": "imagery/2023/scene1.tif",
  "eventTime": "2023-06-17T10:30:00Z"
}
```

```JSON
# Output: Standardized metadata event
{
  "idempotencyKey": "sha256(identifier+timestamp+eventType+contentHash)",
  "tenantId": "client-123",
  "timestamp": "2023-06-17T10:30:15Z",
  "source": {
    "type": "S3"
    "event": "ObjectCreated",
    "identifier:" "/client-data/imagery/2023/scene1.tif"
    "location": "s3://client-data/imagery/2023/scene1.tif",
    "size": 1048576,
    "checksums": {"md5": "...", "sha256": "..."},
    "metadata": {
    }
  }
}
```

---
### #12: CI-CD: Quality Checks
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Gregory Bosch
- **Labels**: None
- **Created**: 2025-06-18T13:56:28.407Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/12

Add a GitLab CI workflow that enforces quality gates, static-analysis scans, and deployments to LocalStack and AWS account (May need to create separate ticket for AWS deployment, secrets config, etc).

**Acceptance Criteria**
- Workflow stages: `lint` -> `unit-test` -> `coverage â¥ 30%` -> `git-secrets scan` -> `semgrep` -> `LocalStack deploy (SAM/Serverless)`.
- Fails the build on any High/Critical vulnerability or secrets hit.
- Manual Promote to the development AWS account.

---
### #11: Edge Connector Basic Metrics
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-18T13:51:51.755Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/11

Create CloudWatch metrics for Lambda; Create dashboard with uptime and error alarms.

**Acceptance Criteria**
- Structured JSON logging, suggested to look for [Lambda Powertools](https://github.com/aws-powertools/powertools-lambda-typescript) for this or other alternatives like Watson.
- Custom metrics collected:
  - edge_events_sent_total (Counter)
  - edge_post_latency_ms (Histogram)
- CloudWatch Dashboard with:
  - send rate
  - latency P95
  - error count
- Alarms:
  - HighErrorRate - error > 1% for 5min.
  - BufferBacklog - SQS age > 2h.
- All CloudWatch log groups, dashboards, alerts deployed by SAM / Terraform / Serverless.

---
### #10: Create Mock Ingestion Gateway
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Adam Galyoon
- **Labels**: None
- **Created**: 2025-06-17T20:06:16.814Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/10

**Overview**

Develop a mock version of the Ingestion Gateway to facilitate local development and testing of the Edge Connector. This mock service will simulate the behavior of the actual Ingestion Gateway, allowing developers to test the Edge Connector functionality without requiring access to the production gateway.
Requirements

**Mock Gateway Features**

REST API endpoints that mirror the production Ingestion Gateway
JWT authentication validation (using same format as production)
Data ingestion endpoints with validation
Response simulation (success/error scenarios)
Request logging for debugging


**Endpoints to Implement**

POST /api/v1/ingest - Main data ingestion endpoint

GET /api/v1/health - Health check endpoint

POST /api/v1/auth/validate - Token validation endpoint (optional)

Configure appropriate response codes and payloads

---
### #9: JSON Encryption
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-17T20:05:35.895Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/9

Description:
Add encryption for payloads sent to the Ingestion Gateway. Use AWS KMS or symmetric encryption to encrypt payload contents before sending.


Technical Requirements:
* All JSON payloads must be encrypted before being stored or transmitted.

Acceptance Criteria:

* Payload body is encrypted using AES-256 or envelope encryption before transmission.
* Encryption key is retrieved securely from AWS Secrets Manager or KMS via `JWT_SECRET_ARN`.
* Gateway successfully decrypts the payload and returns 202 on valid inputs. (tag with assignee #10)
* Encrypted payload size remains < 50 KB after base64 encoding.
* `ENABLE_PAYLOAD_ENCRYPTION` env var toggles encryption; enabled by default.
* * Keys are securely  integrated with AWS KMS.
* Encryption and decryption processes need to be thoroughly tested for accuracy.
* Failures in encryption or decryption should be logged within logger.


Notes:
* AWS KMS Developer Guide âÂ What is AWS Key Management Service?
* https://docs.aws.amazon.com/kms/latest/developerguide/overview.html
* AWS Encryption SDK âÂ Encrypting and decrypting data
* Per discussion with Greg, this item can remain in the active backlist.

---
### #8: JWT Auth
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-17T20:04:56.289Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/8

Implement JWT (JSON Web Token) authentication for the Edge Connector when sending data to the Ingestion Gateway. This will ensure secure communication between the Edge Connector and the gateway by using AWS Secrets Manager to store and retrieve authentication credentials.

**Requirements**

**AWS Secrets Manager Integration**

Create a new secret in AWS Secrets Manager to store JWT credentials
Secret should include:

**JWT signing key/secret**
Issuer information
Token expiration configuration
Any additional authentication parameters

**Edge Connector Authentication Implementation**

Implement JWT token generation in the Edge Connector
Retrieve credentials from AWS Secrets Manager on startup
Generate and sign JWT tokens for each request to the Ingestion Gateway
Implement token refresh logic before expiration

**Security Considerations**

Use appropriate IAM roles for accessing AWS Secrets Manager
Implement secure credential caching with appropriate TTL
Ensure tokens have reasonable expiration times (recommended: 1 hour)
Include necessary claims in JWT payload (edge_connector_id, timestamp, etc.)

**Technical Details**

Use AWS SDK for Secrets Manager integration
Implement retry logic for credential retrieval
Handle credential rotation scenarios
Log authentication events appropriately (without exposing sensitive data)

**Acceptance Criteria**

 AWS Secret created with JWT credentials
 Edge Connector successfully retrieves credentials from Secrets Manager
 JWT tokens are generated and included in all requests to Ingestion Gateway
 Token refresh occurs before expiration
 Authentication failures are properly logged and handled
 Documentation updated with authentication flow

---
### #6: Exponential back-off and retry mechanism
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-17T20:02:35.364Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/6

Exponential Back-off and Retry 

Description:
Implement a back-off and retry mechanism for the edge connector when delivering events to the ingestion gateway. OpenMetaData / LocalStack should automatically handle errors (network timeouts or HTTP > 500 responses) by retrying failed requests. This will help avoid overloading the gateway.

Technical Requirements:

* On failure to send an event, the edge connector should wait for increasing delay (ideally, sequenced) before retrying.
* The mechanism could support the following parameters: initial delay, maximum delay, and maximum number of retries.
* If the maximum retry limit is reached, failures need to be logged within the logger.
* The back-off algorithm should use full jitter as recommended by AWS link below to avoid synchronized retries within LockStack.


Acceptance Criteria:
* When delivery to the ingestion gateway fails, the edge connector retries with exponential back-off and full jitter.
* All back-off and retry parameters are configurable via application properties .env/â¦
* Maximum retry attempts and wait time are enforced.
* Success resets the retry mechanism for the next operation.
* Unit and integration tests validate exponential back-off logic.

Notes:
* AWS Architecture Blog âÂ Exponential Backoff and Jitter
* https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
* AWS SDK Error Retries âÂ Retry Behavior
* https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html

---
### #5: Generate Idempotency Keys for Edge Connector output
- **State**: closed
- **Author**: Ryan Cross
- **Assignee**: Ryan Cross
- **Labels**: None
- **Created**: 2025-06-17T19:58:16.965Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/5

The edge connector should be able to process the same triggering input event multiple times, and the result should be the same as if it was only processed once. (within a reasonable time window) To do this, we need to implement some form of idempotency. 

**Success Criteria:**

* Generate an idempotency key based on the incoming event or subset of the event. Think generically, can hash the entire event payload if needed, we want this to work outside of just S3 eventually.
* Determine and scaffold (locally) a suitable architecture for persisting idempotency keys. (Suggestions: Redis Cache/DynamoDB)
* Build the control flow to check/set idemptotency keys before proceeding with extraction. 
* Investigate the use of AWS powertools idemptotency and existing Lion solution and create a detailed follow up story if more work is needed.

Links:
Lion Previous IMPL
https://docs.powertools.aws.dev/lambda/typescript/latest/features/idempotency/#amazon-dynamodb

---
### #4: File Type (MIME/EXIF) extractor
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-17T19:43:05.092Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/4



Description:
S3 MIME type metadata is often unreliable or may be missing if not explicitly set by the source system. The edge connector must ensure that each fileâs MIME type is accurately populated. Implement logic to identify and record the MIME type and lightweight metadata (file extension, size, encoding hints) for each file ingested, including unknown formats if possible.

Acceptance Criteria:

* MIME type is extracted using `mime-types` or `file-type` package based on file extension or magic bytes.
* Metadata includes: `mimeType`, `extension`, `sizeBytes`, `etag`, and optionally encoding.
* If MIME cannot be inferred, value is set to `application/octet-stream` with a warning log.
* Output JSON schema includes `source.mimeType` and source.extension.
* If S3 metadata for Content-Type/MIME type is missing or generic, the edge connector calls the MIME Type Extractor.
* MIME Type Extractor reads the file header and determines the actual MIME type.
* The extracted MIME type is included in the outgoing metadata payload.
* Solution works for common file types (PDF, TIFF, CSV) used in our datasets, please see example-datasets created by Serge.
* Unit/integration tests verify fallback logic and correct MIME type assignment.
* Unit tests cover CSV, PDF, JSON, and unknown file types.


Technical Requirements: 

* If the MIME type is not present or is set to a generic/unknown value, the edge connector should trigger the MIME Type Extractor.
* The MIME Type Extractor must review the file header to determine the correct MIME type.
* The determined MIME type should be added to the fileâs metadata before any downstream processing.

Notes:

* AWS S3 MIME Type Handling:
    * AWS S3 Documentation â Working with Object Metadata
    * https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html
    * AWS S3 â Content-Type and Metadata
    * https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html#object-metadata

---
### #3: Raw Geospatial Metadata Extractor
- **State**: opened
- **Author**: Ryan Cross
- **Assignee**: Ryan Cross
- **Labels**: None
- **Created**: 2025-06-17T19:41:24.821Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/3

Extractors should be pluggable and chainable. Meaning, they can be dropped in and out of an extraction chain with ease.

Create an extractor that implements the following methods to perform the task of extracting raw geospatial metadata.
```
interface Extractor<T,V> {
    initialize(): Promise<void>;
    extract(event: T, out: V): <T,V>
    can_extract: (event: T) => boolean;
}
```

**Success Criteria**
* GDAL dependencies configured up in project
* Extracts all raw geospatial data from the GDAL binding calls based on the filetype (raster vs vector)
* Populates raw data to our Edge Connector event output schema

Example datasets: https://gitlab.com/ftsg/lion/example-datasets/-/tree/EXAMPLE001-initial-dataset?ref_type=heads

**Out of Scope**
Batch processing

---
### #2: S3 Metadata Extractor
- **State**: closed
- **Author**: Ryan Cross
- **Assignee**: Ryan Cross
- **Labels**: None
- **Created**: 2025-06-17T19:39:20.841Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/2

The edge connector should have an extraction phase that retrieves all S3 related metadata.

You can find details on the S3 metadata model here.
https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html

Extractors should be pluggable and chainable. Meaning, they can be dropped in and out of an extraction chain with ease.

Create an extractor that implements the following methods to perform the task of extracting all relevant s3 metadata.
Tags, aws-metadata-x, triggering system event
```
interface Extractor<T,V> {
    initialize(): Promise<void>;
    extract(event: T, out: V): <T,V>
    can_extract: (event: T) => boolean;
}
```

**Success Criteria**

The extractor should be able to extract all relevant metadata to our schema provided by a s3 notifications event. https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html

---
### #1: Create base Lambda Function skeleton
- **State**: closed
- **Author**: Ryan Cross
- **Assignee**: Ryan Cross
- **Labels**: None
- **Created**: 2025-06-17T19:38:20.979Z
- **Web**: https://gitlab.com/atlas-datascience/lion/project-lion/edge-connector/-/issues/1

Create the initial codebase for the Node 22 + TypeScript Edge-Connector Lambda, including  configuring local deployment to LocalStack with our [Local Development Repo](https://gitlab.com/ftsg/lion/local-environment).

**Acceptance Criteria**
- Repo skeleton: `src/`, `test/`, `scripts/`, `docs/`.
- `README.md` with prerequisites and instruction to run locally.
- Connect Git pre-hooks with [Husky](https://typicode.github.io/husky/get-started.html).
  - ESLint
  - Prettier
- Jest for Unit test
  - Create placeholder test thats passes.
- `npm run build` produces minified bundle with esbuild.
- `npm run deploy:local` deploy resources to LocalStack deployed from [Local Development Repo](https://gitlab.com/ftsg/lion/local-environment).

---
### #2: Create new Repository for EDGE Connector
- **State**: closed
- **Author**: Serge Zahniy
- **Assignee**: Alain Atemnkeng
- **Labels**: None
- **Created**: 2025-06-17T18:23:12.443Z
- **Web**: https://gitlab.com/atlas-datascience/lion/local-environment/-/issues/2



---
### #6: Geospatial Connectors to docker-compose
- **State**: closed
- **Author**: Serge Zahniy
- **Assignee**: Serge Zahniy
- **Labels**: None
- **Created**: 2025-06-09T14:42:11.613Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/6

Update the existing docker-compose.yml and local development scripts to include the new geospatial connectors and ensure they can be easily run and tested.

Acceptance Criteria:

- Update docker-compose.yml to include connector services
- Add environment variables for connector configuration
- Create scripts to run sample ingestion processes
- Update documentation in local-environment README
- Ensure example datasets are properly mounted/accessible

---
### #5: OpenMetadata Schema Extension for Geospatial Data
- **State**: opened
- **Author**: Serge Zahniy
- **Assignee**: Robert Price
- **Labels**: None
- **Created**: 2025-06-09T14:26:42.372Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/5

Extend OpenMetadata data model to properly represent geospatial datasets including spatial properties, coordinate reference systems, and bounding boxes. 

OpenMetadata Database Schema will be influenced by #2 #3 #4 issues

Acceptance Criteria:

- Define spatial entity types in OpenMetadata
- Add fields for bounding boxes, spatial resolution and other missing properties
- Ensure compatibility with PostGIS
- Create migration scripts for schema updates and apply them to local dev stack
- Document the extended data model

---
### #4: Create Standard TIFF Connector
- **State**: closed
- **Author**: Serge Zahniy
- **Assignee**: Serge Zahniy
- **Labels**: None
- **Created**: 2025-06-09T14:24:16.908Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/4

Develop a connector for standard TIFF images that may contain geospatial metadata in EXIF or other embedded formats.

Use https://github.com/msgis/openmetadata-spatial-connector to understand implementation

The current extraction method is implemented in https://gitlab.com/ftsg/lion/core/data-in/extract-transform-load/inventory-enhancement/extraction and can be used as an example

Acceptance Criteria:

- Process .tiff files from example-datasets-tif directory
- Extract EXIF and embedded metadata
- Parse associated XML files
- Identify any spatial components in standard TIFF files
- Create OpenMetadata entities

---
### #3: Create Geospatial PDF Connector
- **State**: closed
- **Author**: Serge Zahniy
- **Assignee**: Unassigned
- **Labels**: None
- **Created**: 2025-06-09T14:23:04.451Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/3

Develop a connector that can process georeferenced PDF files and extract spatial metadata. This connector should handle PDF files with embedded geospatial information and associated XML metadata.

Use https://github.com/msgis/openmetadata-spatial-connector to understand implementation

The current extraction method is implemented in https://gitlab.com/ftsg/lion/core/data-in/extract-transform-load/inventory-enhancement/extraction and can be used as an example

Acceptance Criteria:

- Connector can process .pdf files from example-datasets-geo-pdf directory
- Extract geospatial information from georeferenced PDFs
- Parse associated XML metadata files
- Handle coordinate transformations if needed
- Create appropriate OpenMetadata entities

---
### #2: Create S3 GeoTIFF Connector (Proof of Concept)
- **State**: closed
- **Author**: Serge Zahniy
- **Assignee**: Ryan Cross
- **Labels**: None
- **Created**: 2025-06-09T14:11:25.656Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/2

Develop a connector that can read GeoTIFF files from S3 buckets (example-datasets-geo-tif folder) and extract both standard metadata and geospatial information including coordinate reference systems, bounding boxes, and other properties.

Use https://github.com/msgis/openmetadata-spatial-connector to understand implementation.

The current extraction method is implemented in https://gitlab.com/ftsg/lion/core/data-in/extract-transform-load/inventory-enhancement/extraction and can be used as an example

Acceptance Criteria:

- Connector can read .tif files from the example-datasets-geo-tif directory
- Extract geospatial metadata (CRS, bounds, resolution)
- Parse associated .xml metadata files
- Create OpenMetadata entities with spatial properties
- Store extracted metadata in PostgreSQL with PostGIS fields

---
### #1: Setup Example Datasets
- **State**: closed
- **Author**: Serge Zahniy
- **Assignee**: Serge Zahniy
- **Labels**: None
- **Created**: 2025-06-09T13:49:34.438Z
- **Web**: https://gitlab.com/atlas-datascience/lion/example-datasets/-/issues/1



---
### #1: Setup local development repository
- **State**: closed
- **Author**: Serge Zahniy
- **Assignee**: Serge Zahniy
- **Labels**: None
- **Created**: 2025-06-09T13:48:40.936Z
- **Web**: https://gitlab.com/atlas-datascience/lion/local-environment/-/issues/1



---
