"""
Реализация структурированной ортогональной сетки.
Наследуется от BaseGrid и представляет регулярную 3D сетку.
"""
from core.base_grid import BaseGrid
from typing import Tuple, List


class StructuredOrthoGrid(BaseGrid):
    """
    Класс для представления регулярной ортогональной сетки в 3D пространстве.

    Сетка определяется размерами, количеством разбиений и начальной точкой.
    Все ячейки являются прямоугольными параллелепипедами.

    Атрибуты:
        length_x, length_y, length_z: Размеры сетки по осям
        divisions_x, divisions_y, divisions_z: Количество интервалов по осям
        origin: Координаты начальной точки
        name: Название сетки
    """

    def __init__(
        self,
        length_x: float,
        length_y: float,
        length_z: float,
        divisions_x: int,
        divisions_y: int,
        divisions_z: int,
        origin: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        name: str = "grid"
    ):
        """
        Инициализация структурированной ортогональной сетки.

        Args:
            length_x: Размер сетки по оси X
            length_y: Размер сетки по оси Y
            length_z: Размер сетки по оси Z
            divisions_x: Количество разбиений по оси X
            divisions_y: Количество разбиений по оси Y
            divisions_z: Количество разбиений по оси Z
            origin: Координаты начальной точки (x0, y0, z0)
            name: Название сетки

        Raises:
            ValueError: Если размеры или разбиения некорректны
        """
        super().__init__(name)

        # Валидация размеров
        if length_x <= 0 or length_y <= 0 or length_z <= 0:
            raise ValueError("Размеры сетки должны быть положительными числами")

        # Валидация разбиений
        if divisions_x <= 0 or divisions_y <= 0 or divisions_z <= 0:
            raise ValueError("Количество разбиений должно быть положительным целым числом")

        self.length_x = length_x
        self.length_y = length_y
        self.length_z = length_z
        self.divisions_x = divisions_x
        self.divisions_y = divisions_y
        self.divisions_z = divisions_z
        self.origin = tuple(origin)

        # Вычисляемые параметры
        self.spacing = self._calculate_spacing()
        self.dimensions = self._calculate_dimensions()

    def _calculate_spacing(self) -> Tuple[float, float, float]:
        """Вычисляет шаги сетки по каждой оси."""
        dx = self.length_x / self.divisions_x
        dy = self.length_y / self.divisions_y
        dz = self.length_z / self.divisions_z
        return (dx, dy, dz)

    def _calculate_dimensions(self) -> Tuple[int, int, int]:
        """Вычисляет количество точек по каждой оси."""
        nx = self.divisions_x + 1
        ny = self.divisions_y + 1
        nz = self.divisions_z + 1
        return (nx, ny, nz)

    def get_dimensions(self) -> Tuple[int, int, int]:
        """Возвращает количество точек по каждой оси (nx, ny, nz)."""
        return self.dimensions

    def get_spacing(self) -> Tuple[float, float, float]:
        """Возвращает шаги сетки по каждой оси (dx, dy, dz)."""
        return self.spacing

    def get_origin(self) -> Tuple[float, float, float]:
        """Возвращает координаты начальной точки сетки."""
        return self.origin

    def get_number_of_points(self) -> int:
        """Возвращает общее количество точек в сетке."""
        nx, ny, nz = self.dimensions
        return nx * ny * nz

    def get_number_of_cells(self) -> int:
        """Возвращает общее количество ячеек в сетке."""
        return self.divisions_x * self.divisions_y * self.divisions_z

    def get_bounds(self) -> Tuple[float, float, float, float, float, float]:
        """
        Возвращает границы сетки (xmin, xmax, ymin, ymax, zmin, zmax).
        """
        x0, y0, z0 = self.origin
        xmin, xmax = x0, x0 + self.length_x
        ymin, ymax = y0, y0 + self.length_y
        zmin, zmax = z0, z0 + self.length_z
        return (xmin, xmax, ymin, ymax, zmin, zmax)

    def get_point_coordinates(self, i: int, j: int, k: int) -> Tuple[float, float, float]:
        """
        Возвращает координаты точки по индексам (i, j, k).

        Args:
            i: Индекс по оси X (0 <= i < nx)
            j: Индекс по оси Y (0 <= j < ny)
            k: Индекс по оси Z (0 <= k < nz)

        Returns:
            Кортеж координат (x, y, z)

        Raises:
            IndexError: Если индексы выходят за границы
        """
        nx, ny, nz = self.dimensions

        if not (0 <= i < nx and 0 <= j < ny and 0 <= k < nz):
            raise IndexError(
                f"Индексы ({i}, {j}, {k}) выходят за границы сетки "
                f"({nx}, {ny}, {nz})"
            )

        x0, y0, z0 = self.origin
        dx, dy, dz = self.spacing

        x = x0 + i * dx
        y = y0 + j * dy
        z = z0 + k * dz

        return (x, y, z)

    def get_all_points(self) -> List[Tuple[float, float, float]]:
        """
        Возвращает список координат всех точек сетки.

        Returns:
            Список кортежей (x, y, z)
        """
        nx, ny, nz = self.dimensions
        points = []

        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    points.append(self.get_point_coordinates(i, j, k))

        return points

    def get_grid_info(self) -> dict:
        """
        Возвращает полную информацию о сетке.

        Returns:
            Словарь с информацией о сетке
        """
        return {
            'name': self.name,
            'dimensions': self.dimensions,
            'divisions': (self.divisions_x, self.divisions_y, self.divisions_z),
            'spacing': self.spacing,
            'origin': self.origin,
            'bounds': self.get_bounds(),
            'number_of_points': self.get_number_of_points(),
            'number_of_cells': self.get_number_of_cells(),
            'lengths': (self.length_x, self.length_y, self.length_z)
        }

    def __str__(self) -> str:
        """Строковое представление сетки."""
        info = self.get_grid_info()
        return (
            f"StructuredOrthoGrid '{self.name}':\n"
            f"  Размеры (точек): {info['dimensions']}\n"
            f"  Разбиения (ячеек): {info['divisions']}\n"
            f"  Шаги: {info['spacing']}\n"
            f"  Начало: {info['origin']}\n"
            f"  Точек: {info['number_of_points']:,}\n"
            f"  Ячеек: {info['number_of_cells']:,}"
        )