# 🧠 Master Prompt: Fantasy Football BI Project

I want to build a **searchable, story-driven fantasy football database** for my private ESPN-hosted league (dating back to 2012), following best practices in **Business Intelligence** using a **Hybrid + Predictive + Storytelling framework**. 

🎯 **The Goal**:  
To analyze drafts, trades, players, and teams/owners while also writing league history and generating weekly stories during the season.

---

## ✅ 1. Modern Data Architecture

- 💻 I’m using **macOS Sequoia 15.5** and **Safari**.
- 🐍 My environment includes **Python 3.10**, managed in a `venv` virtual environment.
- 🗃️ I will use **SQLite** as the database engine, accessed via **DB Browser** and Python.
- 🗂️ I want a **predefined folder structure** as follows:

fantasy-football-data/
├── app/
├── data/
│   ├── raw/
│   └── processed/
├── db/
│   └── fantasy_football.db
├── docs/
│   ├── prompt.md
│   ├── roadmap.md
│   ├── schema.md
│   ├── metrics.md
│   ├── model_eval.md
│   ├── data_dictionary.md
│   └── etl_pipeline.md
├── etl/
├── notebooks/
├── sql/
│   ├── schema.sql
│   ├── seed.sql
│   └── queries/
├── tests/
│   └── test_db_connection.py
├── requirements.txt
├── README.md
└── .gitignore

---

## ✅ 2. Semantic Layer & Metric Definition

- 📊 I am using **Looker** as my BI tool.
- ✅ I want to define reusable **metrics** via SQL views and/or LookML.
- 🏆 **First 3 Core KPIs**:
  1. **Champion** – which team won each season
  2. **Loser** – which team finished last each season
  3. **Favorite Player** – the player each owner started the most across all seasons

📘 Please create:
- A **metrics dictionary** and glossary in `docs/metrics.md`.

---

## ✅ 3. Predictive Analytics Integration

- 🤖 I want to use **scikit-learn** for predictive modeling.
- 📈 The first model will **predict trade value or trade outcome impact**.
- 💾 Store predictions in a table (e.g., `predictions_trade_value`) and make them available in dashboards and stories.
- 🔁 Retrain models weekly and evaluate accuracy/performance.

🧾 Please document:
- Modeling workflow and evaluation in `docs/model_eval.md`.

---

## ✅ 4. Storytelling & Narrative Dashboards

- 📚 I want to support both **manual** and **automated** story generation.
- 📝 **Story Types** will include:
  - Draft analysis (“steal of the draft”, “biggest bust”)
  - Weekly recaps
  - Championship narratives
  - Rivalry matchups and trades

📂 Stories should be:
- Saved as **Markdown files**
- Indexed in a **`stories` table** with fields like: `type`, `week`, `season`, `title`, `content`

📊 In Looker, dashboards should support **drill-down**:
`Season Summary → Team → Player → Story`

---

## ✅ 5. Governance + Flexibility

- 🧑‍💻 I am working solo, but I want **light governance**.
- Please implement:
  - A **data dictionary** in `docs/data_dictionary.md`
  - Filters for `season`, `team`, `week`, `player`
  - ETL logging and error tracking
  - Use **semantic layers** and shared definitions to avoid inconsistencies

---

## ✅ 6. Automation & BI Ops

- ⏱️ I want to **automate weekly ETL and model refreshes** using `cron` on macOS.
- 🧪 Add **unit tests** for ETL and model validation in the `tests/` folder.
- 🔁 I will **version control** all code and documentation with **GitHub**.

📘 Please document:
- Automation setup in `docs/etl_pipeline.md`

---

## Final Objective

Build a **full-stack BI solution** that allows me to **explore, analyze, and narrate the history** of my fantasy football league. This project should support both **analytical queries** and **human storytelling** — and grow over time with **automated insights** and **league-wide legacy analysis**.