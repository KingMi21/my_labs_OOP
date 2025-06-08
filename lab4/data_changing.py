from typing import Any
from protocols import PropertyChangingListenerProtocol, DataChangingProtocol, COLORING


class NameValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: DataChangingProtocol, property_name: str, old_value: Any,
                             new_value: Any) -> bool:
        if property_name != 'name':
            return True
        if not isinstance(new_value, str):
            print(COLORING.format(31, "Ошибка: Имя должно быть строкой!"))
            return False
        if not new_value.isalpha():
            print(COLORING.format(31, "Ошибка: Имя должно содержать только буквы!"))
            return False
        if len(new_value) < 2:
            print(COLORING.format(31, "Ошибка: Имя слишком короткое!"))
            return False
        print(COLORING.format(33, f"Имя объекта {str(obj)} изменяется с {old_value} на {new_value}"))
        return True


class EmailValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: DataChangingProtocol, property_name: str, old_value: Any,
                             new_value: Any) -> bool:
        if property_name != 'email':
            return True
        if not isinstance(new_value, str):
            print(COLORING.format(31, "Ошибка: Email должен быть строкой!"))
            return False
        if not ("@stud.kantiana.ru" in new_value):
            print(COLORING.format(31, "Ошибка: Email должен быть в домене BFU. Некорректный email."))
            return False
        print(COLORING.format(33, f"Email объекта {str(obj)} изменяется с {old_value} на {new_value}"))
        return True
