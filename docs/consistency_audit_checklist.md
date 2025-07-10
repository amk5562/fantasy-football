# ✅ Fantasy Football Data Project – Consistency Audit Checklist

This checklist is used to ensure consistency across all layers of the fantasy football BI system (schema, ETL, views, tests).

---

## 1. Schema Consistency
- [ ] All base tables are created in `schema.sql`
- [ ] All tables use consistent naming (`snake_case`, plural if row = entity)
- [ ] Foreign keys are declared with matching types
- [ ] Primary keys are composite where necessary (e.g. season + team)
- [ ] Views are not mistakenly defined as tables

## 2. ETL Consistency
- [ ] Each `load_*.py` script uses `get_valid_seasons()` to loop
- [ ] ETL scripts check for existing records before insert
- [ ] Error handling and logging follow the same format
- [ ] Field mappings are explicitly defined

## 3. View Consistency
- [ ] View definitions are stored in `sql/views/`
- [ ] View names match what they represent (e.g. `schedule_team_view`)
- [ ] Views join cleanly using existing foreign key relationships
- [ ] Views are drop-safe: `DROP VIEW IF EXISTS`

## 4. Test Consistency
- [ ] Tests confirm ETL scripts populate each table
- [ ] Sample queries validate expected record counts
- [ ] All `.sql` view files are re-runnable without error
- [ ] Tests exist to confirm data integrity (e.g. foreign key joins)

## 5. Data Integrity & QA
- [ ] All tables load successfully across all seasons
- [ ] Spot checks show expected values (e.g. no null player names)
- [ ] Queries use correct columns (e.g. `team_name` vs `team_id`)
- [ ] Lookups (e.g. player position, team name) match across years

---

_Last Updated: July 7, 2025_
