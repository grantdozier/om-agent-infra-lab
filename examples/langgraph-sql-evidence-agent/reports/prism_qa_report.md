# Prism QA Proof-Gap Report

## Purpose

Identify operational records that need human QA attention before report finalization.

## Summary

- Missing proof gaps: 1
- Proof exists but QA pending: 1

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

## Interpretation

- Missing-proof gaps need proof collection or task status correction.
- Pending-QA items need reviewer action before final reporting.

## Source Tables

- tasks
- staff_members
- proof_records
- qa_reviews
