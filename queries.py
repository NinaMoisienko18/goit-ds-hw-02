import psycopg2
from colorama import Fore, Style

db_params = {
    "database": "postgres",
    "user": "postgres",
    "host": "localhost",
    "password": "Lavanda18",
    "port": 5432
}


def show_all_users(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, fullname FROM users")
        users = cur.fetchall()

        user_ids = [row[0] for row in users]
        fullname_list = [row[1] for row in users]

        print("User IDs:", user_ids)
        print("Full Names:", fullname_list)

def all_tasks_of_user(conn):
    show_all_users(conn)
    with conn.cursor() as cur:
        user_input = input("Enter the ID of the user: ")
        cur.execute("SELECT title FROM tasks WHERE user_id = %s", (user_input,))
        tasks = cur.fetchall()
        conn.commit()
        print(f"User with id {user_input} has next tasks: ")
        for number, task in enumerate(tasks):
            print(f"\t{number + 1} ---> {task[0]}")


def tasks_with_status(conn):
    with conn.cursor() as cur:
        status_id = None
        status = None
        user_input = input("Enter status for tasks:\n1. new\n2. in progress \n3. completed\nAnswer: ")
        if user_input == "1":
            status_id = "1"
            status = "new"
        elif user_input == "2":
            status_id = "2"
            status = "in progress"

        elif user_input == "3":
            status_id = "3"
            status = "completes"
        cur.execute("SELECT title FROM tasks WHERE status_id = %s", (status_id,))
        tasks = cur.fetchall()
        conn.commit()
        print(f"Tasks with status {user_input}:")
        for number, task in enumerate(tasks):
            print(f"\t{number + 1} ---> {task[0]} [{status}]")


def update_task_status(conn):
    with conn.cursor() as cur:
        task_id = int(input("Enter the ID of the task: "))
        cur.execute("SELECT t.title, s.name FROM tasks t JOIN status s ON t.status_id = s.id WHERE t.id = %s",
                    (task_id,))
        task_info = cur.fetchone()

        if task_info:
            print(f"Current status of task '{task_info[0]}': {task_info[1]}")

            new_status = input("Enter the new status ('new', 'in progress', 'completed'): ")
            cur.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s",
                        (new_status, task_id))
            conn.commit()
            print(f"Task with id {task_id} status updated to {new_status}")
        else:
            print(f"No task found with ID {task_id}")

def get_users_without_tasks(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, fullname, email FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")
        users = cur.fetchall()
        conn.commit()
        print("Users without tasks: ")
        for user in users:
            print(f"ID: {user[0]}, Fullname: {user[1]}, Email: {user[2]}")

def add_task_for_user(conn):
    with conn.cursor() as cur:
        user_id = input("Enter the ID of the user: ")
        title = input("Enter the title of the task: ")
        description = input("Enter the description of the task: ")
        status = input("Enter the status of the task ('new', 'in progress', 'completed'): ")
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)", (title, description, status, user_id))
        conn.commit()
        print(f"Task '{title}' added for user with id {user_id}")

def get_uncompleted_tasks(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT t.id, t.title, t.description, t.status_id, t.user_id FROM tasks t JOIN status s ON t.status_id = s.id WHERE s.name <> 'completed'")
        tasks = cur.fetchall()
        conn.commit()
        print("Uncompleted tasks: ")
        for task in tasks:
            print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Status ID: {task[3]}, User ID: {task[4]}")

def delete_task(conn):
    with conn.cursor() as cur:
        task_id = input("Enter the ID of the task to delete: ")
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        print(f"Task with id {task_id} has been deleted")


def test_deleting(conn):
    show_all_users(conn)
    with conn.cursor() as cur:
        user_input = input("Enter the ID of the user to delete: ")
        cur.execute("DELETE FROM users WHERE id = %s", (user_input,))
        conn.commit()
        print(f"User with ID {user_input} has been deleted.")

def find_users_by_email(conn):
    with conn.cursor() as cur:
        email_part = input("Enter the part of the email to search: ")
        cur.execute("SELECT id, fullname, email FROM users WHERE email LIKE %s", ('%' + email_part + '%',))
        users = cur.fetchall()
        conn.commit()
        print("Users found: ")
        for user in users:
            print(f"ID: {user[0]}, Fullname: {user[1]}, Email: {user[2]}")

def update_user_name(conn):
    with conn.cursor() as cur:
        user_id = input("Enter the ID of the user: ")
        new_name = input("Enter the new full name of the user: ")
        cur.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_name, user_id))
        conn.commit()
        print(f"User with id {user_id} name updated to {new_name}")

def get_task_count_by_status(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT s.name AS status_name, COUNT(t.id) AS task_count FROM status s LEFT JOIN tasks t ON s.id = t.status_id GROUP BY s.name")
        status_counts = cur.fetchall()
        conn.commit()
        print("Task count by status: ")
        for status in status_counts:
            print(f"Status: {status[0]}, Task Count: {status[1]}")

def get_tasks_by_user_email_domain(conn):
    with conn.cursor() as cur:
        email_domain = input("Enter the email domain (e.g., '@example.com'): ")
        cur.execute("SELECT t.* FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE %s", ('%' + email_domain, ))
        tasks = cur.fetchall()
        conn.commit()
        print(f"Tasks for users with email domain '{email_domain}': ")
        for task in tasks:
            print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Status ID: {task[3]}, User ID: {task[4]}")

def get_tasks_without_description(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tasks WHERE description IS NULL OR description = ''")
        tasks = cur.fetchall()
        conn.commit()
        print("Tasks without description: ")
        for task in tasks:
            print(f"ID: {task[0]}, Title: {task[1]}, Status ID: {task[3]}, User ID: {task[4]}")

def get_users_and_in_progress_tasks(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT u.id, u.fullname, t.id AS task_id, t.title FROM users u INNER JOIN tasks t ON u.id = t.user_id WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress')")
        results = cur.fetchall()
        conn.commit()
        print("Users and their 'in progress' tasks: ")
        for row in results:
            print(f"User ID: {row[0]}, Fullname: {row[1]}, Task ID: {row[2]}, Task Title: {row[3]}")

def get_users_and_task_counts(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT u.id, u.fullname, COUNT(t.id) AS task_count FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.id, u.fullname")
        results = cur.fetchall()
        conn.commit()
        print("Users and their task counts: ")
        for row in results:
            print(f"User ID: {row[0]}, Fullname: {row[1]}, Task Count: {row[2]}")


def main():
    conn = psycopg2.connect(**db_params)
    # test_deleting(conn)
    # all_tasks_of_user(conn)
    # tasks_with_status(conn)
    # update_task_status(conn)
    # get_users_without_tasks(conn)
    # add_task_for_user(conn)
    # get_uncompleted_tasks(conn)
    # delete_task(conn)
    # find_users_by_email(conn)
    # update_user_name(conn)
    # get_task_count_by_status(conn)
    # get_tasks_by_user_email_domain(conn)
    # get_tasks_without_description(conn)
    # get_users_and_in_progress_tasks(conn)
    # get_users_and_task_counts(conn)
    conn.close()

if __name__ == "__main__":
    main()