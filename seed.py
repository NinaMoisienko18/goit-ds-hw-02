import psycopg2
from faker import Faker
import random

fake = Faker()

db_params = {
    "database": "postgres",
    "user": "postgres",
    "host": "localhost",
    "password": "Lavanda18",
    "port": 5432
}

def create_users(conn, n=10):
    with conn.cursor() as cur:
        for _ in range(n):
            fullname = fake.name()
            email = fake.email()
            cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
        conn.commit()

def create_statuses(conn):
    statuses = ['new', 'in progress', 'completed']
    with conn.cursor() as cur:
        for status in statuses:
            cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (status,))
        conn.commit()

def create_tasks(conn, n=30):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT id FROM status")
        status_ids = [row[0] for row in cur.fetchall()]

        for _ in range(n):
            title = fake.sentence(nb_words=6)
            description = fake.text(max_nb_chars=200)
            status_id = random.choice(status_ids)
            user_id = random.choice(user_ids)
            cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", (title, description, status_id, user_id))
        conn.commit()

def test_deleting(conn):
    with conn.cursor() as cur:
        # Виконання запиту для отримання користувачів
        cur.execute("SELECT id, fullname FROM users")
        users = cur.fetchall()

        # Отримання списку user_id та імен користувачів
        user_ids = [row[0] for row in users]
        fullname_list = [row[1] for row in users]

        # Виведення списків
        print("User IDs:", user_ids)
        print("Full Names:", fullname_list)

        # Введення ID користувача, якого потрібно видалити
        user_input = input("Enter the ID of the user to delete: ")

        # Видалення користувача з бази даних
        cur.execute("DELETE FROM users WHERE id = %s", (user_input,))
        conn.commit()
        print(f"User with ID {user_input} has been deleted.")

def main():
    conn = psycopg2.connect(**db_params)

    create_statuses(conn)
    create_users(conn, 10)
    create_tasks(conn, 30)
    print("База даних успішно заповнена випадковими даними.")

    test_deleting(conn)

    conn.close()

if __name__ == "__main__":
    main()