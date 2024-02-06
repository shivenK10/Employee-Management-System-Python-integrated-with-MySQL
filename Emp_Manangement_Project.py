import mysql.connector as sql
import sys
import time


# Function to check if tables (EmployeePersonalInformation and EmployeeCompanyInformation) exists or not.
def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("SHOW TABLES")  # Sql command to get all tables.
    result = [x[0] for x in dbcur.fetchall()]  # Converting the tables into a list.
    if tablename in result:  # Checking if table name is in the list of table.
        return True
    return False


def GetInput(String, Type):
    try:
        return Type(input(String))
    except ValueError:
        print('Invalid input type.\n')
        return GetInput(String, Type)
    except:
        print('Unexpected error occurred. Try again. \n')
        return GetInput(String, Type)


# Login ID & Password
Test_Username = "Admin001"  # Username defined
Test_Password = "password123"  # Password defined
Sql_Username = 'root'  # Sql user
Sql_Password = ''  # Sql password, NOTE: PLEASE ENTER THE PASSWORD SET BY YOU FOR MySQL SERVER.

SqlConnector = sql.connect(host="localhost", user=Sql_Username, passwd=Sql_Password, charset='utf8')  # Connecting with sql.

SqlConnectorExecutor = SqlConnector.cursor()
SqlConnectorExecutor.execute("SHOW DATABASES")  # Sql command to get all databases.

DatabaseList = [x[0] for x in SqlConnectorExecutor.fetchall()]  # Converting databases into a list.

if 'LoginInformationDatabase' not in DatabaseList:  # To check whether the database is there or not.
    SqlConnectorExecutor.execute("CREATE DATABASE LoginInformationDatabase")

# This is the syntax for establishing connection with the database.
LoginInformationDatabaseConnector = sql.connect(host="localhost", user=Sql_Username, passwd=Sql_Password, charset='utf8', database='LoginInformationDatabase')

# Connection Object, this connection object is used to access only LoginInformationDatabase.
LoginInformationDatabaseExecutor = LoginInformationDatabaseConnector.cursor()

# To check whether the table(Information) is there or not. If not then the table is created.
if not checkTableExists(LoginInformationDatabaseConnector, "Information"):
    LoginInformationDatabaseExecutor.execute("CREATE TABLE Information (Tries INT, LastLocked INT, LastLogin INT)")
    LoginInformationDatabaseExecutor.execute(
        "INSERT INTO Information (Tries, LastLocked, LastLogin) VALUES (" + str(3) + ", " + str(
            time.time()) + ", " + str(time.time()) + ") ")  # Setting Tries and Last locked values (time.time() gives number of seconds passed  since January 1, 1970).
    LoginInformationDatabaseConnector.commit()

LoginInformationDatabaseExecutor.execute("SELECT * FROM Information")
myresult = list(LoginInformationDatabaseExecutor.fetchall())  # Getting values of tries and last locked from the table.

if int(myresult[0][0]) <= 0:  # Checking if number of tries left is 0.
    if time.time() - int(myresult[0][1]) < 30:  # Checking if 30 seconds have not passed since last lock.
        print('Locked. Try again later. Time remaining:- ',
              "{:.2f}".format(float(30 - (time.time() - int(myresult[0][1])))))
        sys.exit()
    else:  # If 30 seconds have passed since last lock, reset the try count.
        LoginInformationDatabaseExecutor.execute("UPDATE Information SET Tries = '" + str(3) + "'")
        LoginInformationDatabaseConnector.commit()
elif int(myresult[0][0]) < 3:
    if time.time() - int(myresult[0][2]) > 60:  # Checking if 60 seconds have passed since last login.
        LoginInformationDatabaseExecutor.execute("UPDATE Information SET Tries = '" + str(3) + "'")
        LoginInformationDatabaseConnector.commit()

LoginInformationDatabaseExecutor.execute("UPDATE Information SET LastLogin = '" + str(time.time()) + "'")
LoginInformationDatabaseConnector.commit()

def EnterLoginId():
    LoginInformationDatabaseExecutor.execute("SELECT * FROM Information")
    myresult = list(LoginInformationDatabaseExecutor.fetchall())
    if int(myresult[0][0]) <= 0:  # If number of tries left is 0. Lock the user from trying again.
        LoginInformationDatabaseExecutor.execute("UPDATE Information SET LastLocked = '" + str(time.time()) + "'")
        LoginInformationDatabaseConnector.commit()
        print('Locked. Try again later.')
        return
    Username = input("Enter Username: ")  # User will input the Username
    Password = input("Enter Password: ")  # User will input the Password
    if CheckLogin(Username, Password):
        print()
        print('Succesfully logged in.\n')
        menu()
    else:
        print('Incorrect Username or Password. Tries left:', int(myresult[0][0]) - 1, '\n')
        LoginInformationDatabaseExecutor.execute(
            "UPDATE Information SET Tries = '" + str(int((myresult[0][0])) - 1) + "'")
        LoginInformationDatabaseConnector.commit()
        EnterLoginId()


def CheckLogin(Username, Password):  # Function to check whether the entered Username and Password (by the user) is correct or not
    if (Username == Test_Username) and (Password == Test_Password):
        return True
    else:
        return False


# Function to Check if table is present or not. If not then table is created. Also the menu is displayed that what
# the user want to do.
def menu():
    SqlConnector = sql.connect(host="localhost", user=Sql_Username, passwd=Sql_Password, charset='utf8')
    # Connection Object, this connection object is used to access all the databases.
    SqlConnectorExecutor = SqlConnector.cursor()
    SqlConnectorExecutor.execute("SHOW DATABASES")

    DatabaseList = [x[0] for x in SqlConnectorExecutor.fetchall()]

    if 'EmployeeProfileDatabase' in DatabaseList:  # To check whether the database is there or not.
        print("EmployeeProfileDatabase found!")
    else:  # If not then the database is created.
        SqlConnectorExecutor.execute("CREATE DATABASE EmployeeProfileDatabase")
        print("EmployeeProfileDatabase not found. Creating Database.")

    # This is the syntax for establishing connection with the database.
    EmployeeProfileDatabaseConnector = sql.connect(host="localhost", user=Sql_Username, passwd=Sql_Password,
                                                   charset='utf8', database='EmployeeProfileDatabase')
    # Connection Object, this connection object is used to access only EmployeeProfileDatabase.
    EmployeeProfileDatabaseExecutor = EmployeeProfileDatabaseConnector.cursor()
    print("Connected to database.")

    # To check whether the table(EmployeePersonalInformation) is there or not.
    if checkTableExists(EmployeeProfileDatabaseConnector, "EmployeePersonalInformation"):
        print("Employee Personal Information table found.")
        pass
    else:  # If not then the table(EmployeePersonalInformation) is created.
        EmployeeProfileDatabaseExecutor.execute(
            "CREATE TABLE EmployeePersonalInformation (Employee_ID INT AUTO_INCREMENT PRIMARY KEY, Employee_Name VARCHAR(255), DOB VARCHAR(255), Phone_Number VARCHAR(255), Address VARCHAR(255), Email_ID VARCHAR(255))")
        print("Employee Personal Information table created.")

    # To check whether the table(EmployeeCompanyInformation) is there or not.
    if checkTableExists(EmployeeProfileDatabaseConnector, "EmployeeCompanyInformation"):
        print("Employee Company Information table found.")
        pass
    else:  # If not then the table(EmployeeCompanyInformation) is created.
        EmployeeProfileDatabaseExecutor.execute(
            "CREATE TABLE EmployeeCompanyInformation (Employee_ID INT AUTO_INCREMENT PRIMARY KEY, Employee_Name VARCHAR(255), Department VARCHAR(255), Designation VARCHAR(255), Salary INT, Number_Of_Holidays_Taken INT)")
        print("Employee Company Information table created.")
    print()
    print()
    # Loop to display the menu and ask the user what he/she wants to do.
    while True:
        print("........MENU.......")
        print("1. Add a New Record")
        print("2. Edit an Existing Record")
        print("3. Delete a Record")
        print("4. Display Record")
        print("5. Exit")
        choice = input("Enter you choice (1/2/3/4/5): ")
        if choice == '1':
            add_record(EmployeeProfileDatabaseConnector, EmployeeProfileDatabaseExecutor)
        elif choice == '2':
            edit_record(EmployeeProfileDatabaseConnector, EmployeeProfileDatabaseExecutor)
        elif choice == '3':
            delete_record(EmployeeProfileDatabaseConnector, EmployeeProfileDatabaseExecutor)
        elif choice == '4':
            display_record(EmployeeProfileDatabaseConnector, EmployeeProfileDatabaseExecutor)
        elif choice == '5':
            print("Log Out Successful!")
            break
        else:
            print("Invalid Input!!!")
        print()
        print()
    else:
        sys.exit()


# If the user chooses first choice, so the function to let user add the data in both the tables.
def add_record(Database, Executor):
    if Database.is_connected():
        print()
        # Inserting values in Company Information Table.
        print("Enter the following fields for Personal Information")
        print()
        Emp_id = GetInput("Enter the Employee ID (Please enter Employee ID as a number, 'eg: 1001'): ", int)
        Emp_Name = GetInput("Enter Employee Name: ", str)
        Emp_DOB = GetInput("Enter Employee's Date of Birth: ", str)
        Emp_Phone = GetInput("Enter Employee's Phone Number: ", str)
        Emp_Address = GetInput("Enter Employee's Address: ", str)
        Emp_Email = GetInput("Enter Employee's Email ID: ", str)
        # Command for inserting Employee_ID, Employee_Name, DOB, Phone_Number, Address, Email_ID in table (EmployeePersonalInformation)
        Sql = "INSERT INTO EmployeePersonalInformation (Employee_ID, Employee_Name, DOB, Phone_Number, Address, " \
              "Email_ID) VALUES (%s, %s, %s, %s, %s, %s) "
        Records = (Emp_id, Emp_Name, Emp_DOB, Emp_Phone, Emp_Address, Emp_Email)
        Executor.execute(Sql, Records)
        Database.commit()
        print()
        # Inserting values in Company Information Table.
        print("Enter the following fields for Company Information")
        print()
        Emp_Department = GetInput("Enter Employees Department: ", str)
        Emp_Designation = GetInput("Enter Employee's Designation: ", str)
        Emp_Salary = GetInput("Enter Employee's Salary: ", int)
        Emp_Holidays = GetInput("Enter the Number of Holidays taken by the employee: ", int)
        # Command for inserting Employee_ID, Employee_Name, Department, Designation, Salary, Number_Of_Holiday_Taken in table (EmployeeCompanyInformation)
        Sql1 = "INSERT INTO EmployeeCompanyInformation (Employee_ID, Employee_Name, Department, Designation, Salary, " \
               "Number_Of_Holidays_Taken) VALUES(%s, %s, %s, %s, %s, %s) "
        records = (Emp_id, Emp_Name, Emp_Department, Emp_Designation, Emp_Salary, Emp_Holidays)
        Executor.execute(Sql1, records)
        Database.commit()
        print("Record Inserted Successfully.")
    else:
        print("Error: Database not connected.")


# If the user chooses second choice, so this function will let user edit the data in either Personal Information table
# or in Company Information table.
def edit_record(Database, Executor):
    print("1. Edit data in Employee Personal Information.")
    print("2. Edit data in Employee Company Information.")
    print()
    choice1 = input("Enter your choice (1/2): ")
    print()
    Emp_id = GetInput("Enter the Employee ID: ", int)
    Executor.execute("SELECT Employee_ID FROM EmployeePersonalInformation")
    data = Executor.fetchall()
    lst = []
    if choice1 == '1':
        for i in data:
            for j in i:
                lst.append(j)

        for k in lst:
            if Emp_id == k:
                Emp_Name = GetInput("Enter Employee Name: ", str)
                Emp_DOB = GetInput("Enter Employee's Date of Birth: ", str)
                Emp_Phone = GetInput("Enter Employee's Phone Number: ", str)
                Emp_Address = GetInput("Enter Employee's Address: ", str)
                Emp_Email = GetInput("Enter Employee's Email ID: ", str)
                print()
                # Command for editing Employee_ID, Employee_Name, DOB, Phone_Number, Address, Email_ID in table (EmployeePersonalInformation)
                SqlCommand = "UPDATE EmployeePersonalInformation SET Employee_Name = '" + Emp_Name + "', DOB = '" + Emp_DOB + "', Phone_Number = '" + Emp_Phone + "', Address = '" + Emp_Address + "', Email_ID = '" + Emp_Email + "'" + " WHERE Employee_ID = " + str(
                    Emp_id)
                Executor.execute(SqlCommand)
                Database.commit()
                print("Record Updated Successfully.")
                return
        print("Entered Employee ID doesn't exist. Please Try Again!")


    elif choice1 == '2':
        for i in data:
            for j in i:
                lst.append(j)

        for k in lst:
            if Emp_id == k:
                Emp_Name = GetInput("Enter Employee Name: ", str)
                Emp_Department = GetInput("Enter Employees Department: ", str)
                Emp_Designation = GetInput("Enter Employee's Designation: ", str)
                Emp_Salary = GetInput("Enter Employee's Salary: ", int)
                Emp_Holidays = GetInput("Enter the Number of Holidays taken by the employee: ", int)
                print()
                # Command for editing Employee_ID, Employee_Name, Department, Designation, Salary, Number_Of_Holiday_Taken in table (EmployeeCompanyInformation)
                SqlCommand1 = "UPDATE EmployeeCompanyInformation SET Employee_Name = '" + Emp_Name + "', Department = '" + Emp_Department + "', Designation = '" + Emp_Designation + "', Salary = '" + str(
                    Emp_Salary) + "', Number_Of_Holidays_Taken = '" + str(
                    Emp_Holidays) + "'" + " WHERE Employee_ID = " + str(
                    Emp_id)
                Executor.execute(SqlCommand1)
                Database.commit()
                print("Record Updated Successfully.")
                return
        print("Entered Employee ID doesn't exist. Please Try Again!")

    else:
        print("Invalid Input! Try Again!")


# If the user chooses third choice, so the function to let user delete a particular record by entering the Employee ID.
def delete_record(Database, Executor):
    Emp_ID = GetInput("Enter the Employee ID: ", int)
    # Command for deleting Employee_ID, Employee_Name, DOB, Phone_Number, Address, Email_ID, Department, Designation, Salary, Number_Of_Holiday_Taken in both the table (EmployeePersonalInformation & EmployeeCompanyInformation)
    Executor.execute("SELECT Employee_ID FROM EmployeePersonalInformation")
    data = Executor.fetchall()
    print()
    lst = []
    for i in data:
        for j in i:
            lst.append(j)

    for k in lst:
        if Emp_ID == k:
            SqlCommand = "DELETE FROM EmployeePersonalInformation WHERE Employee_ID = " + str(Emp_ID)
            SqlCommand1 = "DELETE FROM EmployeeCompanyInformation WHERE Employee_ID = " + str(Emp_ID)
            Executor.execute(SqlCommand)
            Database.commit()
            Executor.execute(SqlCommand1)
            Database.commit()
            print("Record Delered Successfully.")
            return
    print("Entered Employee ID doesn't exist. Please Try Again!")


# If the user chooses fourth choice, so this will display either Personal Information table or Company Information
# table or whole record at once.
def display_record(Database, Executor):
    print("1. Display records of Personal Information Table.")
    print("2. Display records of Company Information Table.")
    print("3. Display all the records.")
    choice2 = input("Enter your choice (1/2/3): ")
    print()
    if choice2 == '1':
        if Database.is_connected():
            # Command for displaying EmployeePersonalInformation Table
            Executor.execute("SELECT * FROM EmployeePersonalInformation")
            myresult = list(Executor.fetchall())
            print(" {:<5} {:<15} {:<15} {:<15} {:<15} {:<10} {:<20}".format('No.', 'Employee ID', 'Employee Name', 'Date Of Birth', 'Phone Number', 'Address', 'Email'))
            count = 1
            for i in myresult:
                print(" {:<5} {:<15} {:<15} {:<15} {:<15} {:<10} {:<20}".format(count, i[0], i[1], i[2], i[3], i[4], i[5]))
                count += 1

    elif choice2 == '2':
        if Database.is_connected():
            # Command for displaying EmployeeCompanyInformation Table
            Executor.execute("SELECT * FROM EmployeeCompanyInformation")
            myresult1 = Executor.fetchall()
            print("{:<5} {:<15} {:<15} {:<15} {:<20} {:<15} {:<5}".format('No.', 'Employee ID', 'Employee Name', 'Department', 'Designation', 'Salary', 'No. of Holidays Taken'))
            count = 1
            for i in myresult1:
                print("{:<5} {:<15} {:<15} {:<15} {:<20} {:<15} {:<5}".format(count, i[0], i[1], i[2], i[3], i[4], i[5]))
                count += 1

    elif choice2 == '3':
        if Database.is_connected():
            # Command for displaying bot EmployeePersonalInformation & EmployeeCompanyinformation Table
            Executor.execute("SELECT * FROM EmployeePersonalInformation")
            myresult = list(Executor.fetchall())
            Executor.execute("SELECT * FROM EmployeeCompanyInformation")
            myresult1 = list(Executor.fetchall())

            count = 1

            print(" {:<5} {:<15} {:<15} {:<15} {:<15} {:<10} {:<20} {:<15} {:<20} {:<15} {:<5}".format('No.', 'Employee_ID', 'Employee_Name', 'DateOfBirth', 'PhoneNumber', 'Address', 'Email', 'Department', 'Designation', 'Salary', 'No. Of Holidays Taken'))

            for i in range(0, len(myresult)):
                print(" {:<5} {:<15} {:<15} {:<15} {:<15} {:<10} {:<20} {:<15} {:<20} {:<15} {:<5}".format(count, myresult[i][0], myresult[i][1], myresult[i][2], myresult[i][3], myresult[i][4], myresult[i][5], myresult1[i][2], myresult1[i][3], myresult1[i][4], myresult1[i][5]))

                count += 1
    else:
        print("Invalid Input!")
    print()


EnterLoginId()
