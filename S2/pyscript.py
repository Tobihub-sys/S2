import sqlite3
import datetime

def connect_to_database():
    return sqlite3.connect('school.db')

def is_valid_date(date_str, format='%Y-%m-%d'):
    try:
        datetime.datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def insert_initial_lessons():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Check if lessons table is empty
    cursor.execute("SELECT COUNT(*) FROM lessons")
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert initial lessons
        cursor.execute("INSERT INTO lessons (lesson_name) VALUES ('Math')")
        cursor.execute("INSERT INTO lessons (lesson_name) VALUES ('Science')")
        cursor.execute("INSERT INTO lessons (lesson_name) VALUES ('English')")

        conn.commit()
        print("Initial lessons inserted into the lessons table.")
    else:
        print("Lessons table already contains data. Skipping insertion.")

    conn.close()

def add_student():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Get student information from user with input validation
    while True:
        name = input("Enter student name: ")
        if name.isalpha():
            break
        else:
            print("Invalid input. Name must contain only letters.")

    while True:
        nickname = input("Enter student nickname: ")
        if nickname.isalpha():
            break
        else:
            print("Invalid input. Nickname must contain only letters.")
    
    # Validate age input
    while True:
        try:
            age = int(input("Enter student age: "))
            break
        except ValueError:
            print("Invalid input. Age must be a number.")

    grade = input("Enter student grade: ")
    
    # Validate registration date input
    while True:
        registration_date_input = input("Enter registration date (DD/MM/YYYY): ")
        try:
            registration_date = datetime.datetime.strptime(registration_date_input, '%d/%m/%Y').strftime('%Y-%m-%d')
            if is_valid_date(registration_date):
                break
            else:
                print("Invalid date. Please enter a valid date.")
        except ValueError:
            print("Invalid date format. Please enter date in DD/MM/YYYY format.")

    # Display available lessons for the user to choose
    cursor.execute("SELECT * FROM lessons")
    lessons = cursor.fetchall()
    print("Available Lessons:")
    for lesson in lessons:
        print(f"{lesson[0]}: {lesson[1]}")

    # Get lesson_id from user
    while True:
        try:
            lesson_id = int(input("Enter the lesson_id for the student: "))
            break
        except ValueError:
            print("Invalid input. Lesson ID must be a number.")

    # Insert student information into the students table
    cursor.execute('''
        INSERT INTO students (name, nickname, age, grade, registration_date, lesson_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, nickname, age, grade, registration_date, lesson_id))

    conn.commit()
    conn.close()
    print("Student added successfully.")

def delete_student():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Get student_id from user with input validation
    while True:
        try:
            student_id = int(input("Enter the student_id of the student to delete: "))
            break
        except ValueError:
            print("Invalid input. Student ID must be a number.")

    # Delete student from the students table
    cursor.execute('''
        DELETE FROM students WHERE student_id = ?
    ''', (student_id,))

    conn.commit()
    conn.close()
    print("Student deleted successfully.")

def update_student():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Get student_id from user with input validation
    while True:
        try:
            student_id = int(input("Enter the student_id of the student to update: "))
            break
        except ValueError:
            print("Invalid input. Student ID must be a number.")

    # Get existing student information
    cursor.execute('''
        SELECT * FROM students WHERE student_id = ?
    ''', (student_id,))
    student_data = cursor.fetchone()

    if student_data:
        # Display current student information
        print("Current Student Information:")
        print(f"Name: {student_data[1]}")
        print(f"Nickname: {student_data[2]}")
        print(f"Age: {student_data[3]}")
        print(f"Grade: {student_data[4]}")
        print(f"Registration Date: {student_data[5]}")
        print(f"Lesson ID: {student_data[6]}")

        # Get updated student information from user with input validation
        name = input("Enter updated student name (press Enter to keep current): ") or student_data[1]
        nickname = input("Enter updated student nickname (press Enter to keep current): ") or student_data[2]
        
        while True:
            try:
                age = int(input("Enter updated student age (press Enter to keep current): ") or student_data[3])
                break
            except ValueError:
                print("Invalid input. Age must be a number.")
                
        grade = input("Enter updated student grade (press Enter to keep current): ") or student_data[4]
        
        while True:
            registration_date = input("Enter updated registration date (YYYY-MM-DD) (press Enter to keep current): ") or student_data[5]
            if is_valid_date(registration_date):
                break
            else:
                print("Invalid date format. Please enter date in YYYY-MM-DD format.")

        # Display available lessons for the user to choose
        cursor.execute("SELECT * FROM lessons")
        lessons = cursor.fetchall()
        print("Available Lessons:")
        for lesson in lessons:
            print(f"{lesson[0]}: {lesson[1]}")

        # Get updated lesson_id from user with input validation
        while True:
            try:
                lesson_id = int(input("Enter updated lesson_id for the student (press Enter to keep current): ") or student_data[6])
                break
            except ValueError:
                print("Invalid input. Lesson ID must be a number.")

        # Update student information in the students table
        cursor.execute('''
            UPDATE students
            SET name=?, nickname=?, age=?, grade=?, registration_date=?, lesson_id=?
            WHERE student_id=?
        ''', (name, nickname, age, grade, registration_date, lesson_id, student_id))

        conn.commit()
        print("Student updated successfully.")
    else:
        print(f"No student found with student_id {student_id}")

    conn.close()

def view_student():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Get student_id from user with input validation
    while True:
        try:
            student_id = int(input("Enter the student_id of the student to view: "))
            break
        except ValueError:
            print("Invalid input. Student ID must be a number.")

    # Retrieve student information including the associated lesson
    cursor.execute('''
        SELECT students.*, lessons.lesson_name
        FROM students
        INNER JOIN lessons ON students.lesson_id = lessons.lesson_id
        WHERE student_id = ?
    ''', (student_id,))
    
    student_info = cursor.fetchone()

    if student_info:
        print("Student Information:")
        print(f"Student ID: {student_info[0]}")
        print(f"Name: {student_info[1]}")
        print(f"Nickname: {student_info[2]}")
        print(f"Age: {student_info[3]}")
        print(f"Grade: {student_info[4]}")
        print(f"Registration Date: {student_info[5]}")
        print(f"Lesson ID: {student_info[6]}")
        print(f"Lesson Name: {student_info[7]}")
    else:
        print(f"No student found with student_id {student_id}")

    conn.close()

# Call the function to insert initial lessons
insert_initial_lessons()

# Main loop
while True:
    print("Options:")
    print("a: Add student")
    print("d: Delete student")
    print("u: Update student")
    print("v: View student information")
    print("q: Quit")

    choice = input("Enter your choice: ").lower()

    if choice == 'a':
        add_student()
    elif choice == 'd':
        delete_student()
    elif choice == 'u':
        update_student()
    elif choice == 'v':
        view_student()
    elif choice == 'q':
        break
    else:
        print("Invalid choice. Please try again.")
