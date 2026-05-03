SELECT
  t.task_id,
  t.task_type,
  t.client_ref,
  sm.full_name,
  sm.clinic,
  qr.review_status,
  qr.issue_found
FROM tasks t
JOIN staff_members sm
  ON sm.staff_id = t.staff_id
LEFT JOIN proof_records pr
  ON pr.task_id = t.task_id
LEFT JOIN qa_reviews qr
  ON qr.task_id = t.task_id
WHERE t.status = 'completed'
  AND t.requires_proof = 1
  AND pr.task_id IS NULL
ORDER BY t.task_id;
