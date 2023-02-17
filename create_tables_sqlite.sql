/*The example shows various uses 
    of some similar commands (sequence)*/

-- Table: groups_ --[groups] -- keyword
DROP TABLE IF EXISTS groups_; 
CREATE TABLE groups_ (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  group_name CHAR(10) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: students
DROP TABLE IF EXISTS students;
CREATE TABLE students (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name VARCHAR(50) NOT NULL,
  -- group_id INTEGER,
  group_id REFERENCES groups_ (id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP --,
  -- CONSTRAINT students_name_un UNIQUE KEY (name),
  /*FOREIGN KEY (group_id) REFERENCES groups_ (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE*/
);

-- Table: teachers
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name VARCHAR(50) NOT NULL,
  -- CONSTRAINT teachers_name_uq UNIQUE KEY (name),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
			
-- Table: subjects
DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  subject CHAR(30), 
  teacher_id INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);			
				
-- Table: assessments
DROP TABLE IF EXISTS assessments;
CREATE TABLE assessments (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
  value_ TINYINT UNSIGNED NOT NULL, 
  date_of DATE NOT NULL,
  subject_id INTEGER, 
  student_id INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (subject_id) REFERENCES subjects (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,       
  FOREIGN KEY (student_id) REFERENCES students (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);					
	