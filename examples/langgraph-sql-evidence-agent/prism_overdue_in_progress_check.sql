-- Requires the psql variable reporting_date, e.g.:
--   psql -v reporting_date=2026-05-03 -f prism_overdue_in_progress_check.sql
-- generate_prism_qa_report.py supplies it from the REPORTING_DATE
-- environment variable, defaulting to the lab value 2026-05-03.
SELECT
  t.task_id,
  t.task_type,
  t.client_ref,
  sm.full_name,
  sm.clinic,
  t.due_date,
  t.status
FROM tasks t
JOIN staff_members sm
  ON sm.staff_id = t.staff_id
WHERE t.status = 'in_progress'
  AND t.due_date < :'reporting_date'
ORDER BY t.due_date, t.task_id;
