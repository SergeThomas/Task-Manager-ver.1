"""
This is a basic Admin CRUD app that allows users to create
tasks, read, update and delete the tasks.
"""

# =====importing libraries===========
from datetime import datetime

# ====Login Section====
switch = True

while switch:
    username_login: str = input("Enter your username: ").lower()
    password_login = input("Enter your password: ").lower()

    with open("user.txt", "r+") as user_file:

        for lines in user_file.readlines():
            username_text, password_text = lines.strip("\n").lower().split(", ")

            if (username_text == username_login) and (password_text == password_login):
                print("\n☆*: .｡. o(≧▽≦)o .｡.:*☆ \nYou have successfully logged in!\n")
                switch = False
            elif (username_text != username_login) or (password_text != password_login):
                pass

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    menu = input('''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    if (menu == 'r') and (username_login == "admin"):
        with open("user.txt", "a+") as user_file:
            new_user = input("Enter new username: ").lower()
            new_password = input("Enter new password: ").lower()

            while True:
                new_password_confirmation = input("Confirm new user password: ").lower()
                if new_password == new_password_confirmation:
                    print("New user has been registerd successfully! ")
                    break
                else:
                    print("Passwords do not match! Try again")

            user_file.write(f"\n{new_user}, {new_password}")
            print("Details have been written to file....")

    elif (menu == 'r') and (username_login != "admin"):
        print("Only the Admin is allowed to register a user!")

    elif menu == 'a':
        with open("tasks.txt", "a+") as tasks_file:

            while True:

                task_add = input("A - add task \nR - return to main menu \n: ").upper()

                if task_add == "A":
                    # grabbing user inputs to write
                    assigned_user = input("Enter user task is assigned to: ")
                    task_title = input("Enter task title: ")
                    task_description = input("Enter task description: ")
                    task_assigned_date = datetime.today().strftime("%d %b %Y")
                    task_assingned_due_date = input("Enter the task due date(e.g 12 Oct 2020): ")
                    task_completion_status = "No"

                    # writing to file
                    tasks_file.write(
                        f"\n{assigned_user}, {task_title}, {task_description}, {task_assigned_date}, "
                        f"{task_assingned_due_date}, {task_completion_status}")

                elif task_add == "R":
                    break
                else:
                    print("\nInvalid Input entered!")

    elif menu == 'va':
        with open("tasks.txt", "r+") as tasks_file:
            for no, tasks in enumerate(tasks_file):
                assigned_user, task_title, task_description, task_assigned_date, task_assingned_due_date \
                    , task_completion_status = tasks.split(", ")

                print(f"""
                Task Number: {no}
                Username: {assigned_user}
                Task Title: {task_title}
                Task Description: {task_description}
                Date assigned: {task_assigned_date}
                Task Due Date: {task_assingned_due_date}
                Task complete: {task_completion_status}
                """)

    elif menu == 'vm':
        with open("tasks.txt", "r+") as tasks_file:
            for tasks in tasks_file:
                assigned_user, task_title, task_description, task_assigned_date, task_assingned_due_date \
                    , task_completion_status = tasks.split(", ")

                if assigned_user == username_login:
                    print(f"""
                    Username: {assigned_user}
                    Task Title: {task_title}
                    Task Description: {task_description}
                    Date assigned: {task_assigned_date}
                    Task Due Date: {task_assingned_due_date}
                    Task complete: {task_completion_status}
                    """)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
