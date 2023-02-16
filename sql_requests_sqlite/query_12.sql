/*
Оцінки студентів у певній групі з певного предмета на останньому занятті.
*/
SELECT
  a.value_ AS Assessment, 
  s.name AS Student,
  g.group_name AS Group_,
  sub.subject AS Subject
FROM
  assessments AS a
  JOIN
  subjects AS sub
  ON a.subject_id = sub.id
  JOIN
  students AS s
  ON a.student_id = s.id
  JOIN
  groups AS g
  ON s.group_id = g.id
WHERE Group_ = 'Group-2' AND Subject = 'History' --AND a.date_of = MAX(a.date_of)
GROUP BY Student
ORDER BY a.date_of DESC;
