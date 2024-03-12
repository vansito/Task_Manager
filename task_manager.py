#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

#=======Functions========


def reg_user():

    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ")

    # Checks if the user is already existent 
    duplicate = True
    while duplicate:

        if new_username in username_password.keys():
            print(f"The user {new_username} already exist, please choose another user name.")
            new_username = input("New Username: ")
        else:
            duplicate = False

    # - Request input of a new password
    new_password = input("New Password: ")

    while True:
        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("\nNew user added!")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            break

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do not match, please try again.")


def add_task():

    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    
    present = True
    while present:
        task_username = input("Name of person assigned to task: ")

        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        
        else:
            present = False

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT).date()
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

        # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''

    while True:   
        if curr_date < due_date_time:
            new_task = {
                "username": task_username,
                "title": task_title,
                "description": task_description,
                "due_date": due_date_time,
                "assigned_date": curr_date,
                "completed": False
            }

            task_list.append(new_task)
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
            print("Task successfully added.")
            break
        else:
            print("The date is in the past, please enter a future date.")
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT).date()

def view_all():

    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Complete? \t {t['completed']}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_mine():
    
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
    count = 0
    for index,t in enumerate(task_list):
        if curr_user in t['username']:
            count += 1
            disp_str = f"\nTask {count}: \t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Complete? \t {t['completed']}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    print("#" * 80)
    print()

    # Output of the list of tasks for the user to choose
    count = 0
    task_dict = {}
    for index,t in enumerate(task_list):
        if curr_user in t['username']:
            count += 1
            task_dict.update({count: t['title']})
            print(f"- Task {count}: {t['title']}\n") 

    while True:
        options = int(input("Please choose one of the above tasks number or input '-1' to exit: "))
        if options in task_dict:
            
            while True:
                complete = input("\nTo mark the task completed please input 'completed' or 'edit' to modify it: ").lower()
                # When user mark the task completed the task it's written in the tasks.txt file
                if complete == 'completed':
                    options = task_dict[options]

                    for i in task_list:
                        if options == i['title']:
                            i['completed'] = True
            
                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in task_list:
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No"
                            ]
                            task_list_to_write.append(";".join(str_attrs))
                        task_file.write("\n".join(task_list_to_write))
                    print("\nTask successfully updated.")
                    break

                # When editing the task either a new username or a new due date is promted and then written in the user.txt file
                elif complete == 'edit':
                    options = task_dict[options]

                    for t in task_list:
                        if options == t['title']:
                            if curr_user in t['username'] and t['completed'] != True:
                                edit = int(input("""
        - Press 1 for editing the username
        - press 2 for editing the due date\n
        : """))
                            else:
                                print("\nSorry you can't edit this task as it's completed.")
                                break    
                                
                    if edit == 1:
                        new_name = input("Please enter a new username: ")

                        for x in task_list: #  Changes username into new name and writes it in the tasks file
                            if curr_user == x['username']:
                                x['username'] = new_name
                            break

                        for t in task_list:
                            if t['username'] == new_name:
                                with open("tasks.txt", "w") as task_file:
                                    task_list_to_write = []
                                    str_attrs = [
                                        new_name,
                                        t['title'],
                                        t['description'],
                                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                        "Yes" if t['completed'] else "No"
                                    ]
                                    task_list_to_write.append(";".join(str_attrs))
                                    task_file.write("\n".join(task_list_to_write))
                                

                            with open("tasks.txt", "w") as task_file: # Overwrite in order to update the new name
                                task_list_to_write = []
                                for t in task_list:
                                    str_attrs = [
                                        t['username'],
                                        t['title'],
                                        t['description'],
                                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                        "Yes" if t['completed'] else "No"
                                    ]
                                    task_list_to_write.append(";".join(str_attrs))
                                task_file.write("\n".join(task_list_to_write))

                        print("\nTask successfully edited.")
                        
                        for i in task_list: # Writes new name in the user file 
                            if i['username'] == new_name:
                                with open("user.txt", "w") as out_file:
                                    user_data = []
                                    for k in username_password:
                                        if curr_user == k:
                                            user_data.append(f"{new_name};{username_password[k]}")
                                            continue
                                        user_data.append(f"{k};{username_password[k]}")
                                    out_file.write("\n".join(user_data))
                            break
                        break
                    

                    elif edit == 2:
                        try:
                            new_date = input("Please enter new due date of task (YYYY-MM-DD): ")
                            new_date_time = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                            t['due_date'] = new_date_time
                            
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")

                        with open("tasks.txt", "w") as task_file:
                            task_list_to_write = []
                            for t in task_list:
                                str_attrs = [
                                    t['username'],
                                    t['title'],
                                    t['description'],
                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                    "Yes" if t['completed'] else "No"
                                ]
                                task_list_to_write.append(";".join(str_attrs))
                            task_file.write("\n".join(task_list_to_write))
                        print("\nThe due date has been edited!")
                        break

                    else:
                        print("Invalid input, please try again.")

        elif options == -1:
            exit

        else:
            print("\nInvalid input, please try again!\n")


def reports():

    """
    An overview reports of both tasks data and user data.
    Written and displayed in files.
    """
    # Parse content to extract information
    num_users = len(username_password)
    num_tasks = len(task_list)

    #TASK OVERVIEW

    # total tasks list
    tot_tasks = len(task_list)

    # total uncompleted tasks
    task_uncompleted = []
    for x in task_list:
        if x['completed'] == False:
            task_uncompleted.append(x)
    task_unc = len(task_uncompleted)

    # total completed task
    task_completed = []
    for y in task_list:
        if y['completed'] == True:
            task_completed.append(y)
    task_com = len(task_completed)

    # total uncompleted and overdue
    overdue = []
    x = datetime.now()
    for i in task_list:
        if i['due_date'] < x and i['completed'] == False:
            overdue.append(i)
    unc_overdue = len(overdue)

    # uncomplete task percentage
    unc_percentage = (task_unc / tot_tasks) * 100

    # overdue task percentage
    ov_percentage = (unc_overdue / tot_tasks) * 100

    # Display statistics
    disp_total = f"\nNumber of users: \t\t {num_users}\n"
    disp_total += f"Number of tasks: \t\t {num_tasks}\n"

    # overview display
    disp_overview = f"Total number of tasks: {tot_tasks}\n"
    disp_overview += f"Total number of completed tasks: {task_com}\n"
    disp_overview += f"Total number of completed tasks: {task_unc}\n"
    disp_overview += f"Total number of uncompleted and overdue tasks: {unc_overdue}\n"
    disp_overview += f"Percentage of uncompleted tasks: {unc_percentage:.2f}%\n"
    disp_overview += f"Percentage of overdue tasks: {ov_percentage:.2f}%\n"

    with open("task_overview.txt", "w+") as task_over:
        task_over.write("-"*35)
        task_over.write(disp_total)
        task_over.write("-"*35)
        task_over.write(f"\n{'-'*30} {'Total Overview'} {'-'*30}\n\n")
        task_over.write(disp_overview)
        lines = task_over.read()
    print(lines)

    with open("task_overview.txt", "r") as task_over:
        lines = task_over.read()
    print(lines)

    # USER OVERVIEW

    # unique users
    unique_users = set(task['username'] for task in task_list)
    n = 0
    for user in unique_users:
        # total number of tasks assigned to each user
        total_tasks = sum(1 for task in task_list if task['username'] == user)
        
        # percentage of total tasks assigned to each user
        percentage_total_tasks = (total_tasks / len(task_list)) * 100
        
        # percentage of completed tasks for each user
        completed_tasks = sum(1 for task in task_list if task['username'] == user and task['completed'])
        percentage_completed_tasks = (completed_tasks / total_tasks) * 100 if total_tasks != 0 else 0
        
        # percentage of incomplete tasks for each user
        percentage_incomplete_tasks = 100 - percentage_completed_tasks
        
        # percentage of overdue tasks for each user
        overdue_tasks = sum(1 for task in task_list if task['username'] == user and not task['completed'] and task['due_date'] < datetime.now())
        percentage_overdue_tasks = (overdue_tasks / total_tasks) * 100 if total_tasks != 0 else 0
        
        # Display the results
        user_overview = f"\nUser: {user}\n"
        user_overview += f"Total tasks assigned: {total_tasks}\n"
        user_overview += f"Percentage of total tasks: {percentage_total_tasks:.2f}%\n"
        user_overview += f"Percentage of completed tasks: {percentage_completed_tasks:.2f}%\n"
        user_overview += f"Percentage of incomplete tasks: {percentage_incomplete_tasks:.2f}%\n"
        user_overview += f"Percentage of overdue tasks: {percentage_overdue_tasks:.2f}%\n{'='*78}"


        if n == 0:
            with open("user_overview.txt", "w") as user_over:
                user_over.write(f"\n{'-'*30} {'User Overview'} {'-'*30}\n")
                user_over.write(user_overview)
        else:
            with open("user_overview.txt", "a+") as user_over:
                user_over.write(user_overview)
        n += 1
    with open("user_overview.txt", "r") as user_over:
        file = user_over.read()
    print(file)


def generate_files_if_not_exist():
    """Function to generate tasks_overview.txt and user_overview.txt
        if they don't exist"""

    if not os.path.exists("task_overview.txt"):
        with open("task_overview.txt", "w+") as task_over:
            pass

    if not os.path.exists("user_overview.txt"):
        with open("user_overview.txt", "w") as user_over:
            pass


def statistics():
    '''Function that allows the admin to display statistics about number of users
            and tasks.'''

    # Generate files if they don't exist
    generate_files_if_not_exist()

    # Read content from tasks.txt and user.txt
    
    reports()

# Task list
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':

        reg_user()

    elif menu == 'a':

        add_task()

    elif menu == 'va':
      
        view_all()

    elif menu == 'vm':

       view_mine()

    elif menu == 'gr':

        reports()

    elif menu == 'ds' and curr_user == 'admin':

        statistics()
        
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")