"""Класс для структурированной ортогональной сетки."""

from typing import Tuple, List, Dict, Any
from .base_grid import BaseGrid


class StructuredOrthoGrid(BaseGrid):
    """Представляет регулярную ортогональную сетку в 3D пространстве.
    
    Сетка определяется размерами, количеством разбиений и начальной точкой.
    Все ячейки являются прямоугольными параллелепипедами.
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
        """Инициализация структурированной ортогональной сетки.
        
        Args:
            length_x: Размер сетки по оси X
            length_y: Размер сетки по оси Y
            length_z: Размер сетки по оси Z
            divisions_x: Количество интервалов (ячеек) по оси X
            divisions_y: Количество интервалов (ячеек) по оси Y
            divisions_z: Количество интервалов (ячеек) по оси Z
            origin: Координаты начальной точки (x0, y0, z0)
            name: Название сетки
            
        Raises:
            ValueError: Если параметры некорректны
        """
        super().__init__(name)
        
        # Валидация параметров
        self._validate_parameters(
            length_x, length_y, length_z,
            divisions_x, divisions_y, divisions_z,
            origin
        )
        
        self._length_x = length_x
        self._length_y = length_y
        self._length_z = length_z
        self._divisions_x = divisions_x
        self._divisions_y = divisions_y
        self._divisions_z = divisions_z
        self._origin = tuple(origin)
        
        # Вычисляемые параметры
        self._spacing_x = length_x / divisions_x
        self._spacing_y = length_y / divisions_y
        self._spacing_z = length_z / divisions_z
        
        # Количество точек = количество ячеек + 1
        self._nx = divisions_x + 1
        self._ny = divisions_y + 1
        self._nz = divisions_z + 1
    
    def _validate_parameters(
        self,
        length_x: float, length_y: float, length_z: float,
        divisions_x: int, divisions_y: int, divisions_z: int,
        origin: Tuple[float, float, float]
    ) -> None:
        """Валидация входных параметров.
        
        Raises:
            ValueError: Если параметры некорректны
        """
        if length_x <= 0 or length_y <= 0 or length_z <= 0:
            raise ValueError("Размеры сетки должны быть положительными числами")
        
        if divisions_x <= 0 or divisions_y <= 0 or divisions_z <= 0:
            raise ValueError("Количество разбиений должно быть положительным целым числом")
        
        if not isinstance(divisions_x, int) or not isinstance(divisions_y, int) or not isinstance(divisions_z, int):
            raise ValueError("Количество разбиений должно быть целым числом")
        
        if len(origin) != 3:
            raise ValueError("Origin должен содержать 3 координаты (x, y, z)")
    
    def get_dimensions(self) -> Tuple[int, int, int]:
        """Возвращает количество точек по каждой оси.
        
        Returns:
            Кортеж (nx, ny, nz) - количество точек по осям X, Y, Z
        """
        return (self._nx, self._ny, self._nz)
    
    def get_spacing(self) -> Tuple[float, float, float]:
        """Возвращает шаги сетки по каждой оси.
        
        Returns:
            Кортеж (dx, dy, dz) - шаги сетки по осям
        """
        return (self._spacing_x, self._spacing_y, self._spacing_z)
    
    def get_origin(self) -> Tuple[float, float, float]:
        """Возвращает координаты начальной точки сетки.
        
        Returns:
            Кортеж (x0, y0, z0) - координаты начала сетки
        """
        return self._origin
    
    def get_number_of_points(self) -> int:
        """Возвращает общее количество точек в сетке.
        
        Returns:
            Количество точек
        """
        return self._nx * self._ny * self._nz
    
    def get_number_of_cells(self) -> int:
        """Возвращает общее количество ячеек в сетке.
        
        Returns:
            Количество ячеек
        """
        return self._divisions_x * self._divisions_y * self._divisions_z
    
    def get_point_coordinates(self, i: int, j: int, k: int) -> Tuple[float, float, float]:
        """Возвращает координаты точки по индексам.
        
        Args:
            i: Индекс по оси X (0 <= i < nx)
            j: Индекс по оси Y (0 <= j < ny)
            k: Индекс по оси Z (0 <= k < nz)
            
        Returns:
            Кортеж (x, y, z) - координаты точки
            
        Raises:
            IndexError: Если индексы выходят за границы сетки
        """
        if not (0 <= i < self._nx):
            raise IndexError(f"Индекс i={i} выходит за границы [0, {self._nx})")
        if not (0 <= j < self._ny):
            raise IndexError(f"Индекс j={j} выходит за границы [0, {self._ny})")
        if not (0 <= k < self._nz):
            raise IndexError(f"Индекс k={k} выходит за границы [0, {self._nz})")
        
        x = self._origin[0] + i * self._spacing_x
        y = self._origin[1] + j * self._spacing_y
        z = self._origin[2] + k * self._spacing_z
        
        return (x, y, z)
    
    def get_all_points(self) -> List[Tuple[float, float, float]]:
        """Возвращает список всех координат точек.
        
        Точки упорядочены: сначала по X, затем по Y, затем по Z.
        
        Returns:
            Список кортежей с координатами точек
        """
        points = []
        for k in range(self._nz):
            for j in range(self._ny):
                for i in range(self._nx):
                    points.append(self.get_point_coordinates(i, j, k))
        return points
    
    def get_bounds(self) -> Tuple[float, float, float, float, float, float]:
        """Возвращает границы сетки.
        
        Returns:
            Кортеж (x_min, x_max, y_min, y_max, z_min, z_max)
        """
        return (
            self._origin[0],
            self._origin[0] + self._length_x,
            self._origin[1],
            self._origin[1] + self._length_y,
            self._origin[2],
            self._origin[2] + self._length_z
        )
    
    def get_divisions(self) -> Tuple[int, int, int]:
        """Возвращает количество разбиений (ячеек) по каждой оси.
        
        Returns:
            Кортеж (na, nb, nc) - количество ячеек по осям
        """
        return (self._divisions_x, self._divisions_y, self._divisions_z)
    
    def get_lengths(self) -> Tuple[float, float, float]:
        """Возвращает размеры сетки по каждой оси.
        
        Returns:
            Кортеж (length_x, length_y, length_z)
        """
        return (self._length_x, self._length_y, self._length_z)
    
    def get_grid_info(self) -> Dict[str, Any]:
        """Возвращает полную информацию о сетке.
        
        Returns:
            Словарь с информацией о сетке
        """
        info = super().get_grid_info()
        info.update({
            "divisions": self.get_divisions(),
            "lengths": self.get_lengths()
        })
        return info
