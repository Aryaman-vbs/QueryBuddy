
from database import create_database, execute_readonly_query
from ai_engine import generate_sql, repair_sql
from sql_validator import validate_sql

create_database()

question = input("Ask QueryBuddy: ")

# First SQL generation
sql = generate_sql(question)

if sql.startswith("AI_ERROR:"):
    print(sql)
    exit()

print("\nGenerated SQL:")
print(sql)

# First validation
valid, message = validate_sql(sql)

if not valid:
    print("\nQuery rejected:", message)
    exit()

# First execution
try:

    columns, rows = execute_readonly_query(sql)

except Exception as first_error:

    print("\nFirst execution failed:", first_error)
    print("\nAttempting automatic SQL repair...")

    # Ask Gemini to repair the query
    corrected_sql = repair_sql(
        question,
        sql,
        str(first_error)
    )

    if corrected_sql.startswith("AI_ERROR:"):
        print(corrected_sql)
        exit()

    if corrected_sql.strip().upper() == "INVALID":
        print("The query could not be repaired.")
        exit()

    print("\nCorrected SQL:")
    print(corrected_sql)

    # Validate repaired query
    valid, message = validate_sql(corrected_sql)

    if not valid:
        print("\nRepaired query rejected:", message)
        exit()

    # Second execution
    try:

        columns, rows = execute_readonly_query(corrected_sql)

    except Exception as second_error:

        print("\nRepair failed:", second_error)
        exit()

# Display results
print("\nQuery Results:")
print(columns)

for row in rows:
    print(row)

print(f"\nTotal records: {len(rows)}")
print("\nQueryBuddy completed successfully!")
