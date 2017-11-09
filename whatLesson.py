from config import *

def sayAboutLesson(mod = 's'):
    if(mod == 's'):
        return studentLesson()
    else:
        return teacherLesson()

def studentLesson():
    cursor = cnxn.cursor()
    cursor.execute("""
    SELECT TOP 1 WEEKDAY_NAME, START_TIME, END_TIME, PARITY, SUBJECT_NAME, TEACHER_NAME, CLASSROOM_NAME FROM LESSONS
    INNER JOIN WEEKDAYS ON WEEKDAYS.ID = WEEKDAYS_ID
    INNER JOIN LESSON_TIMES ON LESSON_TIME_ID = LESSON_TIMES.ID
    INNER JOIN SUBJECTS ON SUBJECTS.ID = SUBJECT_ID
    INNER JOIN TEACHERS ON TEACHERS.ID = TEACHER_ID
    INNER JOIN CLASSROOMS ON CLASSROOMS.ID = CLASSROOM_ID
    INNER JOIN GROUPS ON GROUP_ID = GROUPS.ID
    WHERE GROUP_NAME = N'Б3239а' AND
    (Parity = DATEPART(DW, CURRENT_TIMESTAMP + '10:00:00') % 2 OR PARITY = 2) AND
    (CONVERT(TIME, GETDATE() + '10:00:00')) <= START_TIME AND
    (DATEPART(weekday, GETDATE() + '10:00:00')) - 1 <= WEEKDAYS.ID
    ORDER BY WEEKDAYS.ID, START_TIME""")

    result_set = cursor.fetchall()
    return result_set[0][4] + " в " + result_set[0][6] + ", ведет " + result_set[0][5] + " c "+ str(result_set[0][1])[0:len(str(result_set[     0][1]))- 3] + " до " + str(result_set[0][2])[0:len(str(result_set[0][2])) - 3]

def teacherLesson():
    cursor = cnxn.cursor()
    cursor.execute("""
    SELECT TOP 1 WEEKDAY_NAME, START_TIME, END_TIME, PARITY, SUBJECT_NAME, GROUP_NAME, CLASSROOM_NAME FROM LESSONS
    INNER JOIN WEEKDAYS ON WEEKDAYS.ID = WEEKDAYS_ID
    INNER JOIN LESSON_TIMES ON LESSON_TIME_ID = LESSON_TIMES.ID
    INNER JOIN SUBJECTS ON SUBJECTS.ID = SUBJECT_ID
    INNER JOIN TEACHERS ON TEACHERS.ID = TEACHER_ID
    INNER JOIN CLASSROOMS ON CLASSROOMS.ID = CLASSROOM_ID
    INNER JOIN GROUPS ON GROUP_ID = GROUPS.ID
    WHERE TEACHER_NAME = N'Демидова Т.А.' AND
    (Parity = DATEPART(DW, CURRENT_TIMESTAMP + '10:00:00') % 2 OR PARITY = 2) AND
    (CONVERT(TIME, GETDATE() + '10:00:00')) <= START_TIME AND
    (DATEPART(weekday, GETDATE() + '10:00:00')) - 1 <= WEEKDAYS.ID
    ORDER BY WEEKDAYS.ID, START_TIME""")

    result_set = cursor.fetchall()
    return result_set[0][4] + " в " + result_set[0][6] + ", в группе " + result_set[0][5] + " c "+ str(result_set[0][1])[0:len(str(result_set[     0][1]))- 3] + " до " + str(result_set[0][2])[0:len(str(result_set[0][2])) - 3]
