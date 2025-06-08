from enum import Enum
from typing import Self

# Константы для ANSI кодов форматирования
COLOR_FORMAT = "\033[{}m{}"
POSITION_FORMAT = "\033[{};{}H{}"


class TextColor(Enum):
    DEFAULT = 0
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37


class Printer:
    # Хранилище шрифтов
    _font_data = {}
    # Размеры символов по умолчанию
    _default_char_width = 5
    _default_char_height = 5

    def __init__(self, text_color: TextColor, start_position: tuple[int, int], fill_char: str) -> None:
        self.text_color = text_color
        self.fill_char = fill_char
        self.cursor_x, self.cursor_y = start_position

    @classmethod
    def initialize_font(cls, font_file: str = "font.txt") -> None:
        try:
            with open(font_file, "r") as font_data:
                cls._font_data.clear()
                # Чтение размеров символов
                cls._default_char_height = int(font_data.readline().strip())
                cls._default_char_width = int(font_data.readline().strip())

                # Добавление пробела как специального символа
                cls._font_data[' '] = [' ' * cls._default_char_width
                                       for _ in range(cls._default_char_height)]

                # Чтение символов из файла
                while True:
                    char_name = font_data.readline().replace('-', '').strip()
                    if not char_name:
                        break

                    cls._font_data[char_name] = []
                    for _ in range(cls._default_char_height):
                        char_line = font_data.readline()[:cls._default_char_width]
                        if '-' in char_line:
                            raise ValueError(
                                f"Некорректный файл шрифта. Загруженные символы: {cls._font_data.keys()}")
                        cls._font_data[char_name].append(char_line)
        except Exception as error:
            print(f"Ошибка загрузки шрифта: {error}")
            raise FileNotFoundError

    @classmethod
    def print_at_position(cls, text: str, color: TextColor,
                          position: tuple[int, int], char: str) -> None:
        if not cls._font_data:
            cls.initialize_font()

        start_x, start_y = position
        for character in text:
            if character not in cls._font_data:
                raise ValueError(f"Символ '{character}' отсутствует в файле шрифта")

            for line_index, pattern_line in enumerate(cls._font_data[character]):
                # Замена звездочек на нужный символ
                rendered_line = pattern_line.replace("*", char)
                # Установка позиции и цвета
                print(POSITION_FORMAT.format(
                    start_y + line_index + 1,
                    start_x + 1,
                    COLOR_FORMAT.format(color.value, rendered_line)),
                    end="")

            start_x += cls._default_char_width
        print()

    def __enter__(self) -> Self:
        print(COLOR_FORMAT.format(self.text_color.value, ''), end="")
        return self

    def __exit__(self, *args) -> None:
        print(COLOR_FORMAT.format(TextColor.DEFAULT.value, ''), end="")

    def render_text(self, text: str) -> None:
        if not self._font_data:
            self.initialize_font()

        x, y = self.cursor_x, self.cursor_y
        for character in text:
            if character not in self._font_data:
                continue

            for line_num, line_pattern in enumerate(self._font_data[character]):
                # Форматирование строки символа
                formatted_line = line_pattern.replace("*", self.fill_char)
                # Печать в указанной позиции
                print(POSITION_FORMAT.format(
                    y + line_num + 1,
                    x + 1,
                    formatted_line),
                    end="")

            x += self._default_char_width
        self.cursor_x = x


if __name__ == "__main__":
    # Статическая печать
    Printer.initialize_font(font_file="font5.txt")
    Printer.print_at_position("ABC", TextColor.RED, (5, 10), "#")

    # Печать через контекстный менеджер
    Printer.initialize_font(font_file="font7.txt")
    with Printer(TextColor.GREEN, (0, 20), "$") as printer:
        printer.render_text("HELLO ")
        printer.render_text("WORLD")