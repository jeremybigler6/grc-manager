# AI-Powered Enterprise GRC Manager

A high-performance, local-first Governance, Risk, and Compliance (GRC) platform engineered in Python. This platform synthesizes traditional corporate risk management infrastructure with deterministic LLM pipelines to automate regulatory framework mapping, policy generation, and audit readiness reviews. 

Built to handle both complex cybersecurity frameworks and rigorous physical industrial regulations, this application bridges the gap between digital asset protection and operational risk.

---

## Core Architecture & Technical Capabilities

### Relational Database & Data Modeling (SQLite)
*   **Normalized Database Schema:** Utilizing SQLite to manage complex relational structures rather than flat files, ensuring strict data integrity.
*   **Many-to-Many Framework Mapping:** Implements robust junction tables (`risk_control_mapping`) to execute "assess once, comply many" logic. A single security control can be mapped simultaneously across disparate frameworks (e.g., NIST CSF, ISO 27001, and SOC 2).
*   **Immutable Audit Logging:** Features an append-only transaction ledger that captures every major database event, risk-score modification, and user action to provide an examiner-ready trail of platform activity.

### Context-Grounded AI Workspace (OpenAI API)
*   **Deterministic Risk Advising:** Ingests qualitative asset threats to evaluate business impacts, analyze likelihood/impact matrices, and prescribe mitigation strategies.
*   **Cross-Framework Gap Analysis:** Leverages system-prompted LLM pipelines to review existing company documentation against targeted regulatory requirements, isolating control deficiencies.
*   **Automated Evidence Review:** Simulates an internal auditor by evaluating submitted technical evidence against framework criteria, flagging insufficient artifacts, and suggesting explicit remediation documentation.
*   **Policy & Report Engineering:** Generates production-ready security policies, control objectives, and data-driven executive risk posture summaries based directly on live database records.

---

## Platform Features

### 1. Risk Register & Lifecycle Management
- Full CRUD operations supporting comprehensive Risk Profiles.
- Dynamic scoring tracking Inherent vs. Residual Risk metrics (Likelihood $\times$ Impact).
- Granular tracking for ownership assignment, risk treatment strategies (Accept, Mitigate, Transfer, Avoid), and target remediation timelines.

### 2. Control Library & Mapping Engine
- Centralized controls repository categorized by type (Administrative, Technical, Physical) and function (Preventive, Detective, Corrective).
- Direct linking mechanisms associating multiple controls to individual or grouped risks.
- Searchable indexing for rapid control retrieval during audit simulations.

### 3. Integrated Reporting Analytics
- Real-time dashboard generation tracking critical metrics:
  - Open vs. Closed Risk ratios.
  - Risk Level distribution frequencies.
  - Mean and Peak Enterprise Risk Scores.
  - Trackers for upcoming and overdue remediation tasks.
  - Dynamic risk matrix mapping.

---

## Dual-Domain Capabilities & Sample Data

The platform natively handles data across two fundamentally different but increasingly converging risk profiles, showcasing true enterprise flexibility:

### Cybersecurity & IT GRC
- Identity & Access Management (IAM)
- Zero Trust & Cloud Infrastructure Security
- Vendor/Third-Party Risk Management (TPRM)
- Vulnerability Management & Incident Response
- Data Protection, Privacy, and Business Continuity

### Industrial Operations & Critical Infrastructure
- SCADA & Industrial Control Systems (ICS) Security
- Gas Turbine, Boiler, and Steam System Operational Reliability
- Process Safety Management (PSM) & Electrical Reliability
- Environmental Regulatory Compliance (EPA NPDES, SCAQMD, CEMS)
- Confined Space & Physical Plant Safety

---

## Technology Stack

- **Core Language:** Python 3.11+
- **Database Engine:** SQLite (Relational Storage & Schema Optimization)
- **AI Integration:** OpenAI API (Advanced Prompt Engineering & Structured JSON Outputs)
- **Version Control:** Git & GitHub

---

## Project Structure

```text
├── main.py                     # Application entry point & runtime loop
├── database.py                 # SQLite connection layer, schema definition, & migrations
├── risk_register.py            # Risk data models, CRUD logic, and mathematical scoring
├── controls.py                 # Control library indexing & structural definitions
├── ai_tools.py                 # LLM pipeline orchestration & prompt engineering
├── openai_helper.py            # API client initialization, payload validation, & error handling
├── grc_enterprise.db          # Live SQLite relational database 
├── audit_logger.py             # Append-only transaction log handler
├── generated_policies/         # Output directory for AI-engineered documentation
├── generated_reports/          # Output directory for management-ready compliance reports
└── README.md                   # System documentation