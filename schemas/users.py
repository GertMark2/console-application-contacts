from uuid import UUID
from utils import hash_password


class User:
    def __init__(self, user_id: UUID, phone: str, username: str, password: str):
        """Инициализирует объект пользователя"""
        self.__user_id: UUID = user_id
        self.__phone: str = phone
        self.__username: str = username
        self.__password: str = hash_password(password)

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта пользователя"""
        return f"User(id: {self.__user_id}, username: {self.__username}, phone: {self.__phone})"

    @property
    def username(self) -> str:
        """Возвращает имя пользователя"""
        return self.__username

    @property
    def password(self) -> str:
        """Возвращает хэшированный пароль пользователя"""
        return self.__password

    @property
    def user_id(self) -> UUID:
        """Возвращает идентификатор пользователя"""
        return self.__user_id

    @property
    def phone(self) -> str:
        """Возвращает номер телефона пользователя"""
        return self.__phone
