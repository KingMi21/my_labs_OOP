from Point2d import Point2D
from Vector2d import Vector2D


def demonstrate_point_class():
    point_a = Point2D(1, 2)
    point_b = Point2D(4, 6)

    point_a_copy = Point2D(1, 2)

    print(f"Точка A: {point_a}")
    print(f"Точка B: {point_b}")
    print(f"Точки равны? {point_a == point_b}", end="\n\n")

    print(f"Точка A: {point_a}")
    print(f"Точка A': {point_a_copy}")
    print(f"Точки равны? {point_a == point_a_copy}")


def demonstrate_vector_operations():
    point_a = Point2D(1, 2)
    point_b = Point2D(4, 6)

    vec1 = Vector2D(1, 2)
    vec2 = Vector2D.from_points(point_a, point_b)  # (3, 4)

    print(f"\nВектор 1: {vec1}")
    print(f"Вектор 2 (из точек A и B): {vec2}")
    print(f"Длина вектора 1: {vec1.magnitude():.1f}")

    print(f"\nСумма векторов: {vec1 + vec2}")
    print(f"Разность векторов: {vec2 - vec1}")
    print(f"Умножение вектора на скаляр: {vec1 * 2}")
    print(f"Умножение вектора на скаляр: {3 * vec1}")
    print(f"Деление вектора на скаляр: {vec2 / 2}")

    print("\nСкалярное произведение:")  # 1*3 + 2*4 = 3 + 8 = 11
    print(f"Метод экземпляра: {vec1.dot_product(vec2)}")
    print(f"Статический метод: {Vector2D.calculate_dot_product(vec1, vec2)}")

    print("\nВекторное произведение (Z компонента):")  # 1*4 - 2*3 = 4 - 6 = -2
    print(f"Метод экземпляра: {vec1.cross_product(vec2)}")
    print(f"Статический метод: {Vector2D.calculate_cross_product(vec1, vec2)}")

    vec3 = Vector2D(5, 9)  # 3*9 - 5*4 = 27 - 20 = 7
    print("\nСмешанное произведение трех векторов:")  # 1*0 + 2*7 = 0 + 14 = 14
    print(f"Метод экземпляра: {vec1.triple_product(vec2, vec3)}")
    print(f"Статический метод: {Vector2D.calculate_triple_product(vec1, vec2, vec3)}")


if __name__ == "__main__":
    demonstrate_point_class()
    demonstrate_vector_operations()
