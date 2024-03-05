Employee Management System:-
This Employee Management System is designed to facilitate the management of employee records within an organization. It allows for operations such as adding, editing, deleting, and displaying records of employees' personal and company information. The system also features a simple login mechanism with a retry limit and lockout time to secure access.

Features:-
Login Authentication: Secure login mechanism with retry limitations and temporary lockout to prevent unauthorized access.
Database Management: Creation and manipulation of databases and tables for storing employee personal and company information.
CRUD Operations: Ability to create, read, update, and delete employee records in the database.
Interactive Menu: A user-friendly menu for navigating through different functionalities.

Prerequisites:-
Python 3.x
MySQL Server
mysql-connector-python package

Installation:-
Before running the script, ensure you have Python and MySQL Server installed on your system. Then, install the necessary Python package by running:
pip install mysql-connector-python

Setup:-
Database Configuration: Edit the Sql_Username and Sql_Password variables in the script to match your MySQL server credentials.
MySQL Server: Ensure your MySQL server is running and accessible.

Usage:-
To start the application, run the script in your terminal or command prompt:
python employee_management_system.py

Functionalities:-
Login: Enter the predefined username and password to access the system.
Menu Options:
Add a New Record: Insert new employee personal and company information.
Edit an Existing Record: Update information of an existing employee.
Delete a Record: Remove an employee's record from the system.
Display Record: View personal, company, or all records of employees.
Exit: Log out of the system.

Security:-
This script uses a simple login mechanism for demonstration purposes. In a production environment, consider implementing more robust authentication methods.
