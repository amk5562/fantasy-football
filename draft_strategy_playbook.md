# 🧠 Fantasy Football Draft Strategy Playbook (BI Edition)

## 1. Business Questions

**Main Question:**  
How can I optimize my draft strategy to maximize long-term fantasy team success?

**Sub-questions:**
- How does draft position impact available value?
- What’s the opportunity cost of keeping a player vs. drafting new talent?
- When do positional drop-offs typically occur by round?
- Which managers consistently draft well (and which don’t)?
- What trends can I exploit from past drafts (stacking, positional runs, undervalued players)?

---

## 2. KPIs & Metrics

| KPI | Description |
|-----|-------------|
| **Draft ROI** | Final season finish vs. average draft position (ADP) of picks |
| **Positional Value** | Average points per round by position |
| **Keeper Efficiency** | Cost of keeper vs. points gained compared to others |
| **Pick Hit Rate** | % of picks who finish top-10 in their position |
| **ADP vs. Outcome Delta** | How often a player outperforms or underperforms draft slot |

---

## 3. Data Sources

- `draft_results_view` – draft pick data by year and team
- `standings_view` – final season outcomes
- `players` – position and pro team for each player
- `box_scores` – weekly player performance (points scored)
- [To add] ADP data from ESPN, FantasyPros, or Sleeper
- [To add] 2025 keeper predictions and scoring projections

---

## 4. Models & Scenarios

| Model | Description |
|-------|-------------|
| **Keeper Inflation Model** | Estimate value lost when a keeper occupies a Round 1 pick, using reverse draft order logic to map true draft opportunity. |
| **Actual Draft Start Model** | Shows which pick in Round 2 corresponds to the first new selection in the draft. |
| **Adjusted ROI Model** | Subtract keeper pick slots from ROI calculations so we don’t penalize teams for unavoidable keeper costs. |
| **Game Theory Heatmap** | Predict other teams' likely strategies using past draft behavior |
| **Positional Drop-Off Model** | Identify when value tiers break for each position |
| **Roster Construction Score** | Measure how balanced or optimized a draft is by position |
| **Optimal Path Tree** | Simulate pick combinations and strategic outcomes |
| **Draft Start Logic Model** | Adjusts draft analysis to reflect that keepers always fill Round 1 and occur in reverse draft order |
| **Keeper-Adjusted ROI Model** | Measures ROI while excluding Round 1 (keeper) picks from the calculation to isolate true draft value |

---

## 5. Visualizations (Dashboard Mockups)

| Chart Type | Insight |
|------------|---------|
| 📈 Line Chart | Value by draft pick over time |
| 🧊 Heatmap | Roster strength distribution by team and year |
| 📐 Slopegraph | Keeper round vs. performance (points scored) |
| 🧱 Bar Chart | Best-performing rounds per owner |
| 🧠 Decision Tree | Simulated first 3 rounds based on keeper pool |

---



## 6. Strategic Recommendations

### 🧠 How to Win the Draft and the Season (With Game Theory)

**Story Goal:**  
Understand how draft decisions drive season outcomes and use that insight to outperform opponents.

**Narrative Summary:**  
- Review past drafts to analyze how each owner's picks contributed to their season finish.
- Identify key differentiators between successful and unsuccessful drafters (e.g., positional value, hit rate, over-reliance on certain strategies).
- Use ROI and hit rate metrics to isolate which decisions correlate with success.
- Implement game theory by modeling opponent tendencies and simulating likely draft paths based on keeper structure and historical patterns.
- Build a draft strategy that not only maximizes personal value but also exploits predictable behaviors from other managers.

---

## 📌 Project Roadmap: "How to Win the Draft and the Season"

### 1. Planning Phase
**Business Questions:**
- Which draft picks have led to higher season finishes?
- What drafting behaviors separate strong drafters from weak ones?
- How do keepers affect early round opportunity?
- What can I predict about other owners' picks based on past behavior?
- How can I counter those tendencies to improve my outcomes?

---

### 2. Design Phase
**Views to Create:**
- `draft_tendencies_by_owner`
- `keeper_rounds`
- `adjusted_draft_results`
- `positional_value_by_round`

**Models to Build:**
- Keeper Inflation Model
- Game Theory Draft Path Simulator
- Owner Strategy Profiles
- Optimal Counter Paths

---

### 3. ETL Phase
- Extend the ETL process to generate `draft_tendencies_by_owner`
- Aggregate picks by round, position, and owner
- Normalize across seasons

---

### 4. Analysis Phase
**Key Questions:**
- Who benefits most from keepers?
- Which owners follow consistent draft habits?
- When do positional runs occur?
- How do draft starts correlate with season success?

---

### 5. Visualization Phase
**Planned Charts:**
- Heatmap: Draft tendencies by round and position
- Bar chart: Best/worst draft ROI seasons
- Decision tree: Optimal round paths
- Snake draft simulation: Positional runs and impact

---

### 6. Communication Phase
**Deliverables:**
- A notebook/report answering: “How can I beat my league through smarter draft strategy?”
- Owner-by-owner profiles and counter-strategy
- Draft day playbook with tiers and simulations
