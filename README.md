

# 🏈 Fantasy Football BI System

This is a full-stack Business Intelligence (BI) portfolio project that analyzes over a decade of ESPN fantasy football data to uncover trends, behaviors, and insights. It was built to demonstrate the complete BI skill set, from data architecture to predictive modeling, tailored to the expectations of roles in Business Intelligence and Data Analysis.

---

## 📌 Project Overview

This project turns a fantasy football league into a modern BI system that supports:

- Historical league analysis (2012–2024)
- Predictive modeling (draft value)
- Executive dashboards and weekly storylines
---

## 🎯 Business Intelligence Framework

This project is structured around BI best practices:

- **Hybrid BI**: Descriptive 📊 + Predictive 🤖 + Storytelling 📖
- **6-Phase Roadmap**:
  1. Planning
  2. Design (ERD + KPIs)
  3. ETL (multi-season pipeline)
  4. Analysis (SQL views, modeling)
  5. Visualization (dashboard mockups)
  6. Communication (readable insights)

---

## 🛠️ Technical Stack

- **Database**: SQLite (DB Browser)
- **ETL**: Python + ESPN API
- **Modeling**: SQL Views, CTEs, Window Functions
- **Visualization**: Dashboard planning with Looker / Power BI
- **Version Control**: Git + GitHub

---

## 🔄 ETL + Data Architecture

Built a custom multi-season ETL pipeline to ingest:

- Matchups, box scores, rosters, draft results
- Transactions, playoff seeds, team metadata
- Custom enrichment views (e.g. is_playoff, draft_with_names)

All tables are documented and linked via a structured Entity-Relationship Diagram (ERD).

---

## 📊 KPIs & Dashboards

Tracked performance via dashboards:

- Core Roster Retention %
- Draft Value Over Expected
- Transaction Load / Team
- Blowout Wins / Losses
- Owner Loyalty Score (multi-year consistency)

See: [`docs/kpis_and_dashboards.md`](docs/kpis_and_dashboards.md)

---

## 🔍 Analytical & Predictive Insights

Example insights include:

- Predicting owner success based on draft
- Positional draft trends over time (declining RB value, etc.)

---

## 🧠 Storytelling Capabilities

Generated weekly and seasonal stories using SQL + custom views:

- Who got lucky/unlucky this week?
- What players kept showing up on the same team?
- How has each franchise evolved over time?

---

## 🧪 How to Run the Project

1. Clone the repo  
   `git clone https://github.com/amk5562/fantasy-football.git`

2. Set up virtual environment  
   `python -m venv venv && source venv/bin/activate`

3. Install dependencies  
   `pip install -r requirements.txt`

4. Run ETL  
   `python etl/load_teams.py` (or run all load_*.py scripts)

5. Explore DB using DB Browser or SQLite shell

---

## 📂 Project Structure

```
fantasy-football/
├── db/                        # SQLite database
├── docs/                      # BI prompt, KPIs, roadmap
├── etl/                       # ETL scripts per table
├── sql/                       # Views and queries
├── visualizations/ (future)  # Dashboard mockups
├── README.md
```

---

## 👤 Author

**Aran Kirwan**  
Business Intelligence Portfolio | [GitHub @amk5562](https://github.com/amk5562)  
Seeking BI Analyst roles in education, sports, or strategic analytics