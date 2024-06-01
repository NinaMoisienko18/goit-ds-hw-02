import psycopg2


# Параметри підключення
connection_params = {
    "database": "postgres",
    "user": "postgres",
    "host": "localhost",
    "password": "Lavanda18",
    "port": 5432
}

# Шлях до SQL файлу
sql_file_path = 'task_system.sql'


def execute_sql_from_file(file_path, connection_params):
    # Підключення до бази даних
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Відкриття файлу SQL та виконання його вмісту
    with open(file_path, 'r') as file:
        sql_script = file.read()

    try:
        cursor.execute(sql_script)
        conn.commit()
        print("Таблиці були успішно створені відповідно до скрипта.")

    except Exception as e:
        print(f"Виникла помилка: {e}")
        conn.rollback()
    finally:

        cursor.close()
        conn.close()


# Виконання функції
execute_sql_from_file(sql_file_path, connection_params)
