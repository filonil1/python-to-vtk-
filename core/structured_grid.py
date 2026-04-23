"""
Класс для структурированной ортогональной сетки.
Наследуется от BaseGrid и реализует регулярную сетку.
"""
from .base_grid import BaseGrid
from typing import Tuple, List


class StructuredOrthoGrid(BaseGrid):
    """
    Представляет регулярную ортогональную сетку в 3D пространстве.
    Состоит из кубических ячеек.
    """
    
    def __init__(self, length_x: float, length_y: float, length_z: float,
                 divisions_x: int, divisions_y: int, divisions_z: int,
                 origin: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                 name: str = "grid"):
        """
        Инициализация сетки.
        
        Args:
            length_x, length_y, length_z: Размеры сетки по осям
            divisions_x, divisions_y, divisions_z: Количество разбиений (ячеек)
            origin: Начальная точка сетки
            name: Название сетки
        """
        super().__init__(name)
        
        # Валидация
        if length_x <= 0 or length_y <= 0 or length_z <= 0:
            raise ValueError("Размеры сетки должны быть положительными")
        if divisions_x <= 0 or divisions_y <= 0 or divisions_z <= 0:
            raise ValueError("Количество разбиений должно быть положительным")
            
        self.length_x = length_x
        self.length_y = length_y
        self.length_z = length_z
        self.divisions_x = divisions_x
        self.divisions_y = divisions_y
        self.divisions_z = divisions_z
        self.origin = origin
        
        # Вычисляемые параметры
        self.spacing = (
            length_x / divisions_x,
            length_y / divisions_y,
            length_z / divisions_z
        )
        
        # Количество точек (разбиения + 1)
        self.nx = divisions_x + 1
        self.ny = divisions_y + 1
        self.nz = divisions_z + 1
    
    def get_dimensions(self) -> Tuple[int, int, int]:
        """Возвращает количество точек по осям (nx, ny, nz)."""
        return (self.nx, self.ny, self.nz)
    
    def get_spacing(self) -> Tuple[float, float, float]:
        """Возвращает шаги сетки (dx, dy, dz)."""
        return self.spacing
    
    def get_origin(self) -> Tuple[float, float, float]:
        """Возвращает начало координат сетки."""
        return self.origin
    
    def get_bounds(self) -> Tuple[float, float, float, float, float, float]:
        """Возвращает границы (xmin, xmax, ymin, ymax, zmin, zmax)."""
        return (
            self.origin[0], self.origin[0] + self.length_x,
            self.origin[1], self.origin[1] + self.length_y,
            self.origin[2], self.origin[2] + self.length_z
        )
    
    def get_number_of_points(self) -> int:
        """Общее количество точек."""
        return self.nx * self.ny * self.nz
    
    def get_number_of_cells(self) -> int:
        """Общее количество ячеек (кубов)."""
        return self.divisions_x * self.divisions_y * self.divisions_z
    
    def get_point_coordinates(self, i: int, j: int, k: int) -> Tuple[float, float, float]:
        """
        Возвращает координаты точки по индексам (i, j, k).
        """
        if not (0 <= i < self.nx and 0 <= j < self.ny and 0 <= k < self.nz):
            raise IndexError(f"Индексы ({i},{j},{k}) вне диапазона")
            
        x = self.origin[0] + i * self.spacing[0]
        y = self.origin[1] + j * self.spacing[1]
        z = self.origin[2] + k * self.spacing[2]
        
        return (x, y, z)
    
    def get_all_points(self) -> List[Tuple[float, float, float]]:
        """Возвращает список всех координат точек."""
        points = []
        for k in range(self.nz):
            for j in range(self.ny):
                for i in range(self.nx):
                    points.append(self.get_point_coordinates(i, j, k))
        return points
    
    def get_polygons_connectivity(self) -> List[List[int]]:
        """
        Генерирует список полигонов (граней) для всех кубов.
        Каждый куб имеет 6 граней.
        
        Returns:
            List[List[int]]: Список граней. Каждая грань: [4, id0, id1, id2, id3]
        """
        polygons = []
        
        # Проходим по каждому кубу (ячейке)
        for k in range(self.divisions_z):
            for j in range(self.divisions_y):
                for i in range(self.divisions_x):
                    # Индексы 8 вершин текущего куба
                    # Нижний слой (k)
                    p0 = k * self.ny * self.nx + j * self.nx + i
                    p1 = p0 + 1
                    p2 = p0 + self.nx + 1
                    p3 = p0 + self.nx
                    
                    # Верхний слой (k+1)
                    p4 = (k + 1) * self.ny * self.nx + j * self.nx + i
                    p5 = p4 + 1
                    p6 = p4 + self.nx + 1
                    p7 = p4 + self.nx
                    
                    # Добавляем 6 граней куба
                    # 1. Нижняя грань
                    polygons.append([4, p0, p3, p2, p1])
                    # 2. Верхняя грань
                    polygons.append([4, p4, p5, p6, p7])
                    # 3. Передняя грань
                    polygons.append([4, p0, p1, p5, p4])
                    # 4. Задняя грань
                    polygons.append([4, p2, p3, p7, p6])
                    # 5. Левая грань
                    polygons.append([4, p0, p4, p7, p3])
                    # 6. Правая грань
                    polygons.append([4, p1, p2, p6, p5])
        
        return polygons

    def get_grid_info(self) -> dict:
        """Полная информация о сетке."""
        return {
            'name': self.name,
            'dimensions': self.get_dimensions(),
            'divisions': (self.divisions_x, self.divisions_y, self.divisions_z),
            'number_of_points': self.get_number_of_points(),
            'number_of_cells': self.get_number_of_cells(),
            'number_of_polygons': len(self.get_polygons_connectivity()),
            'origin': self.get_origin(),
            'spacing': self.get_spacing(),
            'bounds': self.get_bounds()
        }
    
    def __repr__(self) -> str:
        dims = self.get_dimensions()
        cells = self.get_number_of_cells()
        return f"StructuredOrthoGrid('{self.name}', dims={dims}, cells={cells})"
