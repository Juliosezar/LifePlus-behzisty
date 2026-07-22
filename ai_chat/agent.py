from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from django.conf import settings
from .schema_context import SCHEMA_CONTEXT
import re
import datetime


def _get_db():
    db_url = (
        f"postgresql+psycopg2://{settings.DATABASES['readonly']['USER']}"
        f":{settings.DATABASES['readonly']['PASSWORD']}"
        f"@{settings.DATABASES['readonly']['HOST']}"
        f":{settings.DATABASES['readonly']['PORT']}"
        f"/{settings.DATABASES['readonly']['NAME']}"
    )
    return SQLDatabase.from_uri(
        db_url,
        include_tables=[
            'cases_case',
            'cases_casefamilymembers',
            'cases_disability',
            'cases_reasoncase',
            'cases_recoveredreasoncase',
            'cases_casenotes',
            'cases_casedocuments',
            'cases_visit',
            'cases_demands',
            'cases_services_provided',
        ],
        sample_rows_in_table_info=0,
    )


SQL_GENERATION_PROMPT = SCHEMA_CONTEXT + """

You are a SQL query generator. Given a user question, generate a PostgreSQL SELECT query.
Return ONLY the SQL query, nothing else. No explanations, no markdown, no backticks.
The query must be a valid PostgreSQL SELECT statement.

Important:
- Use the exact table and column names from the schema above.
- For the table structure, use `cases_case` as the main table.
- Respond ONLY with the SQL query."""

# - Always use LIMIT 100 for queries that return rows (not aggregates).

def ask_question(question, history=""):
    """Ask a natural language question and get back (reply, sql_query, result_rows, columns)."""
    llm = ChatOpenAI(
        model=settings.NINEROUTER_MODEL,
        openai_api_key=settings.NINEROUTER_API_KEY,
        openai_api_base=settings.NINEROUTER_BASE_URL,
        temperature=0,
        max_tokens=5000,
        request_timeout=60,
    )
    db = _get_db()

    # Step 1: Generate SQL from the question
    prompt = f"{SQL_GENERATION_PROMPT}\n\nUser question: {question}"
    if history:
        prompt = f"Previous context:\n{history}\n\n{prompt}"

    sql_response = llm.invoke(prompt)
    sql_query = sql_response.content.strip()

    # Clean up: remove markdown code blocks if present
    sql_query = re.sub(r'^```sql\s*', '', sql_query)
    sql_query = re.sub(r'^```\s*', '', sql_query)
    sql_query = re.sub(r'\s*```$', '', sql_query)
    sql_query = sql_query.strip()

    # Validate it's a SELECT
    if not sql_query.upper().startswith('SELECT'):
        return {
            'reply': 'متأسفانه نتوانستم کوئری SQL مناسبی تولید کنم. لطفاً سوال خود را واضح‌تر مطرح کنید.',
            'sql_query': sql_query,
            'result': [],
            'columns': [],
        }

    # Step 2: Execute the SQL directly with SQLAlchemy
    rows = []
    columns = []
    try:
        from sqlalchemy import create_engine, text
        db_url = (
            f"postgresql+psycopg2://{settings.DATABASES['readonly']['USER']}"
            f":{settings.DATABASES['readonly']['PASSWORD']}"
            f"@{settings.DATABASES['readonly']['HOST']}"
            f":{settings.DATABASES['readonly']['PORT']}"
            f"/{settings.DATABASES['readonly']['NAME']}"
        )
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            columns = list(result.keys())
            for row in result.fetchall():
                rows.append({
                    col: (val.isoformat() if isinstance(val, (datetime.datetime, datetime.date)) else str(val) if val is not None and not isinstance(val, (int, float, bool, str)) else val)
                    for col, val in zip(columns, row)
                })
        engine.dispose()
    except Exception as e:
        return {
            'reply': f'خطا در اجرای کوئری: {str(e)}',
            'sql_query': sql_query,
            'result': [],
            'columns': [],
        }

    # Step 4: Generate a Persian summary
    row_count = len(rows)
    sample = str(rows[0])[:200] if rows else "empty"
    summary_prompt = f"User asked: {question}\nSQL query: {sql_query}\nResult: {row_count} rows. Sample: {sample}\n\nWrite a SHORT Persian summary (1-2 sentences). Do NOT include any tables, lists, or data rows."
    summary_response = llm.invoke(summary_prompt)
    reply = summary_response.content.strip()
    reply = re.sub(r'\*\*(.+?)\*\*', r'\1', reply)

    return {
        'reply': reply,
        'sql_query': sql_query,
        'result': rows,
        'columns': columns,
    }
