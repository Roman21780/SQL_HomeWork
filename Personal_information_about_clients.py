import psycopg2

# Функция, создающая структуру БД (таблицы).
def create_db(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(100) UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id),
                phone VARCHAR(15)
            )
        """)
        conn.commit()

# Функция, позволяющая добавить нового клиента.
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cursor:
        try:
            # Проверяем, существует ли клиент с таким email
            cursor.execute("SELECT id FROM clients WHERE email = %s", (email,))
            existing_client = cursor.fetchone()

            if existing_client:
                print(f"Клиент с email '{email}' уже существует. ID: {existing_client[0]}")
                return existing_client[0]  # Возвращаем существующий ID
            else:
                # если клиента нет, добавляем его
                cursor.execute("""
                    INSERT INTO clients (first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id
                """, (first_name, last_name, email))
                client_id = cursor.fetchone()[0]
                print(f"Добавлен новый клиент. ID: {client_id}")

                # добавляем телефоны, если они есть
                if phones:
                    for phone in phones:
                        add_phone(conn, client_id, phone)

                conn.commit()
                return client_id

        except psycopg2.Error as e:
            conn.rollback() # откатываем транзакцию в случае ошибки
            print(f"Ошибка при добавлении клиента: {e}")
            return None

# Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, client_id, phone):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO phones (client_id, phone) VALUES (%s, %s)
        """, (client_id, phone))
        conn.commit()

# Функция, позволяющая изменить данные о клиенте.
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn. cursor() as cursor:
        if first_name:
            cursor.execute("""
                UPDATE clients SET first_name = %s WHERE id = %s
            """, (first_name, client_id))
        if last_name:
            cursor.execute("""
                UPDATE clients SET last_name = %s WHERE id = %s
            """, (last_name, client_id))
        if email:
            cursor.execute("""
                UPDATE clients SET email = %s WHERE id = %s
            """, (email, client_id))
        if phones is not None:
            cursor.execute("""
                DELETE FROM phones WHERE client_id = %s
            """, (client_id,))
            for phone in phones:
                add_phone(conn, client_id, phone)

        conn.commit()

# Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cursor:
        cursor.execute("""
            DELETE FROM phones WHERE client_id = %s AND phone = %s
        """, (client_id, phone))
        conn.commit()

# Функция, позволяющая удалить существующего клиента.
def delete_client(conn, client_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            DELETE FROM phones WHERE client_id = %s
        """, (client_id,))
        cursor.execute("""
            DELETE FROM clients WHERE id = %s
        """, (client_id,))
        conn.commit()

# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    query = "SELECT c.id, c.first_name, c.last_name, c.email, p.phone FROM clients c LEFT JOIN phones p ON c.id = p.client_id WHERE "
    conditions = []
    params = []

    if first_name:
        conditions.append("c.first_name = %s")
        params.append(first_name)
    if last_name:
        conditions.append("c.last_name = %s")
        params.append(last_name)
    if email:
        conditions.append("c.email = %s")
        params.append(email)
    if phone:
        conditions.append("p.phone = %s")
        params.append(phone)

    query += " AND ".join(conditions)

    with conn.cursor() as cursor:
        cursor.execute(query, params)
        for row in cursor.fetchall():
            print(row)


# Пример использования
with psycopg2.connect(
        database="clients_db",
        user="postgres",
        password="Serebro11!!",
        client_encoding="UTF-8") as conn:
    create_db(conn)
    client_id1 = add_client(conn, 'Иван', 'Иванов',
                           'ivan@example.com', ['123456789', '987654321'])
    client_id2 = add_client(conn, 'Петр', 'Петров',
                            'petr@example.com')
    add_phone(conn, client_id1, '555555555')
    change_client(conn, client_id1, phones=['888888888'])
    find_client(conn, first_name='Иван')
    delete_phone(conn, client_id1, '888888888')
    delete_client(conn, client_id2)

# conn.close()