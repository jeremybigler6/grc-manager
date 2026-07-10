# AI-Powered Enterprise GRC Manager

A high-performance, local-first Governance, Risk, and Compliance (GRC) platform engineered in Python. This platform seamlessly synthesizes traditional corporate risk management infrastructure with deterministic LLM pipelines to automate regulatory framework mapping, policy generation, and autonomous audit readiness reviews.

Built to handle both complex cybersecurity frameworks and rigorous physical industrial regulations, this application bridges the gap between digital asset protection and operational risk.

---

## 🛠️ App Module Quick Reference

The application is structured into four main terminal hubs, designed to keep automated AI pipelines distinct from manual record management.

### 1. AI Operations Center
The primary engine room for all artificial intelligence workflows. It is divided into two distinct zones:
* **Agentic & Automated Engines (`ai_services_menu`):** 
  * *Autonomous GRC Agent Loop:* Pass the AI a broad, complex objective (e.g., `"Audit Risk R-001 and remediate gaps"`). The agent runs background analysis loops and prints a comprehensive final compliance report.
  * *Crosswalk Suggestion Engine:* Input a raw corporate control statement, and the AI maps it directly to matching NIST, ISO, or SOC 2 framework requirements.
  * *Pending AI Mapping Suggestions Queue:* A human-in-the-loop review panel where automated background crosswalk mappings wait for a manager to manually approve or reject them before database ingestion.
* **AI Ad-Hoc Workspace (`ai_tools_menu`):** An interactive, real-time playground for manual consultation. It includes an AI Risk Advisor for threat analysis and a Framework Assistant designed for strict regulatory lookups of specific framework requirements based on known control IDs.

### 2. Manual Controls & Risk Management
The traditional compliance workbook. Use this module to manually execute full CRUD operations, editing, viewing, and tracking corporate risks and mitigation controls without using AI pipelines.

### 3. Reports & Audit Trail
The system accountability center. 
* Generates data-driven executive risk summaries and flat compliance reports based on live database metrics.
* Displays an immutable, rolling transaction log of the last 50 platform activities (`view_audit_trail`). 
* Contains a protected, dual-confirmation function to purge and clear the audit log database tables.

### 4. Import Data from CSV
The initialization utility. Allows you to bulk-upload your existing spreadsheet data directly into the application's relational database.

---

---

## 🚀 Quick Start Example: Testing the AI Crosswalk

To see how the deterministic AI harmonization pipeline handles multi-framework overlaps:

1. Run the application and open **Option 1 (AI Operations Center)** -> **Option 1 (Agentic & Automated Engines)**.
2. Select **Option 2 (Run Crosswalk Suggestion Engine)** and paste an internal corporate control statement you want evaluated.
3. The AI scans your internal data, compares the incoming rules against baseline frameworks, and identifies overlapping requirements to prevent duplicate work.
4. **Initial ingestion complete. Open Option 2 from the main menu to act as Manager.** (Navigate to your pending suggestions queue to review, modify, or approve the AI's cross-framework mapping suggestions).

---

## Core Architecture & Technical Capabilities

### Relational Database & Data Modeling (SQLite)
* **Normalized Database Schema:** Utilizing SQLite to manage complex relational structures rather than flat files, ensuring strict data integrity.
* **Many-to-Many Framework Mapping:** Implements robust junction tables (`risk_control_mapping`) to execute "assess once, comply many" logic. A single security control can be mapped simultaneously across disparate frameworks (e.g., NIST CSF, ISO 27001, and SOC 2).
* **Immutable Audit Logging:** Features an append-only transaction ledger that captures every major database event, risk-score modification, and user action to provide an examiner-ready trail of platform activity.

### Context-Grounded AI Workspace (OpenAI API)
* **Deterministic Risk Advising:** Ingests qualitative asset threats to evaluate business impacts, analyze likelihood/impact matrices, and prescribe mitigation strategies.
* **Cross-Framework Gap Analysis:** Leverages system-prompted LLM pipelines to review existing company documentation against targeted regulatory requirements, isolating control deficiencies.
* **Automated Evidence Review:** Simulates an internal auditor by evaluating submitted technical evidence against framework criteria, flagging insufficient artifacts, and suggesting explicit remediation documentation.
* **Zero Code Duplication:** Centralized orchestration layers ensure that raw LLM API completions, prompts, and connection handles live strictly within unified core engine files, allowing clean access from both background daemons and interactive UIs.

---

## 🔒 Core GRC Domain Focus

The platform is purpose-built to engineer and manage controls across critical cybersecurity and information technology risk profiles:

* **Identity & Access Management (IAM):** Strict tracking of user provisioning, role-based access control (RBAC), and least privilege enforcement.
* **Zero Trust & Cloud Security:** Infrastructure baseline monitoring, network segmentation tracking, and data security controls.
* **Vendor & Third-Party Risk Management (TPRM):** Managing vendor security postures, questionnaire evaluations, and SOC 2 readiness.
* **Vulnerability & Threat Management:** Continuous patching metrics, scanning tracking, and incident response plan testing.
* **Data Protection & Privacy:** Governance tracking for sensitive data retention, encryption standards, and business continuity readiness.

---

## Technology Stack & Project Structure

* **Core Language:** Python 3.11+
* **Database Engine:** SQLite (Relational Storage & Schema Optimization)
* **AI Integration:** OpenAI API (Advanced Prompt Engineering & Structured JSON Outputs)

```text
├── main.py                    # Application entry point & runtime loop
├── database.py                # SQLite connection layer, schema definition, & migrations
├── risk_register.py           # Risk data models, CRUD logic, and mathematical scoring
├── controls.py                # Control library indexing & structural definitions
├── ai_tools.py                # Interactive LLM workspace pipelines & prompt engineering
├── grc_agent.py               # Autonomous GRC Agent loops & background services hub
├── openai_helper.py           # API client initialization, payload validation, & error handling
├── grc_enterprise.db          # Live SQLite relational database 
├── audit_logger.py            # Append-only transaction log handler
├── generated_policies/        # Output directory for AI-engineered documentation
├── generated_reports/         # Output directory for management-ready compliance reports
└── README.md                  # System documentation