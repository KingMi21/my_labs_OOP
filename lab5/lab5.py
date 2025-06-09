from user_parse import UserRepository
from user import User
from authorization import AuthService
from typing import Optional


def colorize(text: str, color_code: int) -> str:
    return f"\033[{color_code}m{text}\033[0m"


def text_color(text: str) -> str:
    return colorize(text, 33)


def beautiful_bool(value: bool) -> str:
    return colorize("True" if value else "False", 32 if value else 31)


def beautiful_none(value: Optional[str]) -> str:
    return colorize(str(value), 33 if value is None else 32)


if __name__ == "__main__":
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)

    users = [
        User(0, "admin", "secret", "Administrator", "admin@stud.kantiana.ru"),
        User(1, "user1", "1234", "Ivan Ivanov", "ivanov@stud.kantiana.ru", "Pushkina 123"),
    ]

    for user in users:
        if not user_repo.get_by_id(user.id):
            user_repo.add(user)


    def print_auth_status():
        print(f"Текущий статус авторизации:")
        print(f"Авторизован:    {beautiful_bool(auth_service.is_authorized)}")
        print(f"Текущий пользователь: {beautiful_none(auth_service.current_user)}")
        print()


    print(f"1. {text_color('Попытка автоматической авторизации:')}")
    print_auth_status()

    print(f"2. {text_color('Попытка входа с неверным паролем:')}")
    success = auth_service.sign_in("admin", "1234")
    print(f"Успешно:        {beautiful_bool(success)}")
    print_auth_status()

    print(f"3. {text_color('Успешный вход в систему:')}")
    success = auth_service.sign_in("admin", "secret")
    print(f"Успешно:        {beautiful_bool(success)}")
    print_auth_status()

    print(f"4. {text_color('Выход из системы:')}")
    auth_service.sign_out()
    print_auth_status()

    print(f"5. {text_color('Авторизация после выхода:')}")
    success = auth_service.sign_in("user1", "1234")
    print(f"Успешно:        {beautiful_bool(success)}")
    print_auth_status()

    print(f"6. {text_color('Обновление данных пользователя:')}")
    user = user_repo.get_by_login("user1")
    user.name = "Peter Petrov"
    user_repo.update(user)
    print("Обновлённый пользователь:")
    print(colorize(user_repo.get_by_id(user.id), 32))
