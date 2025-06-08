from data_changed import ConsoleLogger
from data_changing import NameValidator, EmailValidator
from users import User

if __name__ == "__main__":
    user = User("Анна", "anna@stud.kantiana.ru")
    logger = ConsoleLogger()
    user.add_property_changed_listener(logger)

    name_validator = NameValidator()
    email_validator = EmailValidator()
    user.add_property_changing_listener(name_validator)
    user.add_property_changing_listener(email_validator)

    print("--- Корректные изменения ---")
    user.name = "Мария"
    user.email = "maria@stud.kantiana.ru"

    print("\n--- Некорректные изменения ---")
    user.name = 123
    user.name = "И1"
    user.email = True
    user.email = "ivan@gmail.com"

    print("\n--- Итоговые значения ---")
    print(f"Имя: {user.name}, Email: {user.email}")
