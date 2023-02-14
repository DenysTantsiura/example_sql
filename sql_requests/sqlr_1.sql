/*
Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
*/
SELECT students.name, ROUND(avg(assessments.value_), 1)
FROM assessments INNER JOIN students
ON assessments.student_id = students.id
GROUP BY students.id
ORDER BY avg(assessments.value_)
DESC LIMIT 5
