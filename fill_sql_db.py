from collections import Counter
from datetime import datetime
import logging
from random import randint
import sqlite3
from timeit import default_timer

from faker import Faker
from faker.providers import DynamicProvider


NUMBER_OF_GROUPS = 3
NUMBER_OF_STUDENTS = randint(30, 50)
NUMBER_OF_TEACHERS = randint(3, 5)
NUMBER_OF_SUBJECTS = randint(5, 8)
NUMBER_OF_ASSESSMENTS = randint(1, 20) * NUMBER_OF_SUBJECTS * NUMBER_OF_STUDENTS

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')


def duration(fun):
    """Decorator for counting duration."""
    def inner(*args, **kwargs):
        start = default_timer()
        rez = fun(*args, **kwargs)
        logging.info(f'{default_timer()-start=} sec.')

        return rez

    return inner


def fake_data_generator() -> tuple():
    """Generate fake data about students assessments."""
    fake_data = Faker()
    
    #fake_groups = []
    fake_students = [fake_data.name() for _ in range(NUMBER_OF_STUDENTS)]
    fake_teachers = [fake_data.name() for _ in range(NUMBER_OF_TEACHERS)]
    #fake_subjects = []
    #fake_assessments = []
    
    groups_provider = DynamicProvider(
             provider_name='group',
             elements=[list(range(1, NUMBER_OF_GROUPS))],
        )
        
    fake_data.add_provider(groups_provider)
    
    subjects_provider = DynamicProvider(
             provider_name='subjects',
             elements=['Mathematics', 'Economics', 'Physics', 'History',],
        )

    # then add new provider to faker instance
    fake_data.add_provider(subjects_provider)
    
    assessments_provider = DynamicProvider(
             provider_name='assessments',
             elements=[list(range(1, 6))],
        )
                        
    fake_data.add_provider(assessments_provider)	
        
    fake_assessments = [fake_data.assessment() for _ in range(NUMBER_OF_ASSESSMENTS)]

    fake_subjects = [fake_data.subjects() for _ in range(len(subjects_provider.elements))]
    [result.append(fake_data.job()) 
        for _ in range(randint(1, NUMBER_OF_SUBJECTS - len(subjects_provider.elements)))]
    
    fake_groups = [f'Group-{fake_data.group()}' for _ in range(NUMBER_OF_GROUPS)]	

    return fake_groups, fake_students, fake_teachers, fake_subjects, fake_assessments


def prepare_data_to_insert(groups: list, students: list, teachers: list, subjects: list, assessments: list) -> tuple():
    """Converting list data to list of tuples."""
    for_groups = [(group,) for group in groups]
    for_teachers = [(teacher,) for teacher in teachers]
    for_students = [(student, randint(1, NUMBER_OF_GROUPS)) for student in students]
    for_subjects = [(subject, randint(1, NUMBER_OF_TEACHERS)) for subject in subjects]
    for_assessments = [
        (value, 
        datetime(2023, 2, randint(1, 28)).date(), 
        randint(1, NUMBER_OF_SUBJECTS), 
        randint(1, NUMBER_OF_STUDENTS)) 
        for value in assessments]
        
    # до 20 оцінок у кожного студента з усіх предметів:
    def new_student_id():
        return randint(1, NUMBER_OF_STUDENTS)
        
    for_assessments = []
    for value in assessments:
        student_id = new_student_id()
        while Counter(elem[3] for elem in for_assessments).get(student_id, 0) > 19:  # Counter({'12392': 2, '7862': 1})
            student_id = new_student_id()
            
        for_assessments.append(value, 
                        datetime(2023, 2, randint(1, 28)).date(), 
                        randint(1, NUMBER_OF_SUBJECTS), 
                        student_id)

    return for_groups, for_teachers, for_students, for_subjects, for_assessments
    

def insert_data_to_db(groups: list, teachers: list, students: list, subjects: list, assessments: list) -> None:
    """Insertind data to DataBase."""
    # Створимо з'єднання з нашою БД та отримаємо об'єкт курсору для маніпуляцій з даними
    with sqlite3.connect('assessments.db') as connection_to_db:
		active_cursor = connection_to_db.cursor()	
        
        sql_to_groups = """INSERT INTO groups(group_name)
                           VALUES (?)"""
        active_cursor.executemany(sql_to_groups, groups)
        
        sql_to_teachers = """INSERT INTO teachers(name)
                           VALUES (?)"""
        active_cursor.executemany(sql_to_teachers, teachers)
        
        sql_to_students = """INSERT INTO students(name, group_id)
                           VALUES (?, ?)"""
        active_cursor.executemany(sql_to_students, students)
        
        sql_to_subjects = """INSERT INTO subjects(subject, teacher_id)
                           VALUES (?, ?)"""
        active_cursor.executemany(sql_to_subjects, subjects)
        
        sql_to_assessments = """INSERT INTO assessments(value_, date_of, subject_id, student_id)
                           VALUES (?, ?)"""
        active_cursor.executemany(sql_to_assessments, assessments)
        
        # Фіксуємо наші зміни в БД
        connection_to_db.commit()
        

@duration
def main():
    groups, teachers, students, subjects, assessments = prepare_data_to_insert(*fake_data_generator())
    insert_data_to_db(groups, teachers, students, subjects, assessments)


if __name__ == "__main__":
    main()





