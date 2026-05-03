import asyncio
import json
import os
import re
from typing import Any

import psycopg
from psycopg.rows import dict_row
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE_URL")
model = os.getenv("MODEL_NAME")
api_key = os.getenv("OPENAI_API_KEY", "does_not_matter")
database_url = os.getenv("DATABASE_URL")
dialect = os.getenv("DATABASE_DIALECT", "PostgreSQL")

BLOCKED_SQL = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|copy|call|execute|do|merge|vacuum|analyze|refresh|comment)\b",
    re.IGNORECASE,
)

ALLOWED_START = re.compile(r"^\s*(select|with)\b", re.IGNORECASE)


def _json_default(value: Any) -> str:
    return str(value)


@tool
def run_read_only_sql(query: str) -> str:
    """Run a read-only SQL SELECT/WITH query against the Postgres database and return rows as JSON."""
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set.")

    if not ALLOWED_START.search(query):
        return "REFUSED: Only SELECT or WITH queries are allowed."

    if BLOCKED_SQL.search(query):
        return "REFUSED: Query contains a blocked SQL keyword."

    query = query.strip().rstrip(";")

    try:
        with psycopg.connect(database_url, row_factory=dict_row, connect_timeout=10) as conn:
            with conn.cursor() as cur:
                cur.execute("SET statement_timeout = '10s';")
                cur.execute(query)
                rows = cur.fetchmany(200)
                return json.dumps(rows, default=_json_default, indent=2)
    except Exception as exc:
        return (
            "SQL_ERROR: "
            + exc.__class__.__name__
            + ": "
            + str(exc)
            + "\nInspect the relevant table columns, then rewrite the query using only real table and column names."
        )


system_prompt = f"""
You are a read-only SQL evidence agent for a {dialect} database.

Your job:
- answer questions only by using the run_read_only_sql tool
- inspect available tables before answering
- inspect relevant table columns before writing any business-answer query
- use only SELECT or WITH queries
- never invent table names
- never invent column names
- if a SQL_ERROR is returned, inspect schema and retry once with corrected column names
- never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, COPY, GRANT, REVOKE, or other write/destructive SQL
- if the database does not contain enough information, say that clearly
- cite the specific tables you used in your answer

Start by listing tables with:
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

Then inspect columns for the relevant tables with:
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;

Do not answer without querying the database.
"""


async def main():
    if not database_url:
        raise ValueError("Please set DATABASE_URL.")

    llm = init_chat_model(
        model,
        model_provider="openai",
        api_key=api_key,
        base_url=base_url,
    )

    agent = create_react_agent(
        llm,
        tools=[run_read_only_sql],
        prompt=system_prompt,
    )

    question = os.getenv("QUESTION")
    if not question:
        raise ValueError("Please set QUESTION.")

    async for step in agent.astream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()


asyncio.run(main())
