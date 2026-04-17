"""
Пакет writers содержит классы для записи сеток в различные VTK форматы.
"""

from .base_writer import BaseVTKWriter
from .legacy_ascii_writer import LegacyASCIIVTKWriter

__all__ = [
    'BaseVTKWriter',
    'LegacyASCIIVTKWriter',
]
