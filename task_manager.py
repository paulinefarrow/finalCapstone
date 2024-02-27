# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

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

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component to dictionary curr_t
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], 
                                           DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], 
                                                DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    # append each tasks dictionary to task_list
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


# - function to add users to user.txt file
def reg_user():
    """
    Add users to user.txt file.
    :param None
    :return None
    """
    with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))


# - function to add tasks to task.txt
def add_task():
    """
    Add tasks to task.txt file.
    :param None
    :return None
    """     
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


# - function to display all tasks
def view_all():
    """
    Display all tasks.
    :param None
    :return None
    """  
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"""Date Assigned: \t {t['assigned_date'].strftime(
             DATETIME_STRING_FORMAT)}\n"""
        disp_str += f"""Due Date: \t {t['due_date'].strftime(
             DATETIME_STRING_FORMAT)}\n"""
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


# - function to display current users tasks
def view_mine(cu):
    """
    Display tasks assigned to the current user.
    :param cu: The current user's username.
    :type cu: string
    :return: None
    """
    for i, t in enumerate(task_list,1):
        if t['username'] == curr_user:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"""Date Assigned: \t 
            {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"""
            disp_str += f"""Due Date: \t 
            {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"""
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += "Task Completed: " +  ("Yes" if t['completed']
                                                else "No")
            print(f"Task {i}")
            print(disp_str)


# count users in user.txt
def num_users():
    """
    Count users in user.txt
    :param None
    :type None
    :return: The number of users in user.txt
    :rtype: Integer
    """
    with open(r"user.txt", 'r') as u:
        return len(u.readlines())


# count tasks in tasks.txt
def num_tasks():
    """
    Count tasks in tasks.txt.
    :param None
    :type None
    :return: The number of tasks in tasks.txt
    :rtype: Integer
    """
    with open(r"tasks.txt", 'r') as t:
        return len(t.readlines())


# define function to calculate user and task stats and add to .txt files
    
def report_files():
    """
    Calculate user and task stats and add to user_overview.txt 
    and task_overview.txt.
    :param None
    :return: None
    """
    total_task_count = 0
    task_complete = 0
    task_incomplete = 0
    task_incomplete_overdue = 0
    user_task_count = 0
    user_task_complete = 0
    user_task_incomplete = 0
    user_task_incomplete_overdue = 0

    curr_user = ''        
    write_list = []
    sorted_task_list = []
    sorted_task_list = sorted(task_list, key=lambda x: x['username'])

    for i, t in enumerate(sorted_task_list,1):
        if i==1:
            curr_user = t['username']
        if t['username'] == curr_user:
            total_task_count += 1
            user_task_count += 1
            if t['completed'] == True:
                user_task_complete += 1
                task_complete += 1
            elif t['completed'] == False:
                user_task_incomplete += 1
                task_incomplete += 1
                if t['due_date'] < (datetime.combine(date.today(), 
                                                     datetime.min.time())):   
                    user_task_incomplete_overdue += 1
                    task_incomplete_overdue += 1


        elif    (t['username'] != curr_user and i!=1):               
            user_stats = [(curr_user.ljust(10)), 
                          "\t", (str(user_task_count)).ljust(26),
                          "\t", (str(round(100*(user_task_count/
                                                num_tasks())))).ljust(26),
                          "\t", (str(round(100*(user_task_complete/
                                                user_task_count)))).ljust(26),
                          "\t", (str(round(100*(user_task_incomplete/
                                                user_task_count)))).ljust(26),
                          "\t", (str(round(100*(user_task_incomplete_overdue/
                                                user_task_count)))).ljust(26)
            ]

            write_list.append("".join(user_stats))
            user_task_count = 0
            user_task_complete = 0
            user_task_incomplete = 0
            user_task_incomplete_overdue = 0
            curr_user = t['username']

            total_task_count += 1
            user_task_count += 1
            if t['completed'] == True:
                user_task_complete += 1
                task_complete += 1
            elif t['completed'] == False:
                user_task_incomplete += 1
                task_incomplete += 1
                if   t['due_date'] < (datetime.combine(date.today(),
                                                        datetime.min.time())):
                    user_task_incomplete_overdue += 1
                    task_incomplete_overdue += 1

        if i == len(sorted_task_list):
            user_stats = [(curr_user.ljust(10)), 
                          "\t", (str(user_task_count)).ljust(26),
                          "\t", (str(round(100*(user_task_count/
                                                num_tasks())))).ljust(26),
                          "\t", (str(round(100*(user_task_complete/
                                                user_task_count)))).ljust(26),
                          "\t", (str(round(100*(user_task_incomplete/
                                                user_task_count)))).ljust(26),
                          "\t", (str(round(100*(user_task_incomplete_overdue/
                                                user_task_count)))).ljust(26)
            ]

            write_list.append("".join(user_stats))
                          

    # write report to user_overview.txt
               
    with open("user_overview.txt", "w") as useroverview_file:
        useroverview_file.write("USER TASK REPORT" + "\n" 
                                + "----------------" +"\n")
        useroverview_file.write("Total Number of Registered Users = " 
                                + str(num_users()) +"\n")
        useroverview_file.write("Total Number of Tracked Tasks    = " 
                                + str(num_tasks()) +"\n\n")
        useroverview_file.write("User:     " 
                                + "\t" +  "Number of tasks assigned: "
                                + "\t" +  "% of all tasks assigned:  "
                                + "\t" +  "% of own tasks completed: "
                                + "\t" +  "% of own tasks incomplete:"
                                + "\t" +  "% of own tasks overdue:   " +
                                "\n" +"\n")
        
        # write calculated stats to user_overview.txt
        useroverview_file.write("\n".join(write_list))

    # write report to task_overview.txt
               
    with open("task_overview.txt", "w") as taskoverview_file:
        taskoverview_file.write("TASK REPORT:" + "\n" 
                              + "------------" +"\n\n")
       
       
        taskoverview_file.write("Total Number of Completed Tasks    = " + 
                                str(task_complete) + "\n" +
                                "Total Number of Incomplete Tasks   = " + 
                                str(task_incomplete) + " (" 
                                + (str(round(100*(task_incomplete/
                                                  total_task_count)))) + 
                                                  "% of all tasks)" + "\n" +
                                "______________________".rjust(56) + "\n" + 
                                "Total Tasks = ".rjust(51)  + 
                                str(total_task_count) + "\n\n" + 
                                "Total Number of Overdue Tasks      = " + 
                                str(task_incomplete_overdue) + " ("
                                + (str(round(100*(task_incomplete_overdue/
                                                  total_task_count)))) + 
                                                  "% of all tasks)"  
        )                           


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following options:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports                 
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        new_username = input("New Username: ")
        while True:
            if new_username.lower() in username_password.keys():
                new_username = input("""User already exists, 
                                     enter a new user: """)
                continue
            else:
                break

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to username_password dictionary
            
            username_password[new_username] = new_password

            # run function to add all users to user.txt
            reg_user()
            print("New user added")

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do not match")

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, 
                                                  DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use specified format")

        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }
        
        task_list.append(new_task)

        add_task()
        print("Task successfully added.")


    elif menu == 'va':
        '''Reads the task from task.txt file and prints to the console 
        '''
            
        view_all()

    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console
        '''
        
        view_mine(curr_user)

        user_task = input("""\nEnter a task number to edit 
or enter -1 to return to main menu: """)
        if user_task == '-1':
            continue
        else:
            menu2 =input('''\nSelect one of the following options:
ed - Edit username or due date for this task
cm - Mark this task as complete
-1 - Return to main menu
: ''').lower()
            if menu2 == '-1':
                continue

            # mark task as completed
            elif menu2 == 'cm':
                for i, t in enumerate(task_list,1):
                        if (t['username'] == curr_user 
                            and i == int(user_task)):
                            t['completed'] = True
                add_task()

            elif menu2 == 'ed':
                user_edit = input("""\nWould you like to edit username or due date? 
(Enter 'user' or 'date'): """)

                # update username of task
                if user_edit == 'user':
                    new_user = input("Enter new username: ")

                    for i, t in enumerate(task_list,1):
                                            if (t['username'] == curr_user 
                                                and i == int(user_task) 
                                                and t['completed'] != True):
                                                t['username'] = new_user

                    add_task()

                # update due_date of task
                elif user_edit == 'date':
                    while True:
                                try:
                                    new_date = input("""Due date of task 
                                                     (YYYY-MM-DD): """)
                                    new_date_time = datetime.strptime(
                                         new_date, DATETIME_STRING_FORMAT)
                                    break
                                except ValueError:
                                    print("""Invalid datetime format. 
                                          Please use the format specified""")


                    for i, t in enumerate(task_list,1):
                        if (t['username'] == curr_user 
                            and i == int(user_task) 
                            and t['completed'] != True):
                            t['due_date'] = new_date_time

                    add_task()

     # the user 'admin' can display statistics
                    
    elif menu == 'ds' and curr_user == 'admin': 
 

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users()}")
        print(f"Number of tasks: \t\t {num_tasks()}")
        print("-----------------------------------")    


    # the user 'admin' can generate reports

    elif menu == 'gr' and curr_user == 'admin':
        report_files()
        print("""\nReports successfully generated in 
user_overview.txt and task_overview.txt""")

    # exit program
    elif menu == 'e':
        print('\nGoodbye!!!')
        exit()

    else:
        print("\nYou have made a wrong choice, Please Try again")