# Prism QA Proof-Gap Report

## Purpose

Identify operational records that need human QA attention before report finalization.

## Summary

- Missing proof gaps: 1
- Proof exists but QA pending: 1
- Overdue in-progress tasks: 1

---

## Check 1 — Completed Tasks Missing Required Proof

Completed tasks where proof is required but no proof record exists.

1 missing-proof gap(s) found.

| Task ID | Task Type | Client Ref | Staff | Clinic | QA Status | Issue |
|---:|---|---|---|---|---|---|
| 102 | billing_followup | CLIENT-002 | Avery Landry | Lafayette Clinic | needs_fix | Task marked complete but no proof record exists. |

---

## Check 2 — Completed Tasks With Proof But Pending QA

Completed proof-required tasks where proof exists but QA review is missing or pending.

1 pending-QA item(s) found.

| Task ID | Task Type | Client Ref | Staff | Clinic | Proof Type | Captured At | QA Status | Reviewed At |
|---:|---|---|---|---|---|---|---|---|
| 104 | care_plan_update | CLIENT-004 | Morgan Guidry | Crowley Clinic | chart_snapshot | 2026-05-03T09:40:00 | pending |  |

---

## Check 3 — In-Progress Tasks Past Due Date

Tasks still marked in progress after their due date, as of reporting date 2026-05-03.

1 overdue in-progress task(s) found.

| Task ID | Task Type | Client Ref | Staff | Clinic | Due Date | Status |
|---:|---|---|---|---|---|---|
| 103 | chart_review | CLIENT-003 | Morgan Guidry | Crowley Clinic | 2026-05-02 | in_progress |

---

## Interpretation

- Missing-proof gaps need proof collection or task status correction.
- Pending-QA items need reviewer action before final reporting.
- Overdue in-progress tasks need owner follow-up or status correction.

## Source Tables

- tasks
- staff_members
- proof_records
- qa_reviews
