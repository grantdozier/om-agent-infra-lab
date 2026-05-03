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

query = Path("prism_gap_check.sql").read_text()

cmd = COMPOSE + [
    "exec", "-T", "database",
    "psql", "-U", "user", "-d", "database",
    "--csv", "-c", query,
]

result = subprocess.run(cmd, check=True, capture_output=True, text=True)

rows = list(csv.DictReader(result.stdout.splitlines()))

lines = [
    "# Prism QA Proof-Gap Report",
    "",
    "## Check",
    "",
    "Completed tasks where proof is required but no proof record exists.",
    "",
    "## Result",
    "",
]

if not rows:
    lines.append("No proof gaps found.")
else:
    lines.append(f"{len(rows)} proof gap(s) found.")
    lines.append("")
    lines.append("| Task ID | Task Type | Client Ref | Staff | Clinic | QA Status | Issue |")
    lines.append("|---:|---|---|---|---|---|---|")
    for row in rows:
        lines.append(
            f"| {row['task_id']} | {row['task_type']} | {row['client_ref']} | "
            f"{row['full_name']} | {row['clinic']} | {row['review_status']} | {row['issue_found']} |"
        )

lines.extend([
    "",
    "## Interpretation",
    "",
    "These rows require human QA review before report finalization.",
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
