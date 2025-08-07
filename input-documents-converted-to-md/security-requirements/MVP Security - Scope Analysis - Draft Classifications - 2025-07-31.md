# MVP Security - Scope Analysis - Draft Classifications

**Source:** `MVP Security - Scope Analysis - Draft Classifications - 2025-07-31.csv`
**Converted:** convert_security_csv.py
**Total Controls:** 287

## NIST 800-53 Revision 5 Security Controls Analysis

This document contains the complete analysis of NIST 800-53 Rev 5 moderate baseline security controls for the Atlas Data Science Project Lion MVP. Controls are classified using the three-level methodology defined in the Security Requirements Classification document.

### Control Classification Legend

- **In Scope:** Indicates if control applies to MVP implementation
- **MVP Requirement:** Specific implementation requirements and acceptance criteria
- **Control Type:** Classification level (Inherited, Customer-Provided, Developer-Implemented)
- **Baseline:** Security control baseline applicability (Low, Moderate, High)

---

## Security Controls Inventory

### AC - Family Controls (39 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `AC-1` | Policy and Procedures |  |  | ✓ |
| `AC-2` | Account Management |  |  | ✓ |
| `AC-2(1)` | Account Management | Automated System Account M... |  |  | ✓ |
| `AC-2(2)` | Account Management | Automated Temporary and Em... |  |  | ✓ |
| `AC-2(3)` | Account Management | Disable Accounts |  |  | ✓ |
| `AC-2(4)` | Account Management | Automated Audit Actions |  |  | ✓ |
| `AC-2(5)` | Account Management | Inactivity Logout |  |  | ✓ |
| `AC-2(13)` | Account Management | Disable Accounts for High-... |  |  | ✓ |
| `AC-3` | Access Enforcement |  |  | ✓ |
| `AC-4` | Information Flow Enforcement |  |  | ✓ |
| `AC-5` | Separation of Duties |  |  | ✓ |
| `AC-6` | Least Privilege |  |  | ✓ |
| `AC-6(1)` | Least Privilege | Authorize Access to Security ... |  |  | ✓ |
| `AC-6(2)` | Least Privilege | Non-privileged Access for Non... |  |  | ✓ |
| `AC-6(5)` | Least Privilege | Privileged Accounts |  |  | ✓ |
| `AC-6(7)` | Least Privilege | Review of User Privileges |  |  | ✓ |
| `AC-6(9)` | Least Privilege | Log Use of Privileged Functions |  |  | ✓ |
| `AC-6(10)` | Least Privilege | Prohibit Non-privileged Users... |  |  | ✓ |
| `AC-7` | Unsuccessful Logon Attempts |  |  | ✓ |
| `AC-8` | System Use Notification |  |  | ✓ |
| `AC-11` | Device Lock |  |  | ✓ |
| `AC-11(1)` | Device Lock | Pattern-hiding Displays |  |  | ✓ |
| `AC-12` | Session Termination |  |  | ✓ |
| `AC-14` | Permitted Actions Without Identification or Aut... |  |  | ✓ |
| `AC-17` | Remote Access |  |  | ✓ |
| `AC-17(1)` | Remote Access | Monitoring and Control |  |  | ✓ |
| `AC-17(2)` | Remote Access | Protection of Confidentiality a... |  |  | ✓ |
| `AC-17(3)` | Remote Access | Managed Access Control Points |  |  | ✓ |
| `AC-17(4)` | Remote Access | Privileged Commands and Access |  |  | ✓ |
| `AC-18` | Wireless Access |  |  | ✓ |
| `AC-18(1)` | Wireless Access | Authentication and Encryption |  |  | ✓ |
| `AC-18(3)` | Wireless Access | Disable Wireless Networking |  |  | ✓ |
| `AC-19` | Access Control for Mobile Devices |  |  | ✓ |
| `AC-19(5)` | Access Control for Mobile Devices | Full Device... |  |  | ✓ |
| `AC-20` | Use of External Systems |  |  | ✓ |
| `AC-20(1)` | Use of External Systems | Limits on Authorized Use |  |  | ✓ |
| `AC-20(2)` | Use of External Systems | Portable Storage Devi... |  |  | ✓ |
| `AC-21` | Information Sharing |  |  | ✓ |
| `AC-22` | Publicly Accessible Content |  |  | ✓ |

### AT - Family Controls (6 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `AT-1` | Policy and Procedures |  |  | ✓ |
| `AT-2` | Literacy Training and Awareness |  |  | ✓ |
| `AT-2(2)` | Literacy Training and Awareness | Insider Threat |  |  | ✓ |
| `AT-2(3)` | Literacy Training and Awareness | Social Engine... |  |  | ✓ |
| `AT-3` | Role-based Training |  |  | ✓ |
| `AT-4` | Training Records |  |  | ✓ |

### AU - Family Controls (16 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `AU-1` | Policy and Procedures |  |  | ✓ |
| `AU-2` | Event Logging |  |  | ✓ |
| `AU-3` | Content of Audit Records |  |  | ✓ |
| `AU-3(1)` | Content of Audit Records | Additional Audit Inf... |  |  | ✓ |
| `AU-4` | Audit Log Storage Capacity |  |  | ✓ |
| `AU-5` | Response to Audit Logging Process Failures |  |  | ✓ |
| `AU-6` | Audit Record Review, Analysis, and Reporting |  |  | ✓ |
| `AU-6(1)` | Audit Record Review, Analysis, and Reporting | ... |  |  | ✓ |
| `AU-6(3)` | Audit Record Review, Analysis, and Reporting | ... |  |  | ✓ |
| `AU-7` | Audit Record Reduction and Report Generation |  |  | ✓ |
| `AU-7(1)` | Audit Record Reduction and Report Generation | ... |  |  | ✓ |
| `AU-8` | Time Stamps |  |  | ✓ |
| `AU-9` | Protection of Audit Information |  |  | ✓ |
| `AU-9(4)` | Protection of Audit Information | Access by Sub... |  |  | ✓ |
| `AU-11` | Audit Record Retention |  |  | ✓ |
| `AU-12` | Audit Record Generation |  |  | ✓ |

### CA - Family Controls (10 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `CA-1` | Policy and Procedures |  |  | ✓ |
| `CA-2` | Control Assessments |  |  | ✓ |
| `CA-2(1)` | Control Assessments | Independent Assessors |  |  | ✓ |
| `CA-3` | Information Exchange |  |  | ✓ |
| `CA-5` | Plan of Action and Milestones |  |  | ✓ |
| `CA-6` | Authorization |  |  | ✓ |
| `CA-7` | Continuous Monitoring |  |  | ✓ |
| `CA-7(1)` | Continuous Monitoring | Independent Assessment |  |  | ✓ |
| `CA-7(4)` | Continuous Monitoring | Risk Monitoring |  |  | ✓ |
| `CA-9` | Internal System Connections |  |  | ✓ |

### CM - Family Controls (24 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `CM-1` | Policy and Procedures |  |  | ✓ |
| `CM-2` | Baseline Configuration |  |  | ✓ |
| `CM-2(2)` | Baseline Configuration | Automation Support for... |  |  | ✓ |
| `CM-2(3)` | Baseline Configuration | Retention of Previous ... |  |  | ✓ |
| `CM-2(7)` | Baseline Configuration | Configure Systems and ... |  |  | ✓ |
| `CM-3` | Configuration Change Control |  |  | ✓ |
| `CM-3(2)` | Configuration Change Control | Testing, Validat... |  |  | ✓ |
| `CM-3(4)` | Configuration Change Control | Security and Pri... |  |  | ✓ |
| `CM-4` | Impact Analyses |  |  | ✓ |
| `CM-4(2)` | Impact Analyses | Verification of Controls |  |  | ✓ |
| `CM-5` | Access Restrictions for Change |  |  | ✓ |
| `CM-6` | Configuration Settings |  |  | ✓ |
| `CM-7` | Least Functionality |  |  | ✓ |
| `CM-7(1)` | Least Functionality | Periodic Review |  |  | ✓ |
| `CM-7(2)` | Least Functionality | Prevent Program Execution |  |  | ✓ |
| `CM-7(5)` | Least Functionality | Authorized Software |  |  | ✓ |
| `CM-8` | System Component Inventory |  |  | ✓ |
| `CM-8(1)` | System Component Inventory | Updates During Ins... |  |  | ✓ |
| `CM-8(3)` | System Component Inventory | Automated Unauthor... |  |  | ✓ |
| `CM-9` | Configuration Management Plan |  |  | ✓ |
| `CM-10` | Software Usage Restrictions |  |  | ✓ |
| `CM-11` | User-installed Software |  |  | ✓ |
| `CM-12` | Information Location |  |  | ✓ |
| `CM-12(1)` | Information Location | Automated Tools to Suppo... |  |  | ✓ |

### CP - Family Controls (23 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `CP-1` | Policy and Procedures |  |  | ✓ |
| `CP-2` | Contingency Plan |  |  | ✓ |
| `CP-2(1)` | Contingency Plan | Coordinate with Related Plans |  |  | ✓ |
| `CP-2(3)` | Contingency Plan | Resume Mission and Business ... |  |  | ✓ |
| `CP-2(8)` | Contingency Plan | Identify Critical Assets |  |  | ✓ |
| `CP-3` | Contingency Training |  |  | ✓ |
| `CP-4` | Contingency Plan Testing |  |  | ✓ |
| `CP-4(1)` | Contingency Plan Testing | Coordinate with Rela... |  |  | ✓ |
| `CP-6` | Alternate Storage Site |  |  | ✓ |
| `CP-6(1)` | Alternate Storage Site | Separation from Primar... |  |  | ✓ |
| `CP-6(3)` | Alternate Storage Site | Accessibility |  |  | ✓ |
| `CP-7` | Alternate Processing Site |  |  | ✓ |
| `CP-7(1)` | Alternate Processing Site | Separation from Pri... |  |  | ✓ |
| `CP-7(2)` | Alternate Processing Site | Accessibility |  |  | ✓ |
| `CP-7(3)` | Alternate Processing Site | Priority of Service |  |  | ✓ |
| `CP-8` | Telecommunications Services |  |  | ✓ |
| `CP-8(1)` | Telecommunications Services | Priority of Servi... |  |  | ✓ |
| `CP-8(2)` | Telecommunications Services | Single Points of ... |  |  | ✓ |
| `CP-9` | System Backup |  |  | ✓ |
| `CP-9(1)` | System Backup | Testing for Reliability and Int... |  |  | ✓ |
| `CP-9(8)` | System Backup | Cryptographic Protection |  |  | ✓ |
| `CP-10` | System Recovery and Reconstitution |  |  | ✓ |
| `CP-10(2)` | System Recovery and Reconstitution | Transactio... |  |  | ✓ |

### IA - Family Controls (24 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `IA-1` | Policy and Procedures |  |  | ✓ |
| `IA-2` | Identification and Authentication (organization... |  |  | ✓ |
| `IA-2(1)` | Identification and Authentication (organization... |  |  | ✓ |
| `IA-2(2)` | Identification and Authentication (organization... |  |  | ✓ |
| `IA-2(8)` | Identification and Authentication (organization... |  |  | ✓ |
| `IA-2(12)` | Identification and Authentication (organization... |  |  | ✓ |
| `IA-3` | Device Identification and Authentication |  |  | ✓ |
| `IA-4` | Identifier Management |  |  | ✓ |
| `IA-4(4)` | Identifier Management | Identify User Status |  |  | ✓ |
| `IA-5` | Authenticator Management |  |  | ✓ |
| `IA-5(1)` | Authenticator Management | Password-based Authe... |  |  | ✓ |
| `IA-5(2)` | Authenticator Management | Public Key-based Aut... |  |  | ✓ |
| `IA-5(6)` | Authenticator Management | Protection of Authen... |  |  | ✓ |
| `IA-6` | Authentication Feedback |  |  | ✓ |
| `IA-7` | Cryptographic Module Authentication |  |  | ✓ |
| `IA-8` | Identification and Authentication (non-organiza... |  |  | ✓ |
| `IA-8(1)` | Identification and Authentication (non-organiza... |  |  | ✓ |
| `IA-8(2)` | Identification and Authentication (non-organiza... |  |  | ✓ |
| `IA-8(4)` | Identification and Authentication (non-organiza... |  |  | ✓ |
| `IA-11` | Re-authentication |  |  | ✓ |
| `IA-12` | Identity Proofing |  |  | ✓ |
| `IA-12(2)` | Identity Proofing | Identity Evidence |  |  | ✓ |
| `IA-12(3)` | Identity Proofing | Identity Evidence Validatio... |  |  | ✓ |
| `IA-12(5)` | Identity Proofing | Address Confirmation |  |  | ✓ |

### IR - Family Controls (13 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `IR-1` | Policy and Procedures |  |  | ✓ |
| `IR-2` | Incident Response Training |  |  | ✓ |
| `IR-3` | Incident Response Testing |  |  | ✓ |
| `IR-3(2)` | Incident Response Testing | Coordination with R... |  |  | ✓ |
| `IR-4` | Incident Handling |  |  | ✓ |
| `IR-4(1)` | Incident Handling | Automated Incident Handling... |  |  | ✓ |
| `IR-5` | Incident Monitoring |  |  | ✓ |
| `IR-6` | Incident Reporting |  |  | ✓ |
| `IR-6(1)` | Incident Reporting | Automated Reporting |  |  | ✓ |
| `IR-6(3)` | Incident Reporting | Supply Chain Coordination |  |  | ✓ |
| `IR-7` | Incident Response Assistance |  |  | ✓ |
| `IR-7(1)` | Incident Response Assistance | Automation Suppo... |  |  | ✓ |
| `IR-8` | Incident Response Plan |  |  | ✓ |

### MA - Family Controls (9 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `MA-1` | Policy and Procedures |  |  | ✓ |
| `MA-2` | Controlled Maintenance |  |  | ✓ |
| `MA-3` | Maintenance Tools |  |  | ✓ |
| `MA-3(1)` | Maintenance Tools | Inspect Tools |  |  | ✓ |
| `MA-3(2)` | Maintenance Tools | Inspect Media |  |  | ✓ |
| `MA-3(3)` | Maintenance Tools | Prevent Unauthorized Removal |  |  | ✓ |
| `MA-4` | Nonlocal Maintenance |  |  | ✓ |
| `MA-5` | Maintenance Personnel |  |  | ✓ |
| `MA-6` | Timely Maintenance |  |  | ✓ |

### MP - Family Controls (7 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `MP-1` | Policy and Procedures |  |  | ✓ |
| `MP-2` | Media Access |  |  | ✓ |
| `MP-3` | Media Marking |  |  | ✓ |
| `MP-4` | Media Storage |  |  | ✓ |
| `MP-5` | Media Transport |  |  | ✓ |
| `MP-6` | Media Sanitization |  |  | ✓ |
| `MP-7` | Media Use |  |  | ✓ |

### PE - Family Controls (18 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `PE-1` | Policy and Procedures |  |  | ✓ |
| `PE-2` | Physical Access Authorizations |  |  | ✓ |
| `PE-3` | Physical Access Control |  |  | ✓ |
| `PE-4` | Access Control for Transmission |  |  | ✓ |
| `PE-5` | Access Control for Output Devices |  |  | ✓ |
| `PE-6` | Monitoring Physical Access |  |  | ✓ |
| `PE-6(1)` | Monitoring Physical Access | Intrusion Alarms a... |  |  | ✓ |
| `PE-8` | Visitor Access Records |  |  | ✓ |
| `PE-9` | Power Equipment and Cabling |  |  | ✓ |
| `PE-10` | Emergency Shutoff |  |  | ✓ |
| `PE-11` | Emergency Power |  |  | ✓ |
| `PE-12` | Emergency Lighting |  |  | ✓ |
| `PE-13` | Fire Protection |  |  | ✓ |
| `PE-13(1)` | Fire Protection | Detection Systems – Automatic... |  |  | ✓ |
| `PE-14` | Environmental Controls |  |  | ✓ |
| `PE-15` | Water Damage Protection |  |  | ✓ |
| `PE-16` | Delivery and Removal |  |  | ✓ |
| `PE-17` | Alternate Work Site |  |  | ✓ |

### PL - Family Controls (7 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `PL-1` | Policy and Procedures |  |  | ✓ |
| `PL-2` | System Security and Privacy Plans |  |  | ✓ |
| `PL-4` | Rules of Behavior |  |  | ✓ |
| `PL-4(1)` | Rules of Behavior | Social Media and External S... |  |  | ✓ |
| `PL-8` | Security and Privacy Architectures |  |  | ✓ |
| `PL-10` | Baseline Selection |  |  | ✓ |
| `PL-11` | Baseline Tailoring |  |  | ✓ |

### PS - Family Controls (9 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `PS-1` | Policy and Procedures |  |  | ✓ |
| `PS-2` | Position Risk Designation |  |  | ✓ |
| `PS-3` | Personnel Screening |  |  | ✓ |
| `PS-4` | Personnel Termination |  |  | ✓ |
| `PS-5` | Personnel Transfer |  |  | ✓ |
| `PS-6` | Access Agreements |  |  | ✓ |
| `PS-7` | External Personnel Security |  |  | ✓ |
| `PS-8` | Personnel Sanctions |  |  | ✓ |
| `PS-9` | Position Descriptions |  |  | ✓ |

### RA - Family Controls (10 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `RA-1` | Policy and Procedures |  |  | ✓ |
| `RA-2` | Security Categorization |  |  | ✓ |
| `RA-3` | Risk Assessment |  |  | ✓ |
| `RA-3(1)` | Risk Assessment | Supply Chain Risk Assessment |  |  | ✓ |
| `RA-5` | Vulnerability Monitoring and Scanning |  |  | ✓ |
| `RA-5(2)` | Vulnerability Monitoring and Scanning | Update ... |  |  | ✓ |
| `RA-5(5)` | Vulnerability Monitoring and Scanning | Privile... |  |  | ✓ |
| `RA-5(11)` | Vulnerability Monitoring and Scanning | Public ... |  |  | ✓ |
| `RA-7` | Risk Response |  |  | ✓ |
| `RA-9` | Criticality Analysis |  |  | ✓ |

### SA - Family Controls (17 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `SA-1` | Policy and Procedures |  |  | ✓ |
| `SA-2` | Allocation of Resources |  |  | ✓ |
| `SA-3` | System Development Life Cycle |  |  | ✓ |
| `SA-4` | Acquisition Process |  |  | ✓ |
| `SA-4(1)` | Acquisition Process | Functional Properties of ... |  |  | ✓ |
| `SA-4(2)` | Acquisition Process | Design and Implementation... |  |  | ✓ |
| `SA-4(9)` | Acquisition Process | Functions, Ports, Protoco... |  |  | ✓ |
| `SA-4(10)` | Acquisition Process | Use of Approved PIV Products |  |  | ✓ |
| `SA-5` | System Documentation |  |  | ✓ |
| `SA-8` | Security and Privacy Engineering Principles |  |  | ✓ |
| `SA-9` | External System Services |  |  | ✓ |
| `SA-9(2)` | External System Services | Identification of Fu... |  |  | ✓ |
| `SA-10` | Developer Configuration Management |  |  | ✓ |
| `SA-11` | Developer Testing and Evaluation |  |  | ✓ |
| `SA-15` | Development Process, Standards, and Tools |  |  | ✓ |
| `SA-15(3)` | Development Process, Standards, and Tools | Cri... |  |  | ✓ |
| `SA-22` | Unsupported System Components |  |  | ✓ |

### SC - Family Controls (25 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `SC-1` | Policy and Procedures |  |  | ✓ |
| `SC-2` | Separation of System and User Functionality |  |  | ✓ |
| `SC-4` | Information in Shared System Resources |  |  | ✓ |
| `SC-5` | Denial-of-service Protection |  |  | ✓ |
| `SC-7` | Boundary Protection |  |  | ✓ |
| `SC-7(3)` | Boundary Protection | Access Points |  |  | ✓ |
| `SC-7(4)` | Boundary Protection | External Telecommunicatio... |  |  | ✓ |
| `SC-7(5)` | Boundary Protection | Deny by Default — Allow b... |  |  | ✓ |
| `SC-7(7)` | Boundary Protection | Split Tunneling for Remot... |  |  | ✓ |
| `SC-7(8)` | Boundary Protection | Route Traffic to Authenti... |  |  | ✓ |
| `SC-8` | Transmission Confidentiality and Integrity |  |  | ✓ |
| `SC-8(1)` | Transmission Confidentiality and Integrity | Cr... |  |  | ✓ |
| `SC-10` | Network Disconnect |  |  | ✓ |
| `SC-12` | Cryptographic Key Establishment and Management |  |  | ✓ |
| `SC-13` | Cryptographic Protection |  |  | ✓ |
| `SC-15` | Collaborative Computing Devices and Applications |  |  | ✓ |
| `SC-17` | Public Key Infrastructure Certificates |  |  | ✓ |
| `SC-18` | Mobile Code |  |  | ✓ |
| `SC-20` | Secure Name/address Resolution Service (authori... |  |  | ✓ |
| `SC-21` | Secure Name/address Resolution Service (recursi... |  |  | ✓ |
| `SC-22` | Architecture and Provisioning for Name/address ... |  |  | ✓ |
| `SC-23` | Session Authenticity |  |  | ✓ |
| `SC-28` | Protection of Information at Rest |  |  | ✓ |
| `SC-28(1)` | Protection of Information at Rest | Cryptograph... |  |  | ✓ |
| `SC-39` | Process Isolation |  |  | ✓ |

### SI - Family Controls (18 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `SI-1` | Policy and Procedures |  |  | ✓ |
| `SI-2` | Flaw Remediation |  |  | ✓ |
| `SI-2(2)` | Flaw Remediation | Automated Flaw Remediation S... |  |  | ✓ |
| `SI-3` | Malicious Code Protection |  |  | ✓ |
| `SI-4` | System Monitoring |  |  | ✓ |
| `SI-4(2)` | System Monitoring | Automated Tools and Mechani... |  |  | ✓ |
| `SI-4(4)` | System Monitoring | Inbound and Outbound Commun... |  |  | ✓ |
| `SI-4(5)` | System Monitoring | System-generated Alerts |  |  | ✓ |
| `SI-5` | Security Alerts, Advisories, and Directives |  |  | ✓ |
| `SI-7` | Software, Firmware, and Information Integrity |  |  | ✓ |
| `SI-7(1)` | Software, Firmware, and Information Integrity |... |  |  | ✓ |
| `SI-7(7)` | Software, Firmware, and Information Integrity |... |  |  | ✓ |
| `SI-8` | Spam Protection |  |  | ✓ |
| `SI-8(2)` | Spam Protection | Automatic Updates |  |  | ✓ |
| `SI-10` | Information Input Validation |  |  | ✓ |
| `SI-11` | Error Handling |  |  | ✓ |
| `SI-12` | Information Management and Retention |  |  | ✓ |
| `SI-16` | Memory Protection |  |  | ✓ |

### SR - Family Controls (12 controls)

| Control | Name | In Scope | MVP Requirement | Baseline |
|---------|------|----------|-----------------|----------|
| `SR-1` | Policy and Procedures |  |  | ✓ |
| `SR-2` | Supply Chain Risk Management Plan |  |  | ✓ |
| `SR-2(1)` | Supply Chain Risk Management Plan | Establish S... |  |  | ✓ |
| `SR-3` | Supply Chain Controls and Processes |  |  | ✓ |
| `SR-5` | Acquisition Strategies, Tools, and Methods |  |  | ✓ |
| `SR-6` | Supplier Assessments and Reviews |  |  | ✓ |
| `SR-8` | Notification Agreements |  |  | ✓ |
| `SR-10` | Inspection of Systems or Components |  |  | ✓ |
| `SR-11` | Component Authenticity |  |  | ✓ |
| `SR-11(1)` | Component Authenticity | Anti-counterfeit Training |  |  | ✓ |
| `SR-11(2)` | Component Authenticity | Configuration Control ... |  |  | ✓ |
| `SR-12` | Component Disposal |  |  | ✓ |

---

## Detailed Control Specifications

*Note: Due to document length, full control text and discussion are preserved in original CSV format. Key implementation requirements are extracted above in the family tables.*

### Developer-Implemented Controls Summary

For BMad agent processing, the following control families require active development implementation:

| Family | Total Controls | In Scope | With MVP Requirements | Priority |
|--------|----------------|----------|-----------------------|----------|
| AC | 39 | 0 | 0 | Low |
| AT | 6 | 0 | 0 | Low |
| AU | 16 | 0 | 0 | Low |
| CA | 10 | 0 | 0 | Low |
| CM | 24 | 0 | 0 | Low |
| CP | 23 | 0 | 0 | Low |
| IA | 24 | 0 | 0 | Low |
| IR | 13 | 0 | 0 | Low |
| MA | 9 | 0 | 0 | Low |
| MP | 7 | 0 | 0 | Low |
| PE | 18 | 0 | 0 | Low |
| PL | 7 | 0 | 0 | Low |
| PS | 9 | 0 | 0 | Low |
| RA | 10 | 0 | 0 | Low |
| SA | 17 | 0 | 0 | Low |
| SC | 25 | 0 | 0 | Low |
| SI | 18 | 0 | 0 | Low |
| SR | 12 | 0 | 0 | Low |

---

## Integration Notes

### BMad Agent Processing
- Use `/analyst` for security requirements analysis and gap identification
- Use `/architect` for security architecture validation against controls
- Use `/pm` for security story prioritization and sprint planning
- Use `/dev` for security control implementation in Project Lion components

### Project Lion Component Mapping
Security controls directly impact:
- **Edge Connector:** Customer VPC isolation, IAM permissions, encryption
- **Ingestion Gateway:** Authentication, authorization, audit logging
- **Metadata Catalog:** Data classification, access controls, audit trails
- **Policy Engine:** RBAC, ABAC implementation requirements
- **Search & Discovery:** Tenant isolation, field-level security

**Total Controls Analyzed:** 287
**Moderate Baseline Controls:** 287
**Control Families:** 18

*Generated from CSV export for BMad-Method security requirements processing*