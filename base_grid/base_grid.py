"""
Абстрактный базовый класс для представления сеток (грид).
Определяет интерфейс, который должны реализовать все типы сеток.
"""
from abc import ABC, abstractmethod
from typing import Tuple, List


class BaseGrid(ABC):
    """
    Абстрактный базовый класс для всех типов сеток.
    
    Атрибуты:
        name: Название сетки (используется в VTK файле)
    """
    
    def __init__(self, name: str = "grid"):
        """
        Инициализация базовой сетки.
        
        Args:
            name: Название сетки
        """
        self.name = name
    
    @abstractmethod
    def get_number_of_points(self) -> int:
        """Возвращает общее количество точек в сетке."""
        pass
    
    @abstractmethod
    def get_number_of_cells(self) -> int:
        """Возвращает общее количество ячеек в сетке."""
        pass
    
    @abstractmethod
    def get_dimensions(self) -> Tuple[int, int, int]:
        """
        Возвращает размеры сетки (nx, ny, nz).
        
        Returns:
            Кортеж (nx, ny, nz) - количество точек по каждой оси
        """
        pass
    
    @abstractmethod
    def get_origin(self) -> Tuple[float, float, float]:
        """
        Возвращает координаты начала сетки (x0, y0, z0).
        
        Returns:
            Кортеж (x0, y0, z0) - координаты начальной точки
        """
        pass
    
    @abstractmethod
    def get_bounds(self) -> Tuple[float, float, float, float, float, float]:
        """
        Возвращает границы сетки (xmin, xmax, ymin, ymax, zmin, zmax).
        
        Returns:
            Кортеж границ (xmin, xmax, ymin, ymax, zmin, zmax)
        """
        pass
    
    @abstractmethod
    def get_grid_info(self) -> dict:
        """
        Возвращает полную информацию о сетке.
        
        Returns:
            Словарь с информацией о сетке
        """
        pass
    
    def __repr__(self) -> str:
        """Строковое представление сетки."""
        dims = self.get_dimensions()
        points = self.get_number_of_points()
        return f"{self.__class__.__name__}(name='{self.name}', dimensions={dims}, points={points})"