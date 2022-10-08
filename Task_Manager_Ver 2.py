# ====Functions Section====
from datetime import datetime
import time


def reg_user():
    """In this block we check whether a user can register
    a person that does not exist in our system yet and if so
    we add the new user to the user.txt file"""

    with open("user.txt", "r+") as user_file:
        # users_list = user_file.readlines()    # using
        usernames_list = [name.split(', ')[0]
                          for name in user_file.readlines()]

        name_switch = True
        # Loop structure to validate correct username
        while name_switch:
            new_user = input("Enter new username: ").lower()
            # conditional statement will run true if name not in list of registered users
            if new_user not in usernames_list:
                new_password = input("Enter new password: ").lower()
                # while loop to validate password match
                while True:
                    new_password_confirmation = input(
                        "Confirm new user password: ").lower()
                    if new_password == new_password_confirmation:
                        print("\nNew user has been registered successfully! ")
                        break
                    else:
                        print("Passwords do not match! Try again")
                name_switch = False
            else:
                print("Username already exists! Try again...")

        # Writing new user details to file
        user_file.write(f"\n{new_user}, {new_password}")
        print("Details have been written to file....")


def add_task():
    """In this block we let the user add a new task to task.txt file"""
    with open("tasks.txt", "a") as tasks_file:

        while True:
            task_add = input(
                "\t'a' - add task \n\t'r' - return to main menu \n: ").lower()

            if task_add == "a":
                # grabbing user inputs to write
                assigned_user = input("Enter user task is assigned to: ")
                task_title = input("Enter task title: ")
                task_description = input("Enter task description: ")
                task_assigned_date = datetime.today().strftime("%d %b %Y")
                task_assingned_due_date = input(
                    "Enter the task due date(e.g 12 Oct 2020): ")
                task_completion_status = "No"

                # writing to file
                tasks_file.write(
                    f"{assigned_user}, {task_title}, {task_description}, {task_assigned_date}, {task_assingned_due_date}"
                    f", {task_completion_status}\n")

            elif task_add == "r":
                break
            else:
                print("\nInvalid Input entered!")


def view_all():
    """In this block you will put code so that the program will read the task from task.txt file and
        print to the console.
    """
    with open("tasks.txt", "r+") as tasks_file:
        for tasks in tasks_file:
            assigned_user, task_title, task_description, task_assigned_date, task_assingned_due_date \
                , task_completion_status = tasks.split(", ")

            print(f"""
            ============================================
            Username: {assigned_user}
            Task Title: {task_title}
            Task Description: {task_description}
            Date assigned: {task_assigned_date}
            Task Due Date: {task_assingned_due_date}
            Task complete: {task_completion_status}
            ============================================
            """)


def view_mine(username):
    """In this block you will put code the that will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the L1T19 pdf
    """
    with open("tasks.txt", "r+") as tasks_file:
        task_dict = {}

        # for loop to populate dictionary
        for task_num, task in enumerate(tasks_file.readlines(), 1):
            task_dict[task_num] = task.strip("\n").split(", ")

        # for loop to display user's tasks
        for count, tasks in enumerate(task_dict.values(), 1):
            if tasks[0] == username:
                print(f"""
                ============================================
                Task No: {count}
                Username: {tasks[0]}
                Task Title: {tasks[1]}
                Task Description: {tasks[2]}
                Date assigned: {tasks[3]}
                Task Due Date: {tasks[4]}
                Task complete: {tasks[5]}
                ============================================
                """)

        # Edit section 
        while True:
            edit_prompt_section = input("\n\t'p' - proceed to edit section\n\t'r' - return to main menu\n\t: ").lower()

            if edit_prompt_section == 'p':

                task_number_selection = int(input("\n\tEnter a task number: "))
                # conditional to validate whether task can be edited or not
                if task_dict[task_number_selection][-1] != "Yes":

                    # menu for editing preferences
                    edit_menu = input("\n\t'md' - mark task as complete\n\t'ed' - edit the task\n\t: ").lower()

                    if edit_menu == 'md':
                        task_dict[task_number_selection][-1] = "Yes"

                    elif edit_menu == 'ed':

                        # sub menu for editing task details
                        edit_task_menu = input(
                            "\n\t'eu' - change/update username\n\t'dd' - change/update due date\n\t: ").lower()

                        if edit_task_menu == 'eu':
                            updated_username = input("Enter new username for task: ")
                            task_dict[task_number_selection][0] = updated_username
                            print("Username has been updated!")

                        elif edit_task_menu == 'dd':
                            updated_due_date = input("Enter the new task due date (e.g 12 Oct 2020): ")
                            task_dict[task_number_selection][4] = updated_due_date
                            print("Due date has been updated!")
                        else:
                            print("Invalid input entered, returning to main menu...")
                            time.sleep(2)  # tiny delay added for spice

                else:
                    print("\tThe task can not be edited it has already been marked as complete")

                # updating text file by passing in new dictionary values
                with open("tasks.txt", "w+") as tasks_file_w:
                    new_task = ""
                    for tasks in task_dict.values():
                        new_task += ", ".join(tasks) + "\n"

                    tasks_file_w.write(new_task)


            elif edit_prompt_section == 'r':
                print("\n\treturning to main menu..")
                time.sleep(2)
                break
            else:
                print("Invalid input entered!")


def gen_rep():
    """
    This block of code will contain the statistics logic; it will iterate over
    the file and return the stats around the users and tasks.
    """
    with open("user.txt", "r+") as user_file, open("tasks.txt", "r+") as tasks_file:
        tasks_list = tasks_file.readlines()
        users_list = user_file.readlines()

        # ========== task details section ==========#
        # counter variables
        num_tasks = len(tasks_list)
        num_completed_tasks = 0
        num_incomplete_tasks = 0
        num_incomplete_overdue = 0

        # percentage variables declaration
        percentage_complete = 0
        percentage_incomplete = 0
        percentage_overdue = 0

        for tasks in tasks_list:
            task_details = tasks.strip("\n").split(", ")

            # conditional body to populate counter variables
            if task_details[-1] == "Yes":
                num_completed_tasks += 1
            if task_details[-1] == "No":
                num_incomplete_tasks += 1

                # creating date objects for overdue validation
                curr_date_object = datetime.today()
                due_date_object = datetime.strptime(task_details[4], "%d %b %Y")

                if (curr_date_object > due_date_object):
                    num_incomplete_overdue += 1

        percentage_complete = round((num_completed_tasks / num_tasks) * 100, 2)
        percentage_incomplete = round((num_incomplete_tasks / num_tasks) * 100, 2)
        percentage_overdue = round((num_incomplete_overdue / num_incomplete_tasks) * 100, 2)

        with open("task_overview.txt", "w+") as task_deets:
            task_deets.write(f"\t================= Tasks Details Statistics ===============\n")
            task_deets.write(f"""
              - Number of Tasks: {num_tasks}
              - Number of Complete Tasks: {num_completed_tasks}
              - Number of Incomplete Tasks: {num_incomplete_tasks} 
              - Number of Incomplete & Overdue: {num_incomplete_overdue}
              
              - Percentage of Complete Tasks: {percentage_complete}%
              - Percentage of Incomplete Tasks: {percentage_incomplete}%
              - Percentage of tasks Incomplete tasks that are Overdue: {percentage_overdue}%
        """)

        # ========== User details section ==========#
        with open("user_overview.txt", "w+") as user_deets:
            user_deets.write(f"\t================= User Details Statistics ===============\n")
            for user in users_list:

                # counter variables
                num_u_tasks = 0
                num_completed_u_tasks = 0
                num_incomplete_u_tasks = 0
                num_incomplete_u_overdue = 0

                # percentage variables declaration
                percentage_tasks_assigned = 0
                percentage_u_complete = 0
                percentage_u_incomplete = 0
                percentage_u_overdue = 0

                user_details = user.strip("\n").split(", ")

                for tasks in tasks_list:
                    task_details = tasks.strip("\n").split(", ")

                    if user_details[0] == task_details[0]:
                        num_u_tasks += 1
                        # conditional body to populate counter variables
                        if task_details[-1] == "Yes":
                            num_completed_u_tasks += 1
                        if task_details[-1] == "No":
                            num_incomplete_u_tasks += 1

                            # creating date objects for overdue validation
                            curr_date_object = datetime.today()
                            due_date_object = datetime.strptime(task_details[4], "%d %b %Y")

                            if (curr_date_object > due_date_object):
                                num_incomplete_u_overdue += 1

                try:
                    percentage_tasks_assigned = round((num_u_tasks / num_tasks) * 100, 2)
                    percentage_u_complete = round((num_completed_u_tasks / num_u_tasks) * 100, 2)
                    percentage_u_incomplete = round((num_incomplete_u_tasks / num_u_tasks) * 100, 2)
                    percentage_u_overdue = round((num_incomplete_u_overdue / num_incomplete_u_tasks) * 100, 2)
                except ZeroDivisionError:
                    pass

                user_deets.write(f"""
                ----------------
                Username: {user_details[0]}
                ----------------
                    Number of Tasks: {num_u_tasks}
                    Number of Complete Tasks: {num_completed_u_tasks}
                    Number of Incomplete Tasks: {num_incomplete_u_tasks} 
                    Number of Incomplete & Overdue: {num_incomplete_u_overdue}
                    
                    Percentage of Tasks assigned to user: {percentage_tasks_assigned}
                    Percentage of Complete Tasks: {percentage_u_complete}%
                    Percentage of Incomplete Tasks: {percentage_u_incomplete}%
                    Percentage of tasks Incomplete tasks that are Overdue: {percentage_u_overdue}%
                ----------------
                """)

        print("The user overview and task overview files have been generated!")


def display_rep():
    try:
        with open("user_overview.txt", "r+") as user_file, open("task_overview.txt", "r+") as tasks_file:
            print(user_file.read())
            print(tasks_file.read())
    except FileNotFoundError:
        print("\nFiles have not been generated, try picking 'gr' option first.")


# ====Login Section====
switch = True
while switch:
    username_login = input("Enter your username: ").lower()
    password_login = input("Enter your password: ").lower()

    with open("user.txt", "r+") as user_file:

        for lines in user_file.readlines():
            username_text, password_text = lines.strip("\n").lower().split(", ")

            if (username_text == username_login) and (password_text == password_login):
                print("\n☆*: .｡. o(≧▽≦)o .｡.:*☆ \nYou have successfully logged in!\n")
                switch = False
            elif (username_text != username_login) and (password_text != password_login):
                continue

# ===== Driver Code ===== #
while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    menu = input('''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display reports
e - Exit
: ''').lower()

    if (menu == 'r') and (username_login == "admin"):
        reg_user()
    elif (menu == 'r') and (username_login != "admin"):
        print("Only the Admin can register new users.")
    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine(username_login)

    elif menu == 'gr':
        gen_rep()

    elif menu == 'ds':
        display_rep()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")
