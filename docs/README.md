# AI-Powered GRC Manager

A Python-based Governance, Risk, and Compliance (GRC) platform that simulates many of the core capabilities found in commercial GRC solutions. This project was built to strengthen both my Python programming skills and my understanding of enterprise risk management, cybersecurity governance, compliance, and AI-assisted workflows.

The application combines traditional risk management functionality with OpenAI-powered tools that assist with risk analysis, framework guidance, policy generation, evidence review, and reporting.

---

# Features

## Risk Management

- Create, view, edit, and delete risks
- Search for risks
- View detailed Risk Profiles
- Track likelihood, impact, risk score, and risk level
- Assign risk owners
- Document treatment plans
- Track risk status and target completion dates

## Control Management

- Create, view, edit, and delete controls
- Search for controls
- Link multiple controls to a single risk
- View all controls associated with a risk
- Many-to-many risk/control relationships

## AI Workspace (OpenAI Powered)

### AI Risk Advisor

- Analyze operational and cybersecurity risks
- Recommend preventive, detective, and corrective controls
- Identify business impacts
- Suggest treatment strategies
- Recommend audit evidence

### Framework Assistant

- Explain cybersecurity and compliance frameworks
- Assist with:
  - NIST CSF
  - ISO 27001
  - SOC 2
  - PCI DSS
  - NPDES
  - SCAQMD
  - Custom frameworks

### Control Builder

- Generate controls for existing risks
- Recommend control type
- Save generated controls directly into the control library
- Automatically map controls to risks

### Policy Generator

- Generate policies and procedures from identified risks
- Support both industrial operations and cybersecurity scenarios

### Evidence Review

- Review submitted audit evidence
- Identify evidence gaps
- Recommend additional supporting documentation

### Report Writer

- Generate executive risk summaries
- Summarize risk posture
- Highlight high-risk items
- Produce management-ready reports

---

# Reporting & Analysis

- Risk Dashboard
- Risk Statistics
- Open vs Closed Risks
- Risk Level Distribution
- Average Risk Score
- Highest Risk Score
- Upcoming Risks
- Overdue Risks
- Risk Heat Map

---

# Technologies Used

- Python 3
- OpenAI API
- CSV Data Storage
- Modular Python Architecture
- Git
- GitHub

---

# Project Structure

```
main.py
risk_register.py
controls.py
ai_tools.py
openai_helper.py
database.py
risk_register.csv
controls_library.csv
risk_control_mapping.csv
generated_policies/
generated_reports/
README.md
```

---

# Skills Demonstrated

## Python

- Modular application architecture
- CRUD operations
- File management
- Error handling
- Input validation
- Data modeling
- Menu-driven CLI development

## Governance, Risk & Compliance

- Enterprise Risk Management
- Risk Register Development
- Control Library Management
- Risk-to-Control Mapping
- Risk Assessment Methodology
- Risk Treatment Planning
- Control Evaluation
- Audit Evidence Management
- Executive Reporting

## Cybersecurity

- Identity & Access Management
- Vulnerability Management
- Incident Response
- Security Awareness
- Third-Party Risk
- Data Protection
- Cloud Security
- Security Framework Mapping

## Artificial Intelligence

- OpenAI API Integration
- AI-assisted Risk Analysis
- AI-generated Policies
- AI-generated Controls
- AI-assisted Evidence Review
- AI-generated Executive Reports

---

# Sample Risk Domains

The application includes realistic sample data from two industries.

### Industrial Operations

- Gas Turbine Reliability
- Boiler Systems
- Steam Systems
- SCADA
- Environmental Compliance
- NPDES
- CEMS
- Process Safety
- Electrical Reliability
- Confined Space Safety

### Cybersecurity / GRC

- Identity & Access Management
- Vendor Risk
- Cloud Security
- Vulnerability Management
- Data Protection
- Phishing
- Incident Response
- Backup Recovery
- Security Awareness
- Compliance

---

# Future Roadmap

## Phase 3 — Agentic AI Workflows

- Autonomous Risk Assessments
- Automated Control Recommendations
- Framework Mapping
- Compliance Gap Analysis
- Continuous Risk Monitoring
- AI-assisted Audit Preparation
- Multi-step AI Workflows

## Future Enhancements

- SQLite Database
- User Authentication
- PDF Report Generation
- Audit Logging
- Web Interface
- Dashboard UI
- Evidence Uploads
- Workflow Automation

---

# About This Project

This project was developed as part of my transition into Governance, Risk, and Compliance (GRC).

My goal is to build a portfolio-quality application that demonstrates practical software development skills while solving realistic GRC problems faced by organizations.

Rather than simply learning Python or studying GRC frameworks independently, I chose to build an application that integrates enterprise risk management concepts, cybersecurity controls, OpenAI-powered analysis, and modern software design principles into a single platform.

The long-term vision is to evolve this project from a command-line application into a full AI-assisted GRC platform with agentic workflows, automated compliance analysis, and enterprise reporting capabilities.