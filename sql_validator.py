
import re

def validate_sql(sql):

    if not sql or not sql.strip():
        return False, "Empty SQL query"

    sql = sql.strip()

    # Only SELECT statements allowed
    if not re.match(r"^SELECT\b", sql, re.IGNORECASE):
        return False, "Only SELECT queries are allowed"

    # Block dangerous SQL operations
    forbidden = [
        "INSERT", "UPDATE", "DELETE",
        "DROP", "ALTER", "CREATE",
        "TRUNCATE", "REPLACE",
        "ATTACH", "DETACH", "PRAGMA"
    ]

    for keyword in forbidden:
        if re.search(rf"\b{keyword}\b", sql, re.IGNORECASE):
            return False, f"Forbidden SQL operation: {keyword}"

    # Reject multiple statements
    cleaned_sql = sql.rstrip(";").strip()

    if ";" in cleaned_sql:
        return False, "Multiple SQL statements are not allowed"

    return True, "SQL validation successful"


if __name__ == "__main__":

    test_queries = [
        "SELECT * FROM students;",
        "DELETE FROM students;",
        "DROP TABLE students;"
    ]

    for query in test_queries:
        valid, message = validate_sql(query)
        print(query, "->", valid, message)
