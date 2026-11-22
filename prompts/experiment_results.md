
# QueryBuddy Prompt Experiment Results

## Experiment 1

Input:
Show all CSE students with CGPA above 8.

V1:
SELECT * FROM students WHERE department = 'CSE' AND cgpa > 8;

V2:
SELECT student_id, name, department, cgpa, year
FROM students
WHERE department = 'CSE' AND cgpa > 8;

V3:
SELECT * FROM students WHERE department = 'CSE' AND cgpa > 8;

Observations:
- All three versions generated logically correct SQL.
- V1 and V3 used SELECT *.
- V2 explicitly selected the required columns.
- All three used the correct department and CGPA conditions.

## Further experiments

Test 2: [Add actual outputs]
Test 3: [Add actual outputs]
Test 4: [Add actual outputs]
Test 5: [Add actual outputs]

