# Prompt Iteration Log – QueryBuddy

## Objective
The purpose of prompt iteration was to improve the accuracy, reliability and safety of converting natural-language questions into executable SQLite queries.

### Version 1 – Basic SQL Generation

**Prompt approach:**  
The initial prompt instructed the language model to convert a user's natural-language question into an SQL query.

**Prompt:**
```text
Convert the following natural-language question into
a valid SQL query.

Question: {question}

Return only the SQL query.
```

**Changes introduced:**  
- Established the basic natural-language-to-SQL workflow.
- Kept the prompt simple, without providing database schema context or examples.

**Observed result:**  
The model was able to generate a query for a straightforward question. However, the output could include formatting such as Markdown code fences, and the prompt did not sufficiently constrain table and column selection.

### Version 2 – Schema-Aware SQL Generation

**Prompt approach:**  
The second version introduced database schema information and explicit SQL generation rules.

**Prompt:**
```text
You are an expert Text-to-SQL assistant.
Convert the user's question into a valid SQLite query.

DATABASE SCHEMA:
{schema}

RULES:
1. Use only the tables and columns in the schema.
2. Generate only SELECT statements.
3. Do not generate destructive SQL commands.
4. Follow valid SQLite syntax.
5. Return only the SQL query.

USER QUESTION:
{question}
```

**Changes introduced:**
- Added the database schema as context.
- Restricted generation to SELECT statements.
- Added rules against destructive SQL.
- Specified SQLite syntax and schema compliance.

**Observed result:**  
The generated query became more relevant to the available database structure. The model was better guided to use valid table and column names, reducing the risk of unsupported SQL references.

### Version 3 – Example-Based and Error-Aware Prompting

**Prompt approach:**  
The third version introduced examples and additional instructions for ambiguous or invalid questions.

**Prompt:**
```text
You are QueryBuddy, an expert Text-to-SQL assistant.
Convert natural-language questions into valid SQLite queries.

DATABASE SCHEMA:
{schema}

EXAMPLES:

Question: Show all CSE students.
SQL: SELECT * FROM students WHERE department = 'CSE';

Question: Count all students.
SQL: SELECT COUNT(*) AS total_students FROM students;

Question: Find the average CGPA of CSE students.
SQL: SELECT AVG(cgpa) AS average_cgpa
FROM students WHERE department = 'CSE';

RULES:
1. Use only the provided database schema.
2. Generate only SELECT statements.
3. Never generate destructive SQL.
4. Use correct SQLite syntax.
5. Never invent columns or tables.
6. If a question is ambiguous or cannot be answered,
   return INVALID.
7. Return only the SQL query.

USER QUESTION:
{question}
```

**Changes introduced:**
- Added few-shot examples to demonstrate the expected SQL format.
- Added instructions for ambiguous or unsupported questions.
- Strengthened schema restrictions and output requirements.

**Observed result:**  
The examples provided clearer guidance for generating SQL queries. The model produced more structured SQL output, although Markdown formatting could still appear in some responses. The application therefore uses SQL-cleaning logic to handle formatting before validation.

### Final Prompt – Integrated QueryBuddy Workflow

The final generation prompt incorporated the improvements from the previous versions, including schema awareness, examples, SQLite-specific rules, SELECT-only restrictions and invalid-question handling.

A separate SQL repair prompt was also implemented. It receives the original question, failed SQL query, execution error and database schema to request a corrected query.

**Final improvements:**
- More structured SQL generation.
- Better alignment with the actual database schema.
- Read-only query restrictions.
- Example-guided generation.
- Handling of ambiguous or unsupported questions.
- A separate repair workflow for correcting SQL execution errors.

**Conclusion:**  
Prompt iteration improved the structure and constraints of SQL generation in QueryBuddy. The final implementation uses two distinct LLM prompts: one for SQL generation and another for SQL error repair. SQL validation and read-only execution provide additional safeguards beyond prompt instructions.
