"""
Класс для представления структурированной ортогональной сетки.
Наследуется от BaseGrid и реализует все необходимые методы.
"""
from typing import Tuple, List
from .core.base_grid import BaseGrid


class StructuredOrthoGrid(BaseGrid):
    """
    Класс для работы со структурированной ортогональной сеткой.
    
    Представляет регулярную прямоугольную сетку в 3D пространстве,
    разбитую на равные интервалы по каждой оси.
    
    Атрибуты:
        length_x: Длина сетки по оси X
        length_y: Длина сетки по оси Y
        length_z: Длина сетки по оси Z
        divisions_x: Количество разбиений по оси X
        divisions_y: Количество разбиений по оси Y
        divisions_z: Количество разбиений по оси Z
        origin: Координаты начала сетки (x0, y0, z0)
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
        name: str = "structured_ortho_grid"
    ):
        """
        Инициализация структурированной ортогональной сетки.
        
        Args:
            length_x: Размер по оси X
            length_y: Размер по оси Y
            length_z: Размер по оси Z
            divisions_x: Количество интервалов по оси X
            divisions_y: Количество интервалов по оси Y
            divisions_z: Количество интервалов по оси Z
            origin: Координаты начала сетки (x0, y0, z0)
            name: Название сетки
            
        Raises:
            ValueError: Если размеры или разбиения некорректны
        """
        super().__init__(name)
        
        # Валидация входных данных
        if length_x <= 0 or length_y <= 0 or length_z <= 0:
            raise ValueError("Размеры сетки должны быть положительными")
        
        if divisions_x <= 0 or divisions_y <= 0 or divisions_z <= 0:
            raise ValueError("Количество разбиений должно быть положительным")
        
        self.length_x = float(length_x)
        self.length_y = float(length_y)
        self.length_z = float(length_z)
        
        self.divisions_x = int(divisions_x)
        self.divisions_y = int(divisions_y)
        self.divisions_z = int(divisions_z)
        
        self._origin = tuple(float(x) for x in origin)
        
        # Вычисляем шаги сетки (интервалы между точками)
        self._spacing_x = self.length_x / self.divisions_x
        self._spacing_y = self.length_y / self.divisions_y
        self._spacing_z = self.length_z / self.divisions_z
        
        # Вычисляем размеры (количество точек по каждой оси)
        self._dimensions_x = self.divisions_x + 1
        self._dimensions_y = self.divisions_y + 1
        self._dimensions_z = self.divisions_z + 1
    
    def get_dimensions(self) -> Tuple[int, int, int]:
        """
        Возвращает количество точек по каждой оси.
        
        Returns:
            Кортеж (nx, ny, nz) - количество точек
        """
        return (self._dimensions_x, self._dimensions_y, self._dimensions_z)
    
    def get_origin(self) -> Tuple[float, float, float]:
        """
        Возвращает координаты начала сетки.
        
        Returns:
            Кортеж (x0, y0, z0)
        """
        return self._origin
    
    def get_spacing(self) -> Tuple[float, float, float]:
        """
        Возвращает шаги сетки (интервалы между соседними точками).
        
        Returns:
            Кортеж (dx, dy, dz) - шаги по каждой оси
        """
        return (self._spacing_x, self._spacing_y, self._spacing_z)
    
    def get_number_of_points(self) -> int:
        """
        Вычисляет общее количество точек в сетке.
        
        Returns:
            Количество точек (nx * ny * nz)
        """
        return self._dimensions_x * self._dimensions_y * self._dimensions_z
    
    def get_number_of_cells(self) -> int:
        """
        Вычисляет общее количество ячеек в сетке.
        
        Returns:
            Количество ячеек (divisions_x * divisions_y * divisions_z)
        """
        return self.divisions_x * self.divisions_y * self.divisions_z
    
    def get_bounds(self) -> Tuple[float, float, float, float, float, float]:
        """
        Возвращает границы сетки.
        
        Returns:
            Кортеж (xmin, xmax, ymin, ymax, zmin, zmax)
        """
        x0, y0, z0 = self._origin
        return (
            x0,
            x0 + self.length_x,
            y0,
            y0 + self.length_y,
            z0,
            z0 + self.length_z
        )
    
    def get_grid_info(self) -> dict:
        """
        Возвращает полную информацию о сетке.
        
        Returns:
            Словарь с информацией о сетке
        """
        dims = self.get_dimensions()
        origin = self.get_origin()
        spacing = self.get_spacing()
        bounds = self.get_bounds()
        
        return {
            'name': self.name,
            'type': 'StructuredOrthoGrid',
            'dimensions': dims,
            'number_of_points': self.get_number_of_points(),
            'number_of_cells': self.get_number_of_cells(),
            'origin': origin,
            'spacing': spacing,
            'bounds': bounds,
            'divisions': (self.divisions_x, self.divisions_y, self.divisions_z),
            'lengths': (self.length_x, self.length_y, self.length_z)
        }
    
    def get_point_coordinates(self, i: int, j: int, k: int) -> Tuple[float, float, float]:
        """
        Вычисляет координаты точки по индексам (i, j, k).
        
        Args:
            i: Индекс по оси X (0 <= i < nx)
            j: Индекс по оси Y (0 <= j < ny)
            k: Индекс по оси Z (0 <= k < nz)
            
        Returns:
            Кортеж координат (x, y, z)
            
        Raises:
            IndexError: Если индексы вне границ
        """
        if not (0 <= i < self._dimensions_x):
            raise IndexError(f"Индекс i={i} вне границ [0, {self._dimensions_x})")
        if not (0 <= j < self._dimensions_y):
            raise IndexError(f"Индекс j={j} вне границ [0, {self._dimensions_y})")
        if not (0 <= k < self._dimensions_z):
            raise IndexError(f"Индекс k={k} вне границ [0, {self._dimensions_z})")
        
        x0, y0, z0 = self._origin
        x = x0 + i * self._spacing_x
        y = y0 + j * self._spacing_y
        z = z0 + k * self._spacing_z
        
        return (x, y, z)
    
    def get_all_points(self) -> List[Tuple[float, float, float]]:
        """
        Возвращает координаты всех точек сетки.
        
        Точки упорядочены так: x изменяется быстрее, затем y, затем z.
        
        Returns:
            Список кортежей координат
        """
        points = []
        for k in range(self._dimensions_z):
            for j in range(self._dimensions_y):
                for i in range(self._dimensions_x):
                    points.append(self.get_point_coordinates(i, j, k))
        return points
    
    def __str__(self) -> str:
        """Красивое строковое представление сетки."""
        info = self.get_grid_info()
        lines = [
            f"Структурированная ортогональная сетка: {self.name}",
            f"  Размеры по осям (X, Y, Z): {info['dimensions']}",
            f"  Количество точек: {info['number_of_points']}",
            f"  Количество ячеек: {info['number_of_cells']}",
            f"  Начало сетки (X, Y, Z): {info['origin']}",
            f"  Шаги сетки (dX, dY, dZ): {info['spacing']}",
            f"  Границы (Xmin, Xmax, Ymin, Ymax, Zmin, Zmax): {info['bounds']}"
        ]
        return "\n".join(lines)
    