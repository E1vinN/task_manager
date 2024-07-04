import datetime
import json
import hashlib

# Function to hash a password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load data from the JSON file
def load_data():
    try:
        with open('task_manager_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Function to save data to the JSON file
def save_data(data):
    with open('task_manager_data.json', 'w') as file:
        json.dump(data, file, indent=4)

# Function to gather user information and store it in the JSON file
def user_information(username, password):
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    age = input("Enter your age: ")

    data = load_data()
    data[username] = {
        "password": password,
        "name": name,
        "address": address,
        "age": age,
        "tasks": []
    }
    save_data(data)

# Function to handle user signup process
def signup():
    username = input("Please enter the username you want to use: ")
    password = hash_password(input("Enter a password: "))
    user_information(username, password)
    print("Signup successful. Please proceed to log in.")
    login()

# Function to handle user login process
def login():
    while True:
        username = input("Enter your username (or type '1' to quit): ")
        if username == '1':
            print("Quitting login.")
            return
        
        entered_password = hash_password(input("Enter password: "))

        data = load_data()
        if username in data and data[username]["password"] == entered_password:
            while True:
                print("\n1--My Profile\n2--View your data\n3--Add task\n4--Update task\n5--View task status\n6--Delete task\n7--Logout")
                choice = input("\nChoose an option: ")
                
                if choice == '1':
                    view_profile(username)
                elif choice == '2':
                    view_data(username)
                elif choice == '3':
                    add_task(username)
                elif choice == '4':
                    update_task(username)
                elif choice == '5':
                    view_task_status(username)
                elif choice == '6':
                    delete_task(username)
                elif choice == '7':
                    print("Logging out...")
                    return
                else:
                    print("Invalid input!")
        else:
            print("Incorrect username or password.")

# Function to view user's profile
def view_profile(username):
    data = load_data()
    user_data = data.get(username, {})
    if user_data:
        print("Profile Information:")
        print(f"Name: {user_data.get('name', 'N/A')}")
        print(f"Address: {user_data.get('address', 'N/A')}")
        print(f"Age: {user_data.get('age', 'N/A')}")
    else:
        print("Profile not found.")

# Function to view user's data, specifically the list of tasks
def view_data(username):
    data = load_data()
    tasks = data.get(username, {}).get("tasks", [])
    if not tasks:
        print("No tasks found.")
    else:
        print("Your tasks:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. Task: {task['task']}, Target: {task['target']}, Status: {task['status']}")

# Function to add new tasks for the user
def add_task(username):
    num_tasks = int(input("Enter the number of tasks you want to add: "))
    tasks = []

    for i in range(1, num_tasks + 1):
        task = input(f"Enter task {i}: ")
        target = input(f"Enter target for task {i}: ")
        tasks.append({"task": task, "target": target, "status": "not started"})

    data = load_data()
    data[username]["tasks"].extend(tasks)
    save_data(data)
    print("Tasks added successfully.")

# Function to update the status of an existing task
def update_task(username):
    data = load_data()
    tasks = data[username]["tasks"]

    if not tasks:
        print("No tasks to update.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['task']} - {task['status']}")
    
    task_num = int(input("Enter the number of the task you want to update: ")) - 1
    
    if 0 <= task_num < len(tasks):
        new_status = input("Enter the new status (completed, ongoing, not started): ")
        tasks[task_num]["status"] = new_status
        save_data(data)
        print("Task updated successfully.")
    else:
        print("Invalid task number. Please try again.")

# Function to view the status of all tasks
def view_task_status(username):
    data = load_data()
    tasks = data[username]["tasks"]
    
    if not tasks:
        print("No tasks found.")
        return
    
    print("Task Status:")
    for task in tasks:
        print(f"Task: {task['task']}, Target: {task['target']}, Status: {task['status']}")

# Function to delete a task or all tasks
def delete_task(username):
    data = load_data()
    tasks = data[username]["tasks"]

    if not tasks:
        print("No tasks to delete.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['task']} - {task['status']}")

    task_num = int(input("Enter the number of the task you want to delete (or 0 to delete all tasks): ")) - 1
    
    if task_num == -1:
        confirm = input("Are you sure you want to delete all tasks? (yes/no): ")
        if confirm.lower() == 'yes':
            data[username]["tasks"] = []
            save_data(data)
            print("All tasks deleted successfully.")
        else:
            print("Deletion cancelled.")
    elif 0 <= task_num < len(tasks):
        tasks.pop(task_num)
        save_data(data)
        print("Task deleted successfully.")
    else:
        print("Invalid task number. Please try again.")

if __name__ == '__main__':
    print("TASK MANAGER")
    user_choice = int(input("Type 1 if you are new, otherwise type 0: "))
    
    if user_choice == 1:
        signup()
    elif user_choice == 0:
        login()
    else:
        print("Invalid input!")
