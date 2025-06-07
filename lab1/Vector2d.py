from typing import Generator, Self
import math
from lab1.Point2d import Point2D


class Vector2D:
    def __init__(self, x_component: float, y_component: float) -> None:
        self.x = x_component
        self.y = y_component

    @classmethod
    def from_points(cls, start: Point2D, end: Point2D) -> Self:
        return cls(end.x - start.x, end.y - start.y)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Индекс вектора может быть только 0 (X) или 1 (Y)")

    def __setitem__(self, index: int, value: float) -> None:
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Индекс вектора может быть только 0 (X) или 1 (Y)")

    def __iter__(self) -> Generator[float, None, None]:
        yield self.x
        yield self.y

    def __len__(self) -> int:
        return 2

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    def magnitude(self) -> float:
        return math.hypot(self.x, self.y)

    __abs__ = magnitude  # Альтернативное имя для метода

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, Vector2D):
            raise TypeError("Аргумент должен быть типа Vector2D")
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        if not isinstance(other, Vector2D):
            raise TypeError("Аргумент должен быть типа Vector2D")
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Self:
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Self:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError("Нельзя делить вектор на 0")
        return Vector2D(self.x / scalar, self.y / scalar)

    def dot_product(self, other: 'Vector2D') -> float:
        if not isinstance(other, Vector2D):
            raise TypeError("Аргумент должен быть типа Vector2D")
        return self.x * other.x + self.y * other.y

    @classmethod
    def calculate_dot_product(cls, vec1: Self, vec2: Self) -> float:
        return vec1.dot_product(vec2)

    def cross_product(self, other: 'Vector2D') -> 'Vector2D':
        if not isinstance(other, Vector2D):
            raise TypeError("Аргумент должен быть типа Vector2D")
        return Vector2D(0, self.x * other.y - self.y * other.x)

    @classmethod
    def calculate_cross_product(cls, vec1: 'Vector2D', vec2: 'Vector2D') -> 'Vector2D':
        return vec1.cross_product(vec2)

    def triple_product(self, vec2: 'Vector2D', vec3: 'Vector2D') -> float:
        if not isinstance(vec2, Vector2D) or not isinstance(vec3, Vector2D):
            raise TypeError("Все аргументы должны быть типа Vector2D")

        cross = vec2.cross_product(vec3)
        return self.dot_product(cross)

    @classmethod
    def calculate_triple_product(cls, vec1: 'Vector2D', vec2: 'Vector2D', vec3: 'Vector2D') -> float:
        return vec1.triple_product(vec2, vec3)