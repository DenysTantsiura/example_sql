/*The example shows various uses 
of some similar commands (sequence)*/

-- Table: students
DROP TABLE IF EXISTS students;
CREATE TABLE students (
  id INT UNSIGNED PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(50) NOT NULL,
  group_id INT UNSIGNED,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT students_name_un UNIQUE KEY (name),
  FOREIGN KEY (group_id) REFERENCES groups (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);		
			
-- Table: groups
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
  id INT UNSIGNED PRIMARY KEY AUTOINCREMENT,
  group_name CHAR(10) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);		
		
-- Table: teachers
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
  id INT UNSIGNED PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT teachers_name_uq UNIQUE KEY (name)
);			
			
-- Table: subjects
DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
  id INT UNSIGNED PRIMARY KEY AUTOINCREMENT,
  subject CHAR(30), 
  teacher_id INT UNSIGNED,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);			
				
-- Table: assessments
DROP TABLE IF EXISTS assessments;
CREATE TABLE assessments (
  id INT UNSIGNED PRIMARY KEY AUTOINCREMENT, 
  value_ TINYINT UNSIGNED NOT NULL, 
  date_of DATE NOT NULL,
  subject_id INT UNSIGNED, 
  student_id INT UNSIGNED,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (subject_id) REFERENCES subjects (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,       
  FOREIGN KEY (student_id) REFERENCES students (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);					
	