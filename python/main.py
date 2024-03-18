import psycopg2
from datetime import datetime

# values to modify to establish the connection
database = "A3"
user = "postgres"
password = "postgres"
host = "localhost"
port = "5432"

# actual functionality starts here ############################
conn = psycopg2.connect(database = database, user = user, password = "postgres", host = host, port = port)

# function to check if date input is valid
def valid_date(date):
    try: # try creating a date object with the year, month, and date supplied
        year, month, day = map(int, date.split('-'))
        datetime(year=year, month=month, day=day)
        return True
    except ValueError: # if the object wasn't created, then the values were not valid
        return False

def getAllStudents(): 
    try:
        # get the rows using the cursor
        cur = conn.cursor()
        cur.execute('SELECT * FROM students;')

        # make a list of rows from the cursor
        rows = cur.fetchall()
        conn.commit()

        # print all the rows
        for row in rows:
            print(row)
        return True
    except:
        cur.close()
        return False

def addStudent(first_name, last_name, email, enrollment_date):
    try:
        # check if the date is valid
        if not valid_date(enrollment_date):
            print("Error: Please enter a valid enrollment date in the format YYYY-MM-DD.")
            return False

        # execute the INSERT statement using the cursor, then commit it
        cur = conn.cursor()
        cur.execute(f""" INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES 
                    ('{first_name}', '{last_name}', '{email}', '{enrollment_date}') """)

        conn.commit()
        return True
    except:
        cur.close()
        return False
    
def updateStudentEmail(student_id, new_email):
    try:
        cur = conn.cursor()

        # check if a student with the given id exists
        cur.execute(f"SELECT * FROM students WHERE student_id = {student_id}")
        existing_student = cur.fetchone() # only fetch one row since the id is unique, which means there can only ever be one result to the select statement

        # execute and commit the UPDATE statement
        if existing_student:
            cur.execute(f""" UPDATE students SET email = '{new_email}' WHERE student_id = '{student_id}' """)
            conn.commit()
            return True
    
    except:
        # if the function reaches this, then there was no row in the select statement
        print("There is no student with this ID.")
        cur.close()
        return False

def deleteStudent(student_id):
    try:
        cur = conn.cursor()

        # check if a student with the given id exists
        cur.execute(f"SELECT * FROM students WHERE student_id = {student_id}")
        existing_student = cur.fetchone() # only fetch one row since the id is unique, which means there can only ever be one result to the select statement

        # execute and commit the DELETE statement
        if existing_student:
            cur.execute(f"""DELETE FROM students WHERE student_id = {student_id}""")
            conn.commit()
            return True
    
    except:
        # if the function reaches this, then there was no row in the select statement
        print("There is no student with this ID.")
        cur.close()
        return False

# main control loop to get user inputs and call functions

loop = True

while loop == True:

    # reset the connection for every loop
    conn.close()
    conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
    

    print()
    print("Options:")
    print("1: Retrieve and display all records from the students table.")
    print("2: Insert a new student record into the students table.")
    print("3: Update the email address for a student with the specified student_id.")
    print("4: Deletes the record of the student with the specified student_id.")
    print("q: Exit the program.")

    user_input = input("Please enter your selection: ")
    print()

    # call a function based on the input of the user, or quit for input 'q'

    # the nested if statements are used for checking if the functions return true, which means that the execution went through properly
    # each function returns true or false based on a try-except block

    if user_input == "1":
        getAllStudents()
    elif user_input == "2":
        first_name = input("New student's first name: ")
        last_name = input("New student's last name: ")
        email = input("New student's email: ")
        enrollment_date = input("New student's enrollment date (format is YYYY-MM-DD): ")

        if(addStudent(first_name, last_name, email, enrollment_date)):
            print("The table, after these modifications: ")
            getAllStudents()

    elif user_input == "3":
        student_id = input("ID of student to update: ")
        email = input("Updated email of student: ")

        if(updateStudentEmail(student_id, email)):
            print("The table, after these modifications: ")
            getAllStudents()

    elif user_input == "4":
        student_id = input("ID of student to delete: ")

        if(deleteStudent(student_id)):
            print("The table, after these modifications: ")
            getAllStudents()

    elif user_input == "q":
        loop = False
    else:
        print("Please enter a valid selection.")