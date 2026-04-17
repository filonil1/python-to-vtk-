"""
Пакет core содержит базовые классы для работы с сетками.
"""

from .base_grid import BaseGrid
from .structured_grid import StructuredOrthoGrid

__all__ = [
    'BaseGrid',
    'StructuredOrthoGrid',
]