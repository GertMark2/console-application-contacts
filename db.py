import sqlite3
from utils import hash_password


class DatabaseManager:
    """
    Этот класс отвечает за взаимодействие с базой данных SQLite, создание таблиц и выполнение запросов

    Менеджер базы данных для работы с пользователями и контактами

    Attributes:
        conn: Соединение с базой данных
        cur: Курсор для выполнения SQL-запросов
    """

    def __init__(self, db_name: str) -> None:
        """
        Инициализирует соединение с базой данных и создает таблицы при необходимости
        Инициализирует менеджер базы данных

        Args:
            db_name (str): Имя файла базы данных
        """
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        """Создает таблицы в базе данных, если они не существуют"""
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE,
                            password TEXT)"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            first_name TEXT,
                            last_name TEXT,
                            phone TEXT,
                            email TEXT,
                            FOREIGN KEY (user_id) REFERENCES users(id))"""
        )
        self.conn.commit()

    def add_user(self, username: str, password: str) -> None:
        """
        Добавляет нового пользователя в базу данных в таблицу "users"

        Args:
            username (str): Имя пользователя
            password (str): Пароль пользователя
        """
        hashed_password = hash_password(password)
        self.cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        self.conn.commit()

    def authenticate_user(self, username: str, password: str) -> int | None:
        """
        Проверяет аутентификацию пользователя

        Аутентифицирует пользователя

        Args:
            username (str): Имя пользователя
            password (str): Пароль пользователя

        Returns:
            int | None: Идентификатор аутентифицированного пользователя или None, если пользователь не найден
        """
        hashed_password = hash_password(password)
        self.cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hashed_password),
        )
        user = self.cur.fetchone()
        if user:
            return user[0]
        else:
            return None

    def check_duplicate_phone(self, phone: str) -> bool:
        """
        Проверяет, существует ли контакт с указанным номером телефона в базе данных

        Args:
            phone (str): Номер телефона для проверки

        Returns:
            bool: True, если контакт с таким номером телефона существует, иначе False
        """
        self.cur.execute("SELECT COUNT(*) FROM contacts WHERE phone=?", (phone,))
        count = self.cur.fetchone()[0]
        return count > 0

    def add_contact(
        self, user_id: int, first_name: str, last_name: str, phone: str, email: str
    ) -> None:
        """
        Добавляет контакт в базу данных  в таблицу "contacts"

        Args:
            user_id (int): Идентификатор пользователя.
            first_name (str): Имя контакта.
            last_name (str): Фамилия контакта.
            phone (str): Номер телефона контакта.
            email (str): Email контакта.
        """
        self.cur.execute(
            "INSERT INTO contacts (user_id, first_name, last_name, phone, email) VALUES (?, ?, ?, ?, ?)",
            (user_id, first_name, last_name, phone, email),
        )
        self.conn.commit()

    def edit_contact(
        self,
        contact_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
    ) -> None:
        """
        Редактирует контакт в базе данных, в таблице "contacts"

        Args:
            contact_id (int | None): Идентификатор контакта
            first_name (str | None): Новое имя контакта. По умолчанию None
            last_name (str | None): Новая фамилия контакта. По умолчанию None
            phone (str | None): Новый номер телефона контакта. По умолчанию None
            email (str | None): Новый email контакта. По умолчанию None
        """
        update_query = "UPDATE contacts SET "
        update_params = []
        if first_name:
            update_query += "first_name=?, "
            update_params.append(first_name)
        if last_name:
            update_query += "last_name=?, "
            update_params.append(last_name)
        if phone:
            update_query += "phone=?, "
            update_params.append(phone)
        if email:
            update_query += "email=?, "
            update_params.append(email)
        update_query = update_query.rstrip(", ") + " WHERE id=?"
        update_params.append(contact_id)

        self.cur.execute(update_query, update_params)
        self.conn.commit()

    def delete_contact(self, contact_id: int) -> None:
        """
        Удаляет контакт из базы данных : из таблицы "contacts"

        Args:
            contact_id (int): Идентификатор контакта.
        """
        self.cur.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        self.conn.commit()

    def search_contacts(self, user_id: int, query: str) -> list[tuple]:
        """
        Выполняет поиск контактов в базе данных по запросу В.

        Args:
            user_id (int): Идентификатор пользователя.
            query (str): Поисковый запрос.

        Returns:
            list[tuple]: Список кортежей с результатами поиска.
        """
        search_query = "SELECT * FROM contacts WHERE user_id=? AND (first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR email LIKE ?)"
        search_params = (
            user_id,
            f"%{query}%",
            f"%{query}%",
            f"%{query}%",
            f"%{query}%",
        )
        self.cur.execute(search_query, search_params)
        return self.cur.fetchall()

    def get_contact_details(self, contact_id: int) -> tuple | None:
        """
        Получает детальную информацию о контакте из базы данных, из таблицы "contacts"

        Args:
            contact_id (int): Идентификатор контакта

        Returns:
            tuple | None: Кортеж с информацией о контакте или None, если контакт не найден
        """
        self.cur.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
        return self.cur.fetchone()

    def get_contacts(self, user_id: int) -> list[tuple]:
        """
        Получает список контактов пользователя из базы данных : из таблицы "contacts"

        Args:
            user_id (int): Идентификатор пользователя

        Returns:
            list[tuple]: Список кортежей с контактами пользователя
        """
        self.cur.execute("SELECT * FROM contacts WHERE user_id=?", (user_id,))
        return self.cur.fetchall()

    def clear_table(self, table_name: str) -> None:
        """
        Очищает указанную таблицу в базе данных

        Args:
            table_name (str): Имя таблицы
        """
        self.cur.execute(f"DELETE FROM {table_name}")
        self.conn.commit()

    def close_connection(self) -> None:
        """Закрывает соединение с базой данных"""
        self.conn.close()


class AuthManager:
    """
    Этот класс отвечает за управление аутентификацией пользователей

    Менеджер аутентификации пользователей

    Attributes:
        db (DatabaseManager): Менеджер базы данных для выполнения запросов
    """

    def __init__(self, db_manager: "DatabaseManager"):
        """
        Инициализирует объект менеджера аутентификации

        Args:
            db_manager (DatabaseManager): Менеджер базы данных для выполнения запросов
        """
        self.db = db_manager

    def register_user(self, username: str, password: str) -> None:
        """
        Регистрирует нового пользователя

        Args:
            username (str): Имя пользователя
            password (str): Пароль пользователя
        """
        self.db.add_user(username, password)

    def login(self, username: str, password: str) -> int | None:
        """
        Аутентифицирует пользователя  и возвращает его идентификатор

        Проверяет существование пользователя с указанным именем и паролем в базе данных

        Args:
            username (str): Имя пользователя
            password (str): Пароль пользователя

        Returns:
            int | None: Идентификатор аутентифицированного пользователя, если аутентификация успешна,
            иначе возвращает None
        """
        user_id = self.db.authenticate_user(username, password)
        if user_id:
            print("Login successful!")
            return user_id
        else:
            print("Invalid username or password!")
            return None


class ContactManager:
    """
    Этот класс управляет контактами пользователей

    Менеджер контактов пользователей

    Attributes:
        db (DatabaseManager): Менеджер базы данных для выполнения запросов
    """

    def __init__(self, db_manager: "DatabaseManager"):
        """
        Инициализирует объект менеджера контактов

        Args:
            db_manager (DatabaseManager): Менеджер базы данных для выполнения запросов
        """
        self.db = db_manager

    def add_contact(
        self, user_id: int, first_name: str, last_name: str, phone: str, email: str
    ) -> None:
        """
        Добавляет контакт пользователя, предварительно проверяя уникальность номера телефона

        Args:
            user_id (int): Идентификатор пользователя
            first_name (str): Имя контакта
            last_name (str): Фамилия контакта
            phone (str): Номер телефона контакта
            email (str): Email контакта
        """
        if self.db.check_duplicate_phone(phone):
            print("Контакт с таким номером телефона уже существует!")
            return

        self.db.add_contact(user_id, first_name, last_name, phone, email)

    def edit_contact(
        self,
        contact_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
    ) -> None:
        """
        Редактирует контакт пользователя

        Args:
            contact_id (int): Идентификатор контакта
            first_name ( str | None): Новое имя контакта. По умолчанию None
            last_name ( str | None): Новая фамилия контакта. По умолчанию None
            phone ( str | None): Новый номер телефона контакта. По умолчанию None
            email ( str | None): Новый email контакта. По умолчанию None
        """
        self.db.edit_contact(contact_id, first_name, last_name, phone, email)

    def delete_contact(self, contact_id: int) -> None:
        """
        Удаляет контакт пользователя

        Args:
            contact_id (int): Идентификатор контакта
        """
        self.db.delete_contact(contact_id)

    def search_contacts(self, user_id: int, query: str) -> None:
        """
        Поиск контактов пользователя

        Args:
            user_id (int): Идентификатор пользователя
            query (str): Поисковый запрос
        """
        contacts = self.db.search_contacts(user_id, query)
        for contact in contacts:
            print(contact)

    def view_contact_details(self, contact_id: int) -> None:
        """
        Просмотр детальной информации о контакте

        Args:
            contact_id (int): Идентификатор контакта
        """
        contact = self.db.get_contact_details(contact_id)
        if contact:
            print("Детальная информация о контакте:")
            print(f"Имя: {contact['first_name']}")
            print(f"Фамилия: {contact['last_name']}")
            print(f"Номер телефона: {contact['phone']}")
            print(f"Email: {contact['email']}")
        else:
            print("Контакт не найден!")

    def view_contacts(self, user_id: int) -> list[tuple]:
        """
        Получение списка контактов пользователя

        Args:
            user_id (int): Идентификатор пользователя

        Returns:
            list[tuple]: Список контактов пользователя
        """
        contacts = self.db.get_contacts(user_id)
        # for contact in contacts:
        #     print(f"ID: {contact[0]}, Имя: {contact[1]}, Фамилия: {contact[2]}, Номер телефона: {contact[3]}")
        return contacts

    # def view_contacts(self, user_id: int) -> None:
    #     """
    #     Просмотр контактов пользователя

    #     Args:
    #         user_id (int): Идентификатор пользователя
    #     """
    #     contacts = self.db.get_contacts(user_id)
    #     for contact in contacts:
    #         print(contact)
