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
  AND t.due_date < '2026-05-03'
ORDER BY t.due_date, t.task_id;
