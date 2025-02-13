import psycopg2
import logging
import unittest

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Функция для получения подключения к базе данных
def get_connection():
    """Возвращает подключение к базе данных PostgreSQL."""
    return psycopg2.connect(
        database="clients_db",
        user="postgres",
        password="Serebro11!!",
        client_encoding="UTF-8"
    )

# Функция, создающая структуру БД (таблицы).
def create_db(conn):
    """Создает таблицы clients и phones, если они не существуют."""
    with conn.cursor() as cursor:
        try:
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
            """)
            conn.commit()
            logging.info("Таблицы clients и phones созданы или уже существуют.")
        except psycopg2.Error as e:
            conn.rollback()
            logging.error(f"Ошибка при создании таблиц: {e}")

# Функция, позволяющая добавить нового клиента.
def add_client(conn, first_name, last_name, email, phones=None):
    """
    Добавляет нового клиента в таблицу clients.

    :param conn: Подключение к базе данных.
    :param first_name: Имя клиента.
    :param last_name: Фамилия клиента.
    :param email: Email клиента.
    :param phones: Список телефонов клиента (опционально).
    :return: ID добавленного клиента или None в случае ошибки.
    """
    with conn.cursor() as cursor:
        try:
            # Проверяем, существует ли клиент с таким email
            cursor.execute("SELECT id FROM clients WHERE email = %s", (email,))
            existing_client = cursor.fetchone()

            if existing_client:
                logging.info(f"Клиент с email '{email}' уже существует. ID: {existing_client[0]}")
                return existing_client[0]  # Возвращаем существующий ID
            else:
                # Если клиента нет, добавляем его
                cursor.execute("""
                    INSERT INTO clients (first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id
                """, (first_name, last_name, email))
                client_id = cursor.fetchone()[0]
                logging.info(f"Добавлен новый клиент. ID: {client_id}")

                # Добавляем телефоны, если они есть
                if phones:
                    for phone in phones:
                        add_phone(conn, client_id, phone)

                conn.commit()
                return client_id

        except psycopg2.Error as e:
            conn.rollback()  # Откатываем транзакцию в случае ошибки
            logging.error(f"Ошибка при добавлении клиента: {e}")
            return None

# Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, client_id, phone):
    """
    Добавляет телефон для существующего клиента.

    :param conn: Подключение к базе данных.
    :param client_id: ID клиента.
    :param phone: Номер телефона.
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute("""
                INSERT INTO phones (client_id, phone) VALUES (%s, %s)
            """, (client_id, phone))
            conn.commit()
            logging.info(f"Телефон '{phone}' добавлен для клиента с ID: {client_id}")
        except psycopg2.Error as e:
            conn.rollback()
            logging.error(f"Ошибка при добавлении телефона: {e}")

# Функция, позволяющая изменить данные о клиенте.
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    """
    Изменяет данные о клиенте.

    :param conn: Подключение к базе данных.
    :param client_id: ID клиента.
    :param first_name: Новое имя клиента (опционально).
    :param last_name: Новая фамилия клиента (опционально).
    :param email: Новый email клиента (опционально).
    :param phones: Новый список телефонов клиента (опционально).
    """
    try:
        with conn.cursor() as cursor:
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
            logging.info(f"Данные клиента с ID: {client_id} успешно изменены.")
    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"Ошибка при изменении данных клиента: {e}")

# Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(conn, client_id, phone):
    """
    Удаляет телефон для существующего клиента.

    :param conn: Подключение к базе данных.
    :param client_id: ID клиента.
    :param phone: Номер телефона.
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute("""
                DELETE FROM phones WHERE client_id = %s AND phone = %s
            """, (client_id, phone))
            conn.commit()
            logging.info(f"Телефон '{phone}' удален для клиента с ID: {client_id}")
        except psycopg2.Error as e:
            conn.rollback()
            logging.error(f"Ошибка при удалении телефона: {e}")

# Функция, позволяющая удалить существующего клиента.
def delete_client(conn, client_id):
    """
    Удаляет существующего клиента.

    :param conn: Подключение к базе данных.
    :param client_id: ID клиента.
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute("""
                DELETE FROM phones WHERE client_id = %s
            """, (client_id,))
            cursor.execute("""
                DELETE FROM clients WHERE id = %s
            """, (client_id,))
            conn.commit()
            logging.info(f"Клиент с ID: {client_id} успешно удален.")
        except psycopg2.Error as e:
            conn.rollback()
            logging.error(f"Ошибка при удалении клиента: {e}")

# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    """
    Ищет клиента по указанным данным.

    :param conn: Подключение к базе данных.
    :param first_name: Имя клиента (опционально).
    :param last_name: Фамилия клиента (опционально).
    :param email: Email клиента (опционально).
    :param phone: Номер телефона клиента (опционально).
    """
    query = """
        SELECT c.id, c.first_name, c.last_name, c.email, p.phone
        FROM clients c
        LEFT JOIN phones p ON c.id = p.client_id
        WHERE 1=1
    """
    params = []

    if first_name:
        query += " AND c.first_name = %s"
        params.append(first_name)
    if last_name:
        query += " AND c.last_name = %s"
        params.append(last_name)
    if email:
        query += " AND c.email = %s"
        params.append(email)
    if phone:
        query += " AND p.phone = %s"
        params.append(phone)

    with conn.cursor() as cursor:
        try:
            cursor.execute(query, params)
            for row in cursor.fetchall():
                logging.info(f"Найден клиент: {row}")
        except psycopg2.Error as e:
            logging.error(f"Ошибка при поиске клиента: {e}")

# Тесты
class TestClientDB(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовой базы данных."""
        self.conn = get_connection()
        create_db(self.conn)

    def tearDown(self):
        """Очистка тестовой базы данных."""
        with self.conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS phones, clients CASCADE")
        self.conn.commit()
        self.conn.close()

    def test_add_client(self):
        """Тест добавления клиента."""
        client_id = add_client(self.conn, 'Иван', 'Иванов', 'ivan@example.com')
        self.assertIsNotNone(client_id)

    def test_add_phone(self):
        """Тест добавления телефона."""
        client_id = add_client(self.conn, 'Иван', 'Иванов', 'ivan@example.com')
        add_phone(self.conn, client_id, '123456789')
        find_client(self.conn, phone='123456789')

    def test_change_client(self):
        """Тест изменения данных клиента."""
        client_id = add_client(self.conn, 'Иван', 'Иванов', 'ivan@example.com')
        change_client(self.conn, client_id, first_name='Петр')
        find_client(self.conn, first_name='Петр')

    def test_delete_client(self):
        """Тест удаления клиента."""
        client_id = add_client(self.conn, 'Иван', 'Иванов', 'ivan@example.com')
        delete_client(self.conn, client_id)
        find_client(self.conn, first_name='Иван')

# Основной блок
if __name__ == "__main__":
    # Запуск тестов
    unittest.main()

    # Пример использования
    with get_connection() as conn:
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