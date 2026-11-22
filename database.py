
import sqlite3

DB_NAME = "querybuddy.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            cgpa REAL,
            year INTEGER
        )
    """)

    # Courses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY,
            title TEXT,
            department TEXT,
            credits INTEGER
        )
    """)

    # Enrollments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            student_id INTEGER,
            course_id INTEGER,
            grade TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(course_id) REFERENCES courses(course_id)
        )
    """)

    # Sample student records
    cursor.executemany("""
        INSERT OR IGNORE INTO students
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, "Rahul", "CSE", 8.7, 3),
        (2, "Aman", "CSE", 9.1, 2),
        (3, "Priya", "CSE", 8.4, 3),
        (4, "Neha", "ECE", 7.9, 2),
        (5, "Arjun", "IT", 8.2, 3),
        (6, "Riya", "ECE", 9.0, 4),
        (7, "Karan", "CSE", 7.5, 1),
        (8, "Simran", "IT", 8.9, 4)
    ])

    # Sample courses
    cursor.executemany("""
        INSERT OR IGNORE INTO courses
        VALUES (?, ?, ?, ?)
    """, [
        (101, "Database Management", "CSE", 4),
        (102, "Computer Networks", "CSE", 3),
        (103, "Digital Electronics", "ECE", 4),
        (104, "Machine Learning", "CSE", 4)
    ])

    # Sample enrollments
    cursor.executemany("""
        INSERT INTO enrollments
        SELECT ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM enrollments
            WHERE student_id = ? AND course_id = ?
        )
    """, [
        (1, 101, "A", 1, 101),
        (1, 102, "B", 1, 102),
        (2, 101, "A", 2, 101),
        (3, 104, "A", 3, 104),
        (4, 103, "B", 4, 103),
        (5, 101, "A", 5, 101),
        (6, 103, "A", 6, 103),
        (7, 102, "C", 7, 102),
        (8, 104, "A", 8, 104)
    ])

    conn.commit()
    conn.close()


def get_schema():
    return """
    students(student_id, name, department, cgpa, year)
    courses(course_id, title, department, credits)
    enrollments(student_id, course_id, grade)
    """


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")
    print(get_schema())

def execute_readonly_query(sql):
    conn = sqlite3.connect(
        "file:querybuddy.db?mode=ro",
        uri=True
    )

    try:
        cursor = conn.execute(sql)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        return columns, rows

    finally:
        conn.close()
