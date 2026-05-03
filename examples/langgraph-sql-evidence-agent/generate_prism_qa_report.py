import csv
import subprocess
from pathlib import Path

COMPOSE = [
    "docker", "compose",
    "-f", "compose.yaml",
    "-f", "compose.local.yaml",
    "-f", "compose.direct-sql.yaml",
    "-f", "compose.prism-toy.yaml",
]

REPORT_PATH = Path("reports/prism_qa_report.md")
REPORT_PATH.parent.mkdir(exist_ok=True)


def run_sql_file(path: str) -> list[dict[str, str]]:
    query = Path(path).read_text()
    cmd = COMPOSE + [
        "exec", "-T", "database",
        "psql", "-U", "user", "-d", "database",
        "--csv", "-c", query,
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return list(csv.DictReader(result.stdout.splitlines()))


proof_gap_rows = run_sql_file("prism_gap_check.sql")
pending_qa_rows = run_sql_file("prism_pending_qa_check.sql")
overdue_rows = run_sql_file("prism_overdue_in_progress_check.sql")

lines = [
    "# Prism QA Proof-Gap Report",
    "",
    "## Purpose",
    "",
    "Identify operational records that need human QA attention before report finalization.",
    "",
    "## Summary",
    "",
    f"- Missing proof gaps: {len(proof_gap_rows)}",
    f"- Proof exists but QA pending: {len(pending_qa_rows)}",
    f"- Overdue in-progress tasks: {len(overdue_rows)}",
    "",
    "---",
    "",
    "## Check 1 — Completed Tasks Missing Required Proof",
    "",
    "Completed tasks where proof is required but no proof record exists.",
    "",
]

if not proof_gap_rows:
    lines.append("No missing-proof gaps found.")
else:
    lines.append(f"{len(proof_gap_rows)} missing-proof gap(s) found.")
    lines.append("")
    lines.append("| Task ID | Task Type | Client Ref | Staff | Clinic | QA Status | Issue |")
    lines.append("|---:|---|---|---|---|---|---|")
    for row in proof_gap_rows:
        lines.append(
            f"| {row['task_id']} | {row['task_type']} | {row['client_ref']} | "
            f"{row['full_name']} | {row['clinic']} | {row['review_status']} | {row['issue_found']} |"
        )

lines.extend([
    "",
    "---",
    "",
    "## Check 2 — Completed Tasks With Proof But Pending QA",
    "",
    "Completed proof-required tasks where proof exists but QA review is missing or pending.",
    "",
])

if not pending_qa_rows:
    lines.append("No pending-QA proof records found.")
else:
    lines.append(f"{len(pending_qa_rows)} pending-QA item(s) found.")
    lines.append("")
    lines.append("| Task ID | Task Type | Client Ref | Staff | Clinic | Proof Type | Captured At | QA Status | Reviewed At |")
    lines.append("|---:|---|---|---|---|---|---|---|---|")
    for row in pending_qa_rows:
        lines.append(
            f"| {row['task_id']} | {row['task_type']} | {row['client_ref']} | "
            f"{row['full_name']} | {row['clinic']} | {row['proof_type']} | "
            f"{row['captured_at']} | {row['review_status'] or 'missing'} | {row['reviewed_at'] or ''} |"
        )

lines.extend([
    "",
    "---",
    "",
    "## Check 3 — In-Progress Tasks Past Due Date",
    "",
    "Tasks still marked in progress after their due date.",
    "",
])

if not overdue_rows:
    lines.append("No overdue in-progress tasks found.")
else:
    lines.append(f"{len(overdue_rows)} overdue in-progress task(s) found.")
    lines.append("")
    lines.append("| Task ID | Task Type | Client Ref | Staff | Clinic | Due Date | Status |")
    lines.append("|---:|---|---|---|---|---|---|")
    for row in overdue_rows:
        lines.append(
            f"| {row['task_id']} | {row['task_type']} | {row['client_ref']} | "
            f"{row['full_name']} | {row['clinic']} | {row['due_date']} | {row['status']} |"
        )

lines.extend([
    "",
    "---",
    "",
    "## Interpretation",
    "",
    "- Missing-proof gaps need proof collection or task status correction.",
    "- Pending-QA items need reviewer action before final reporting.",
    "- Overdue in-progress tasks need owner follow-up or status correction.",
    "",
    "## Source Tables",
    "",
    "- tasks",
    "- staff_members",
    "- proof_records",
    "- qa_reviews",
])

REPORT_PATH.write_text("\n".join(lines) + "\n")
print(REPORT_PATH)
