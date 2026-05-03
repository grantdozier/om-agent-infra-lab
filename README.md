# OM Agent Infra Lab

This repo is a local research lab for testing governed AI-agent infrastructure patterns before anything touches a production OM, Prism, or LA.IO repo.

## Current working example

examples/langgraph-sql-evidence-agent/

## Why this exists

This lab proves a simple operating rule:

SQL proves.
Markdown reports.
Agents explain.
Humans decide.

The goal is not to build a full app here.

The goal is to test safe, small, repeatable infrastructure patterns for:

- structured operational data
- deterministic proof checks
- QA/QC reporting
- read-only agent access
- human-reviewed outputs

This supports the Prism operating loop:

Evidence → Task → Proof → QA/QC → Report

## What has been proven

The lab currently proves this repeatable loop:

SQLite toy data
→ Postgres import
→ deterministic SQL checks
→ markdown QA report
→ one-command runner

The current QA report checks:

1. Completed tasks that require proof but have no proof record.
2. Completed tasks where proof exists but QA review is missing or pending.

The latest successful run found:

- Missing proof gaps: 1
- Proof exists but QA pending: 1

## How to run the Prism QA report

From the repo root:

cd examples/langgraph-sql-evidence-agent
./run_prism_qa_report.sh

The script will:

1. start Postgres in Docker
2. import PrismToy.db
3. run deterministic SQL checks
4. generate a markdown report
5. print the report
6. shut down the containers

The report is written to:

examples/langgraph-sql-evidence-agent/reports/prism_qa_report.md

## Key files

examples/langgraph-sql-evidence-agent/PrismToy.db
Synthetic SQLite source data.

examples/langgraph-sql-evidence-agent/prism_gap_check.sql
Finds completed proof-required tasks missing proof records.

examples/langgraph-sql-evidence-agent/prism_pending_qa_check.sql
Finds completed proof-required tasks where proof exists but QA is pending or missing.

examples/langgraph-sql-evidence-agent/generate_prism_qa_report.py
Runs the SQL checks and writes the markdown report.

examples/langgraph-sql-evidence-agent/run_prism_qa_report.sh
One-command runner for the full reporting loop.

examples/langgraph-sql-evidence-agent/agent.py
Experimental read-only SQL agent. This is not the proof layer.

## Architecture rule

Do not treat the LLM as the source of truth.

Use this separation:

Postgres = truth layer
SQL checks = proof layer
Markdown = report layer
Agent = explanation layer
Human = decision layer

## Safety rules

- Use synthetic or non-sensitive data only.
- Do not connect live healthcare, founder, Airtable, or OM production data yet.
- Do not allow agent writes.
- Do not let generated summaries overwrite source records.
- Keep raw data, canonical data, and derived reports separate.
- Prefer deterministic SQL checks before adding agent behavior.

## Current status

Working.

The lab has already generated a QA report showing:

- one missing-proof task
- one pending-QA task

Next recommended slice:

Add Check 3 — in-progress tasks past due date.

After that, this lab can become a reusable pattern for Prism, OM Venture OS, and LA.IO Overwatch reporting workflows.
