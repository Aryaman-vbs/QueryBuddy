
import time
from google import genai

from config import GEMINI_API_KEY
from database import get_schema


# -----------------------------------------
# Gemini Configuration
# -----------------------------------------

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


# -----------------------------------------
# Clean Generated SQL
# -----------------------------------------

def clean_sql(response_text):
    """Remove Markdown code fences from generated SQL."""

    sql = response_text.strip()

    if sql.startswith("```sql"):
        sql = sql[6:]
    elif sql.startswith("```"):
        sql = sql[3:]

    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()


# -----------------------------------------
# Generate SQL
# -----------------------------------------

def generate_sql(question):
    """Convert a natural-language question into SQLite SQL."""

    schema = get_schema()

    prompt = f"""
You are QueryBuddy, an expert Text-to-SQL assistant.

Convert the user's question into a valid SQLite SELECT query.

DATABASE SCHEMA:
{schema}

RULES:
1. Use only the provided tables and columns.
2. Generate only SELECT statements.
3. Never generate INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, or other data-modifying statements.
4. Do not invent table or column names.
5. Use valid SQLite syntax.
6. If the question is ambiguous or cannot be answered
   using the schema, return INVALID.
7. Return only SQL without Markdown code fences.

USER QUESTION:
{question}
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if not response.text:
                return "AI_ERROR: Empty response from Gemini."

            return clean_sql(response.text)

        except Exception as error:
            error_message = str(error)

            is_overloaded = (
                "503" in error_message
                or "overloaded" in error_message.lower()
            )

            if is_overloaded and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue

            return f"AI_ERROR: {error_message}"

    return "AI_ERROR: Gemini request failed after retries."


# -----------------------------------------
# Repair Failed SQL
# -----------------------------------------

def repair_sql(question, failed_sql, error_message):
    """Ask Gemini to repair SQL after a database error."""

    schema = get_schema()

    prompt = f"""
You are QueryBuddy, an expert SQLite SQL debugging assistant.

A SQL query generated for the user failed during execution.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

FAILED SQL:
{failed_sql}

DATABASE ERROR:
{error_message}

TASK:
Correct the SQL query so it answers the original question.

RULES:
1. Use only the provided database schema.
2. Generate only a valid SQLite SELECT query.
3. Never generate INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, or other data-modifying statements.
4. Do not invent tables or columns.
5. Preserve the user's original intent.
6. If the query cannot be repaired, return INVALID.
7. Return only SQL without Markdown code fences.
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if not response.text:
                return "AI_ERROR: Empty repair response from Gemini."

            return clean_sql(response.text)

        except Exception as error:
            error_message = str(error)

            is_overloaded = (
                "503" in error_message
                or "overloaded" in error_message.lower()
            )

            if is_overloaded and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue

            return f"AI_ERROR: {error_message}"

    return "AI_ERROR: SQL repair failed after retries."


# -----------------------------------------
# Run Directly for Testing
# -----------------------------------------

if __name__ == "__main__":

    print("================================")
    print("       QueryBuddy SQL Engine")
    print("================================")

    user_question = input("\nEnter your question: ")

    generated_sql = generate_sql(user_question)

    print("\nGenerated SQL:")
    print(generated_sql)
