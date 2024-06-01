-- Створення таблиці users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Створення таблиці status
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Попереднє заповнення таблиці status унікальними значеннями
INSERT INTO status (name) VALUES
('new'),
('in progress'),
('completed')
ON CONFLICT (name) DO NOTHING; -- Ігнорує спроби вставки дублікатів

-- Створення таблиці tasks
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES status (id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE SET NULL
);
