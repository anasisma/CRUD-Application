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

def createTable():

    try: 
        cur = conn.cursor()

        # creating the table
        cur.execute(""" CREATE TABLE students (
            student_id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            enrollment_date DATE
        ); """)

        # populating the table
        cur.execute(""" INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
        ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
        ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
        ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02'); """)
        conn.commit()
    except:
        print("The table already exists in this database!")

    

# function to check if date input is valid
def valid_date(date):
    try: # try creating a date object with the year, month, and date supplied
        year, month, day = map(int, date.split('-'))
        datetime(year=year, month=month, day=day)
        return True
    except ValueError: # if the object wasn't created, then the values were not valid
        return False

# function to check if the table exists, before doing any operations on it
def check_table_existence(): 
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM students;')
        conn.commit()
        return True
    except:
        print("Please create the table before executing any statements!")
        cur.close()
        return False

def getAllStudents(): 
    # get the rows using the cursor
    cur = conn.cursor()
    cur.execute('SELECT * FROM students;')

    # make a list of rows from the cursor
    rows = cur.fetchall()
    conn.commit()

    # print all the rows
    for row in rows:
        print(row)

def addStudent(first_name, last_name, email, enrollment_date): 
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
    
def updateStudentEmail(student_id, new_email):
    cur = conn.cursor()

    # check if a student with the given id exists
    cur.execute(f"SELECT * FROM students WHERE student_id = {student_id}")
    existing_student = cur.fetchone() # only fetch one row since the id is unique, which means there can only ever be one result to the select statement

    # execute and commit the UPDATE statement
    if existing_student:
        cur.execute(f""" UPDATE students SET email = '{new_email}' WHERE student_id = '{student_id}' """)
        conn.commit()
        return True
    
    # if the function reaches this, then there was no row in the select statement
    print("There is no student with this ID.")
    return False

def deleteStudent(student_id):
    cur = conn.cursor()

    # check if a student with the given id exists
    cur.execute(f"SELECT * FROM students WHERE student_id = {student_id}")
    existing_student = cur.fetchone() # only fetch one row since the id is unique, which means there can only ever be one result to the select statement

    # execute and commit the DELETE statement
    if existing_student:
        cur.execute(f"""DELETE FROM students WHERE student_id = {student_id}""")
        conn.commit()
        return True
    
    # if the function reaches this, then there was no row in the select statement
    print("There is no student with this ID.")
    return False

# main control loop to get user inputs and call functions

loop = True

while loop == True:

    # reset the connection for every loop
    conn.close()
    conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
    

    print()
    print("Options:")
    print("0: Create and populate the students table.")
    print("1: Retrieve and display all records from the students table.")
    print("2: Insert a new student record into the students table.")
    print("3: Update the email address for a student with the specified student_id.")
    print("4: Deletes the record of the student with the specified student_id.")
    print("q: Exit the program.")

    user_input = input("Please enter your selection: ")
    print()

    # call a function based on the input of the user, or quit for input 'q'
    # if the user tries to execute a statement, check if the table exists before proceeding
    # the nested if statements are used for checking if the functions return true, which means that the execution went properly
    # each function returns true or false based on a try-except block
    if user_input == "0":
        createTable()
    elif user_input == "1":
        if(check_table_existence()):
            getAllStudents()
    elif user_input == "2":
        if(check_table_existence()):
            first_name = input("New student's first name: ")
            last_name = input("New student's last name: ")
            email = input("New student's email: ")
            enrollment_date = input("New student's enrollment date (format is YYYY-MM-DD): ")

            if(addStudent(first_name, last_name, email, enrollment_date)):
                print("The table, after these modifications: ")
                getAllStudents()

    elif user_input == "3":
        if(check_table_existence()):
            student_id = input("ID of student to update: ")
            email = input("Updated email of student: ")

            if(updateStudentEmail(student_id, email)):
                print("The table, after these modifications: ")
                getAllStudents()

    elif user_input == "4":
        if(check_table_existence()):
            student_id = input("ID of student to delete: ")

            if(deleteStudent(student_id)):
                print("The table, after these modifications: ")
                getAllStudents()

    elif user_input == "q":
        loop = False
    else:
        print("Please enter a valid selection.")