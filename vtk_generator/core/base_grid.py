"""Абстрактный базовый класс для сеток."""

from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Any


class BaseGrid(ABC):
    """Абстрактный базовый класс для всех типов сеток.
    
    Определяет общий интерфейс для работы с различными типами сеток.
    """
    
    def __init__(self, name: str = "grid"):
        """Инициализация базовой сетки.
        
        Args:
            name: Название сетки
        """
        self._name = name
    
    @property
    def name(self) -> str:
        """Название сетки."""
        return self._name
    
    @abstractmethod
    def get_dimensions(self) -> Tuple[int, int, int]:
        """Возвращает количество точек по каждой оси.
        
        Returns:
            Кортеж (nx, ny, nz) - количество точек по осям X, Y, Z
        """
        pass
    
    @abstractmethod
    def get_spacing(self) -> Tuple[float, float, float]:
        """Возвращает шаги сетки по каждой оси.
        
        Returns:
            Кортеж (dx, dy, dz) - шаги сетки по осям
        """
        pass
    
    @abstractmethod
    def get_origin(self) -> Tuple[float, float, float]:
        """Возвращает координаты начальной точки сетки.
        
        Returns:
            Кортеж (x0, y0, z0) - координаты начала сетки
        """
        pass
    
    @abstractmethod
    def get_number_of_points(self) -> int:
        """Возвращает общее количество точек в сетке.
        
        Returns:
            Количество точек
        """
        pass
    
    @abstractmethod
    def get_number_of_cells(self) -> int:
        """Возвращает общее количество ячеек в сетке.
        
        Returns:
            Количество ячеек
        """
        pass
    
    @abstractmethod
    def get_point_coordinates(self, i: int, j: int, k: int) -> Tuple[float, float, float]:
        """Возвращает координаты точки по индексам.
        
        Args:
            i: Индекс по оси X
            j: Индекс по оси Y
            k: Индекс по оси Z
            
        Returns:
            Кортеж (x, y, z) - координаты точки
        """
        pass
    
    @abstractmethod
    def get_all_points(self) -> List[Tuple[float, float, float]]:
        """Возвращает список всех координат точек.
        
        Returns:
            Список кортежей с координатами точек
        """
        pass
    
    @abstractmethod
    def get_bounds(self) -> Tuple[float, float, float, float, float, float]:
        """Возвращает границы сетки.
        
        Returns:
            Кортеж (x_min, x_max, y_min, y_max, z_min, z_max)
        """
        pass
    
    def get_grid_info(self) -> Dict[str, Any]:
        """Возвращает полную информацию о сетке.
        
        Returns:
            Словарь с информацией о сетке
        """
        return {
            "name": self.name,
            "dimensions": self.get_dimensions(),
            "spacing": self.get_spacing(),
            "origin": self.get_origin(),
            "number_of_points": self.get_number_of_points(),
            "number_of_cells": self.get_number_of_cells(),
            "bounds": self.get_bounds()
        }
    
    def __str__(self) -> str:
        """Строковое представление сетки."""
        info = self.get_grid_info()
        return (f"{self.__class__.__name__}(name='{self.name}', "
                f"dimensions={info['dimensions']}, "
                f"points={info['number_of_points']}, "
                f"cells={info['number_of_cells']})")
