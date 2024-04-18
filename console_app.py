from db import DatabaseManager
from db import AuthManager
from db import ContactManager
from reges import isValidEmail
from reges import isValidPhone

"""Это основная часть кода, где создается соединение с базой данных, инициализируются объекты менеджеров, и запускается пользовательский интерфейс
Oсновные шаги:
Инициализация соединения с базой данных
Создание объектов DatabaseManager, AuthManager и ContactManager
Представление пользователю меню для регистрации, входа и управления контактами
Обработка ввода пользователя и выполнение соответствующих действий
а также при необходимости очистка базы данных,которая закоментирована на данный момент"""


if __name__ == "__main__":
    db_name = "./contacts.db"
    db_manager = DatabaseManager(db_name)
    # db_manager.clear_table("users")
    # db_manager.clear_table("contacts")
    auth_manager = AuthManager(db_manager)
    contact_manager = ContactManager(db_manager)

    print("Добро пожаловать в нашу систему!")

    while True:
        print("\nМеню:")
        print("1. Регистрация")
        print("2. Вход")
        print("3. Выход")

        choice = input("Введите номер действия:")

        if choice == "1":
            username = input("Введите ваш ник:")
            password = input("Введите ваш пароль:")
            auth_manager.register_user(username, password)
            print("Регистрация прошла успешно!")
        elif choice == "2":
            username = input("Введите ваш ник:")
            password = input("Введите ваш пароль:")
            user_id = auth_manager.login(username, password)
            if user_id:
                print("Вход выполнен успешно!")
                while True:
                    print("\nМеню контактов:")
                    print("1. Добавить контакт")
                    print("2. Просмотреть контакты")
                    print("3. Редактировать контакт")
                    print("4. Удалить контакт")
                    print("5. Поиск контактов")
                    print("6. Просмотр детальной информации о контакте")
                    print("7. Выйти")

                    choice = input("Введите номер действия:")

                    if choice == "1":
                        while True:
                            print("\nДобавление контакта:")
                            first_name = input("Имя:")
                            last_name = input("Фамилия:")
                            phone = input(
                                "Введите номер телефона в формате 1234567890: "
                            )
                            while not isValidPhone(phone):
                                print(
                                    "Некорректный формат номера телефона. Пожалуйста, введите номер из 9-11 цифр без пробелов и дефисов"
                                )
                                phone = input(
                                    "Пожалуйста, введите номер телефона заново:"
                                )
                            email = input(
                                "Введите адрес электронной почты в формате name@gogle.com: "
                            )
                            while not isValidEmail(email):
                                print("Некорректный email")
                                email = input("Пожалуйста, введите email заново:")
                            contact_manager.add_contact(
                                user_id, first_name, last_name, phone, email
                            )
                            print("Контакт успешно добавлен!")

                            add_more = input(
                                "Желаете ли ещё добавить контакт? (да/нет):"
                            ).lower()
                            if add_more != "да":
                                break
                    elif choice == "2":
                        contacts = contact_manager.view_contacts(user_id)
                        if contacts:
                            print("\nСписок ваших контактов:")
                            for contact in contacts:
                                print(
                                    f"ID: {contact[0]}, Имя: {contact[2]}, Фамилия: {contact[3]}, Номер телефона: {contact[4]}"
                                )
                        else:
                            print("Ваш список контактов пуст!")
                    elif choice == "3":
                        print("\nРедактирование контакта:")
                        contactss = contact_manager.view_contacts(user_id)
                        if contactss:
                            print("\nСписок ваших контактов:")
                            for contact in contactss:
                                print(
                                    f"ID: {contact[0]}, Имя: {contact[2]}, Фамилия: {contact[3]}, Номер телефона: {contact[4]}"
                                )
                        else:
                            print("Ваш список контактов пуст!")
                        contact_id = input("Введите ID контакта для редактирования: ")
                        contact_details = db_manager.get_contact_details(contact_id)
                        if contact_details:
                            if contact_details[1] == user_id:
                                print("Текущие данные контакта:")
                                print("Имя:", contact_details[2])
                                print("Фамилия:", contact_details[3])
                                print("Номер телефона:", contact_details[4])
                                print("Email:", contact_details[5])
                                print(
                                    "\nВведите новые данные (оставьте пустыми, чтобы сохранить текущие):"
                                )
                                new_first_name = input("Новое имя:")
                                new_last_name = input("Новая фамилия:")
                                new_phone = input("Новый номер телефона:")
                                while new_phone and not isValidPhone(new_phone):
                                    print(
                                        "Номер телефона должен содержать только цифры"
                                    )
                                    new_phone = input("Новый номер телефона:")
                                new_email = input("Новый Email:")
                                while new_email and not isValidEmail(new_email):
                                    print(
                                        "Некорректный формат адреса электронной почты. Пожалуйста, введите валидный адрес."
                                    )
                                    new_email = input("Новый Email:")
                                db_manager.edit_contact(
                                    contact_id,
                                    first_name=new_first_name or contact_details[2],
                                    last_name=new_last_name or contact_details[3],
                                    phone=new_phone or contact_details[4],
                                    email=new_email or contact_details[5],
                                )

                                print("Контакт успешно отредактирован!")
                            else:
                                print(
                                    "Этот контакт не принадлежит вам, вы не можете его редактировать!"
                                )
                        else:
                            print("Контакт с указанным ID не найден!")
                    elif choice == "4":
                        print("\nУдаление контакта:")
                        contact_id = input("Введите ID контакта для удаления:")
                        contact_details = db_manager.get_contact_details(contact_id)
                        if contact_details:
                            if contact_details[1] == user_id:
                                confirm = input(
                                    "Вы уверены, что хотите удалить этот контакт? (да/нет):"
                                ).lower()
                                if confirm == "да":
                                    db_manager.delete_contact(contact_id)
                                    print("Контакт успешно удалён!")
                            else:
                                print(
                                    "Этот контакт не принадлежит вам,вы не можете его удалить!"
                                )
                        else:
                            print("Контакт с указанным ID не найден")
                    elif choice == "5":
                        search_query = input(
                            "Введите имя или номер телефона для поиска:"
                        )
                        search_results = db_manager.search_contacts(
                            user_id, search_query
                        )
                        if search_results:
                            print("\nРезультаты поиска:")
                            for contact in search_results:
                                print(contact)
                        else:
                            print("Контакты не найдены!")
                    elif choice == "6":
                        contact_id = input(
                            "Введите ID контакта для просмотра деталей: "
                        )
                        contact_details = db_manager.get_contact_details(contact_id)
                        if contact_details:
                            if contact_details[1] == user_id:
                                print("\nДетальная информация о контакте:")
                                print("Имя:", contact_details[2])
                                print("Фамилия:", contact_details[3])
                                print("Номер телефона:", contact_details[4])
                                print("Email:", contact_details[5])
                            else:
                                print(
                                    "Этот контакт не принадлежит вам,вы не можете просмотреть его детальную информацию"
                                )
                        else:
                            print("Контакт с указанным ID не найден")
                    elif choice == "7":
                        print("Выход из меню контактов")
                        break
                    else:
                        print("Некорректный выбор! Попробуйте снова")
            else:
                print("Неверный ник или пароль. Попробуйте снова")
        elif choice == "3":
            print("До свидания!")
            break
        else:
            print("Некорректный выбор. Попробуйте снова")

    db_manager.close_connection()
