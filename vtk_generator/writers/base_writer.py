"""Абстрактный базовый класс для VTK писателей."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.base_grid import BaseGrid


class BaseVTKWriter(ABC):
    """Абстрактный базовый класс для всех VTK писателей.
    
    Определяет общий интерфейс для записи сеток в различные VTK форматы.
    """
    
    def __init__(self, grid: 'BaseGrid'):
        """Инициализация писателя.
        
        Args:
            grid: Объект сетки для записи
            
        Raises:
            TypeError: Если grid не является экземпляром BaseGrid
        """
        from ..core.base_grid import BaseGrid
        
        if not isinstance(grid, BaseGrid):
            raise TypeError(f"Ожидается объект типа BaseGrid, получен {type(grid).__name__}")
        
        self._grid = grid
    
    @property
    def grid(self) -> 'BaseGrid':
        """Объект сетки."""
        return self._grid
    
    @abstractmethod
    def write(self, filepath: str) -> None:
        """Записывает сетку в файл.
        
        Args:
            filepath: Путь к выходному файлу
        """
        pass
    
    def _ensure_directory(self, filepath: str) -> Path:
        """Гарантирует существование директории для файла.
        
        Args:
            filepath: Путь к файлу
            
        Returns:
            Path объект файла
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
    
    def __str__(self) -> str:
        """Строковое представление писателя."""
        return f"{self.__class__.__name__}(grid={self._grid.name})"
