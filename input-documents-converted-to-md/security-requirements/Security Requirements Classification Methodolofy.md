1.0 Security Control Classification Methodology
To effectively manage the security requirements for the Lion MVP product, we are adopting a three-level classification system for all security controls. This methodology is designed to streamline the implementation process by providing a clear, hierarchical view of control ownership and technical responsibility. This approach ensures that our agile sprints are precisely scoped, allowing for efficient task prioritization, self-organization, and assignment of user stories to team members based on their specific expertise. The framework is built on the established principles of the FedRAMP and AWS Shared Responsibility Model.

1.1 Level 1: High-Level Control Ownership
The first level of classification defines the overarching ownership of each security control, aligning with the Shared Responsibility Model. This level serves as the initial filter to determine whether a control is in or out of scope for our team’s direct implementation efforts.

Inherited: These controls are fully owned, implemented, and documented by AWS as part of their FedRAMP Moderate authorization for AWS GovCloud. As a customer, our team inherits these controls, and they are therefore considered out of the Lion MVP's direct scope of work.

Customer-Provided (Procedural/Documentation): These are non-technical controls related to organizational policies, procedures, and documentation. While the development team provides input and support, the responsibility for creating and maintaining these artifacts typically rests with a Governance, Risk, and Compliance (GRC) team or the Information System Security Officer (ISSO).

Developer-Implemented: This is the primary classification for all technical work that the Lion MVP team is responsible for. These controls must be designed, implemented, and configured by our team and are the central focus of our security-related user stories.

1.2 Level 2: Team-Level Responsibility
The second level of classification breaks down the "Developer-Implemented" controls into two distinct categories, directly corresponding to the specializations within our agile team. This level is crucial for reducing decision-making overhead and enabling team members to self-organize and pull work from the backlog based on their expertise.

Platform Engineering: This category includes controls related to the foundational infrastructure and security services. These are the responsibilities of our platform engineers, who use tools like Terraform to provision and manage the cloud environment.

Software Development: This category encompasses all controls related to the application layer, custom code, and the direct configuration of application-facing services. These are the responsibilities of our software developers.

1.3 Level 3: Fine-Grained Technical Specialization
The third level provides an even more granular breakdown of the Level 2 categories, allowing for precise user story assignments within the Platform Engineering and Software Development teams. This level directly maps to specific technical domains and skill sets, further fostering agile principles by enabling a deep focus on specialized tasks.

Platform Engineering Sub-categories:

Networking: Includes controls for network infrastructure components like VPCs, Security Groups, Network ACLs, and other related services.

Security Services: Encompasses the configuration of dedicated security tools like AWS WAF, GuardDuty, and AWS Config.

Core Services: Pertains to foundational AWS services such as IAM, AWS Organizations, and account provisioning.

Software Development Sub-categories:

Application Layer: Focuses on controls implemented in the application's source code, including business logic, authentication, and user interfaces.

Data Services: Involves the secure configuration of data-related services such as databases (Amazon RDS), object storage (Amazon S3), and encryption key management (AWS KMS).

Web Services: Covers the security configurations for microservices and API-related components, including API Gateway and Lambda functions.

By implementing this three-level classification system, we can ensure a transparent, efficient, and well-organized approach to meeting the security requirements for the Lion MVP. It provides a clear line of sight from a top-level security control to the specific team member responsible for its implementation, ultimately accelerating our path to a successful ATO.