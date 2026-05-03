SELECT
  t.task_id,
  t.task_type,
  t.client_ref,
  sm.full_name,
  sm.clinic,
  pr.proof_type,
  pr.captured_at,
  qr.review_status,
  qr.reviewed_at
FROM tasks t
JOIN staff_members sm
  ON sm.staff_id = t.staff_id
JOIN proof_records pr
  ON pr.task_id = t.task_id
LEFT JOIN qa_reviews qr
  ON qr.task_id = t.task_id
WHERE t.status = 'completed'
  AND t.requires_proof = 1
  AND (
    qr.review_status IS NULL
    OR qr.review_status = 'pending'
  )
ORDER BY t.task_id;
