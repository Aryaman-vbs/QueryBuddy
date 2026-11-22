
import streamlit as st
import pandas as pd

from database import create_database, execute_readonly_query
from ai_engine import generate_sql, repair_sql
from sql_validator import validate_sql


# Page configuration
st.set_page_config(
    page_title="QueryBuddy",
    page_icon="🤖",
    layout="wide"
)

# Initialize database
create_database()

st.title("🤖 QueryBuddy")
st.subheader("Natural Language to SQL Assistant")

st.write(
    "Ask questions about your student database "
    "in plain English. QueryBuddy will generate SQL "
    "and execute it automatically."
)

# User input
question = st.text_area(
    "Enter your question:",
    placeholder="Example: Show all CSE students with CGPA above 8"
)

if st.button("Generate SQL & Execute"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Generating SQL..."):

            sql = generate_sql(question)

        if sql.startswith("AI_ERROR"):
            st.error(sql)

        elif sql.strip().upper() == "INVALID":
            st.warning("This question cannot be answered using the database.")

        else:
            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            is_valid, message = validate_sql(sql)

            if not is_valid:
                st.error(f"SQL validation failed: {message}")

            else:
                st.success("SQL validation successful")

                try:
                    columns, rows = execute_readonly_query(sql)

                    st.subheader("Query Results")

                    if rows:
                        df = pd.DataFrame(rows, columns=columns)
                        st.dataframe(df, use_container_width=True)
                        st.success(f"Total records: {len(rows)}")
                    else:
                        st.info("Query executed successfully. No records found.")

                except Exception as first_error:

                    st.warning(
                        "SQL execution failed. QueryBuddy is attempting "
                        "to repair the query automatically."
                    )

                    with st.spinner("Repairing SQL..."):

                        repaired_sql = repair_sql(
                            question,
                            sql,
                            str(first_error)
                        )

                    if repaired_sql.startswith("AI_ERROR"):
                        st.error(repaired_sql)

                    elif repaired_sql.strip().upper() == "INVALID":
                        st.error("QueryBuddy could not repair this query.")

                    else:
                        st.subheader("Repaired SQL")
                        st.code(repaired_sql, language="sql")

                        repair_valid, repair_message = validate_sql(
                            repaired_sql
                        )

                        if not repair_valid:
                            st.error(
                                f"Repaired SQL validation failed: "
                                f"{repair_message}"
                            )

                        else:
                            try:
                                columns, rows = execute_readonly_query(
                                    repaired_sql
                                )

                                st.success(
                                    "Query repaired and executed successfully!"
                                )

                                if rows:
                                    df = pd.DataFrame(rows, columns=columns)
                                    st.dataframe(
                                        df,
                                        use_container_width=True
                                    )
                                    st.success(
                                        f"Total records: {len(rows)}"
                                    )
                                else:
                                    st.info(
                                        "Query executed successfully. "
                                        "No records found."
                                    )

                            except Exception as second_error:
                                st.error(
                                    f"Automatic repair failed: {second_error}"
                                )

# Example questions
st.divider()
st.subheader("Example Questions")

examples = [
    "Show all students",
    "Show all CSE students",
    "Find students with CGPA above 8",
    "Count all students",
    "Find the average CGPA of CSE students",
    "List all available courses"
]

for example in examples:
    st.write(f"• {example}")
