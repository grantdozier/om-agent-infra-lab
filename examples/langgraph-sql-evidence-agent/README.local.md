# LangGraph SQL Evidence Agent Lab

Purpose:
Test Dockerized agent patterns for querying structured operational data through MCP and Postgres.

Use cases:
- Prism evidence → task → proof → QA/QC → report
- OM founder evidence → assumptions → patterns → readiness
- LA.IO Overwatch sources → mentions → verified signals → reporting summaries

Rules:
- Lab only.
- Do not copy directly into production.
- Do not connect sensitive data yet.
- Test with synthetic or exported non-sensitive data first.
- Preserve raw data, canonical data, and derived answers as separate layers.
- Agent may query truth; agent does not own truth.
