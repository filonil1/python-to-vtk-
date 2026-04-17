"""
Пакет writers содержит классы для записи VTK файлов.
"""
from .base_writer import BaseVTKWriter
from .legacy_ascii_writer import LegacyASCIIVTKWriter, LegacyBINARYVTKWriter

__all__ = [
    'BaseVTKWriter',
    'LegacyASCIIVTKWriter',
    'LegacyBINARYVTKWriter',
]
