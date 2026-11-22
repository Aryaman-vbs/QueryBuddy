
from database import create_database, execute_readonly_query
from ai_engine import repair_sql
from sql_validator import validate_sql

create_database()

question = "Show all CSE students with CGPA above 8"

# Deliberately incorrect SQL
failed_sql = """
SELECT * FROM student
WHERE department = 'CSE' AND cgpa > 8;
"""

print("Original SQL:")
print(failed_sql)

try:
    execute_readonly_query(failed_sql)

except Exception as error:

    print("\nDatabase error:", error)
    print("\nAsking Gemini to repair SQL...")

    corrected_sql = repair_sql(
        question,
        failed_sql,
        str(error)
    )

    print("\nCorrected SQL:")
    print(corrected_sql)

    if corrected_sql.startswith("AI_ERROR:"):
        print("Repair API failed.")
        exit()

    valid, message = validate_sql(corrected_sql)

    print("\nValidation:", message)

    if not valid:
        print("Corrected query rejected.")
        exit()

    try:
        columns, rows = execute_readonly_query(corrected_sql)

        print("\nRepaired query executed successfully!")

        for row in rows:
            print(row)

        print("\nTotal records:", len(rows))

    except Exception as final_error:
        print("Repair execution failed:", final_error)
