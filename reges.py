import re


def isValidEmail(email: str) -> bool:
    """
    Проверка адресов электронной почты на валидность
    Проверяет, является ли переданный адрес электронной почты допустимым


    Parametrs:
                email(str) Электронная почта для проверки

    Returns:
            Возвращает True,если адрес электронной почты допустимый,иначе False
    """
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    return bool(re.fullmatch(regex, email))


def isValidPhone(phone: str) -> bool:
    """
    Проверка телефонных номеров на валидность

    Parametrs:
                phone(str) Номер телефона для проверки

    Returns:
            bool:True, если номер телефона имеет корректный формат, иначе False
    """
    regex = re.compile(r"^((8|\+7)[\- ]?)?(\(?\d{3,4}\)?[\- ]?)?[\d\- ]{5,10}$")

    return bool(re.fullmatch(regex, phone))


isValidPhone("77475753908")
