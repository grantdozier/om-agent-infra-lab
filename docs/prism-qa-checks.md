# Prism QA Checks Contract

This document defines the deterministic QA checks used in the Prism-style agent infrastructure lab.

The purpose is to separate proof from explanation.

SQL checks identify operational records that need attention.
Markdown reports make those findings readable.
Agents may explain findings, but agents do not decide truth.
Humans review and act.

## Core Rule

SQL proves.
Markdown reports.
Agents explain.
Humans decide.

## Data Flow

1. Synthetic source data starts in `PrismToy.db`.
2. Docker imports the SQLite database into Postgres.
3. SQL checks query Postgres.
4. `generate_prism_qa_report.py` turns check results into markdown.
5. `run_prism_qa_report.sh` runs the full loop.
6. A human reviews the output.

## Source Tables

| Table | Role |
|---|---|
| `tasks` | Operational work records |
| `staff_members` | Staff ownership and clinic context |
| `proof_records` | Evidence that work was completed |
| `qa_reviews` | Human QA review status and findings |
| `reports` | Draft reporting artifact metadata |

---

## Check 1 — Completed Tasks Missing Required Proof

### SQL file

`examples/langgraph-sql-evidence-agent/prism_gap_check.sql`

### What it flags

Completed tasks where:

- `tasks.status = 'completed'`
- `tasks.requires_proof = 1`
- no matching row exists in `proof_records`

### Why it matters

A completed task that requires proof should not move into final reporting without evidence.

This check catches records where the task status says “done,” but the proof layer does not support that status.

### Source tables

- `tasks`
- `staff_members`
- `proof_records`
- `qa_reviews`

### Flag meaning

A row in this check means:

- the task may be missing documentation
- the task may be incorrectly marked completed
- the proof may exist somewhere else but has not been linked
- QA should not treat the record as report-ready yet

### Human action

Review the source system and decide whether to:

1. add the missing proof record
2. correct the task status
3. mark the QA issue as unresolved
4. escalate to the staff owner

### False-positive risks

This check may flag a record even when proof exists outside the structured table.

Examples:

- proof is in email
- proof is in an EHR
- proof is in a spreadsheet
- proof was captured but not linked to the task

The correct response is not automatic failure.
The correct response is human review.

---

## Check 2 — Completed Tasks With Proof But Pending QA

### SQL file

`examples/langgraph-sql-evidence-agent/prism_pending_qa_check.sql`

### What it flags

Completed proof-required tasks where:

- `tasks.status = 'completed'`
- `tasks.requires_proof = 1`
- a matching row exists in `proof_records`
- QA review is missing or `qa_reviews.review_status = 'pending'`

### Why it matters

Proof exists, but the record still needs human QA review before final reporting.

This separates “proof captured” from “proof accepted.”

### Source tables

- `tasks`
- `staff_members`
- `proof_records`
- `qa_reviews`

### Flag meaning

A row in this check means:

- the task has evidence
- the evidence has not been fully reviewed
- the record should stay out of final approval until QA acts

### Human action

Review the proof and decide whether to:

1. approve the QA review
2. request a fix
3. reject the proof
4. ask the staff owner for clarification

### False-positive risks

This check may flag a task if QA was completed in another system but not synced.

The data contract should eventually require QA status to be normalized into `qa_reviews`.

---

## Check 3 — In-Progress Tasks Past Due Date

### SQL file

`examples/langgraph-sql-evidence-agent/prism_overdue_in_progress_check.sql`

### What it flags

Tasks where:

- `tasks.status = 'in_progress'`
- `tasks.due_date` is before the reporting date used by the check

The reporting date is a psql variable (`reporting_date`).

The report generator sets it from the `REPORTING_DATE` environment variable.

Default lab value (keeps runs deterministic against the synthetic data):

`2026-05-03`

To run against a different cutoff, for example today:

`REPORTING_DATE=$(date +%F) ./run_prism_qa_report.sh`

The generated report states which reporting date was used.

### Why it matters

A task that is still in progress after its due date needs follow-up.

This catches operational drift before reports are finalized.

### Source tables

- `tasks`
- `staff_members`

### Flag meaning

A row in this check means:

- work may be overdue
- the task status may be stale
- the staff owner may need follow-up
- report readiness may be blocked

### Human action

Review the task and decide whether to:

1. update the task status
2. revise the due date
3. request proof
4. escalate the blocker
5. exclude the task from final reporting until resolved

### False-positive risks

The reporting date is parameterized, so the check can run against:

- today
- a reporting period end date

A single run still applies one reporting date to every row.

Clinic-specific cutoffs or payer-specific deadlines would need per-row reporting dates sourced from the data, not a single run-level value.

---

## Report Output

Generated report:

`examples/langgraph-sql-evidence-agent/reports/prism_qa_report.md`

The report currently includes:

- summary counts
- Check 1 results
- Check 2 results
- Check 3 results
- interpretation
- source tables

## Acceptance Standard

A QA report is acceptable when:

- each row is traceable to source tables
- each finding comes from deterministic SQL
- each check has a clear human action
- no generated interpretation overwrites source data
- unresolved findings remain visible

## Non-Negotiables

- Do not let an LLM decide whether a task is valid.
- Do not let a generated summary become canonical data.
- Do not hide missing proof.
- Do not mark pending QA as approved.
- Do not overwrite raw records.
- Do not connect live sensitive data in this lab.

## Next Recommended Checks

Potential future checks:

1. tasks completed after due date
2. proof captured after completion date
3. QA rejected but task still marked completed
4. missing staff owner
5. duplicate proof records
6. report generated while unresolved QA findings exist
7. task owner with repeated unresolved proof gaps

## Pattern for Adding a New Check

For every new check, add:

1. one SQL file
2. one report section
3. one expected finding in synthetic data
4. one human action definition
5. one false-positive note
6. one commit

The check should be deterministic before any agent behavior is added.
