from typing import Self

# Глобальные константы для ограничения координат
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720


class Point2D:
    def __init__(self, x_coord: float, y_coord: float) -> None:
        self.x = x_coord
        self.y = y_coord

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        if not 0 <= value <= SCREEN_WIDTH:
            raise ValueError(f"X координата должна быть между 0 и {SCREEN_WIDTH}")
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        if not 0 <= value <= SCREEN_HEIGHT:
            raise ValueError(f"Y координата должна быть между 0 и {SCREEN_HEIGHT}")
        self._y = value

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"Point2D({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()
