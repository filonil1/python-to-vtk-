"""
Реализация писателя для VTK Legacy ASCII формата.
Наследуется от BaseVTKWriter и реализует запись в простой текстовый формат.
"""
from .base_writer import BaseVTKWriter
from ..core.structured_grid import StructuredOrthoGrid
from pathlib import Path
from typing import List, Tuple


class LegacyASCIIVTKWriter(BaseVTKWriter):
    """
    Писатель для VTK Legacy ASCII формата.
    
    Записывает структурированные ортогональные сетки в простой текстовый формат.
    Поддерживает STRUCTURED_POINTS тип набора данных.
    """
    
    VTK_VERSION = "2.0"
    
    def __init__(self, grid: StructuredOrthoGrid):
        """
        Инициализация Legacy ASCII писателя.
        
        Args:
            grid: Структурированная ортогональная сетка для записи
        """
        if not isinstance(grid, StructuredOrthoGrid):
            raise TypeError(
                f"grid должен быть StructuredOrthoGrid, получен {type(grid)}"
            )
        super().__init__(grid, file_format="ASCII")
    
    def write(self, filepath: str) -> None:
        """
        Записывает сетку в VTK файл в Legacy ASCII формате.
        
        Формат состоит из следующих частей:
        1. Версия и идентификатор файла
        2. Заголовок (до 256 символов)
        3. Формат файла (ASCII или BINARY)
        4. Описание сетки (DATASET STRUCTURED_POINTS)
        5. Описание точек данных (опционально)
        
        Args:
            filepath: Путь к файлу для записи
            
        Raises:
            IOError: Если возникла ошибка при записи
            ValueError: Если заголовок слишком длинный
        """
        path = self._validate_filepath(filepath)
        
        try:
            with open(path, 'w') as f:
                # Часть 1: Версия и идентификатор
                f.write(f"# vtk DataFile Version {self.VTK_VERSION}\n")
                
                # Часть 2: Заголовок
                header = self._get_header()
                self._validate_header(header)
                f.write(f"{header}\n")
                
                # Часть 3: Формат файла
                f.write(f"{self.file_format}\n")
                
                # Часть 4: Описание сетки (DATASET)
                self._write_dataset(f)
                
            print(f"✓ Файл успешно записан: {path}")
            self._print_write_info(path)
            
        except IOError as e:
            raise IOError(f"Ошибка при записи файла {filepath}: {e}")
    
    def _validate_header(self, header: str) -> None:
        """
        Валидирует заголовок VTK файла.
        
        Args:
            header: Заголовок для проверки
            
        Raises:
            ValueError: Если заголовок слишком длинный
        """
        if len(header) > 256:
            raise ValueError(
                f"Заголовок слишком длинный ({len(header)} > 256 символов)"
            )
    
    def _write_dataset(self, f) -> None:
        """
        Записывает описание сетки в формате DATASET STRUCTURED_POINTS.
        
        Args:
            f: Открытый файл для записи
        """
        dims = self.grid.get_dimensions()
        origin = self.grid.get_origin()
        spacing = self.grid.get_spacing()
        
        # Ключевое слово DATASET и тип
        f.write("DATASET STRUCTURED_POINTS\n")
        
        # Размеры сетки
        f.write(f"DIMENSIONS {dims[0]} {dims[1]} {dims[2]}\n")
        
        # Начало координат
        f.write(f"ORIGIN {origin[0]} {origin[1]} {origin[2]}\n")
        
        # Шаги сетки (интервалы между точками)
        f.write(f"SPACING {spacing[0]} {spacing[1]} {spacing[2]}\n")
    
    def _print_write_info(self, path: Path) -> None:
        """
        Выводит информацию о записанном файле.
        
        Args:
            path: Путь к записанному файлу
        """
        file_size = path.stat().st_size
        info = self.grid.get_grid_info()
        
        print(f"\n{'=' * 60}")
        print(f"Информация о записанном файле:")
        print(f"{'=' * 60}")
        print(f"Имя сетки: {info['name']}")
        print(f"Размеры (nx, ny, nz): {info['dimensions']}")
        print(f"Количество точек: {info['number_of_points']:,}")
        print(f"Количество ячеек: {info['number_of_cells']:,}")
        print(f"Начало сетки: {info['origin']}")
        print(f"Шаги сетки: {info['spacing']}")
        print(f"Границы сетки: {info['bounds']}")
        print(f"Размер файла: {file_size:,} байт")
        print(f"{'=' * 60}\n")


class LegacyBINARYVTKWriter(BaseVTKWriter):
    """
    Писатель для VTK Legacy BINARY формата.
    
    Записывает структурированные ортогональные сетки в бинарный формат.
    (Заготовка для будущей реализации)
    """
    
    def __init__(self, grid: StructuredOrthoGrid):
        """Инициализация Legacy BINARY писателя."""
        if not isinstance(grid, StructuredOrthoGrid):
            raise TypeError(
                f"grid должен быть StructuredOrthoGrid, получен {type(grid)}"
            )
        super().__init__(grid, file_format="BINARY")
    
    def write(self, filepath: str) -> None:
        """
        Записывает сетку в VTK файл в Legacy BINARY формате.
        
        Args:
            filepath: Путь к файлу для записи
            
        Raises:
            NotImplementedError: Функция еще не реализована
        """
        raise NotImplementedError(
            "BINARY формат пока не реализован. Используйте LegacyASCIIVTKWriter."
        )