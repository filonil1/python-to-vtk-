"""
Реализация писателя для VTK Legacy ASCII формата.
Наследуется от BaseVTKWriter и реализует запись в текстовый формат.
"""
from .base_writer import BaseVTKWriter
from core.structured_grid import StructuredOrthoGrid
from pathlib import Path


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
            
        Raises:
            TypeError: Если grid не является StructuredOrthoGrid
        """
        if not isinstance(grid, StructuredOrthoGrid):
            raise TypeError(
                f"grid должен быть StructuredOrthoGrid, получен {type(grid)}"
            )
        super().__init__(grid, file_format="ASCII")
    
    def write(self, filepath: str) -> None:
        """
        Записывает сетку в VTK файл в Legacy ASCII формате.
        
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
                if len(header) > 256:
                    raise ValueError(
                        f"Заголовок слишком длинный ({len(header)} > 256 символов)"
                    )
                f.write(f"{header}\n")
                
                # Часть 3: Формат файла
                f.write(f"{self.file_format}\n")
                
                # Часть 4: Описание сетки
                self._write_dataset(f)
                
            print(f"✓ Файл успешно записан: {path}")
            self._print_write_info(path)
            
        except IOError as e:
            raise IOError(f"Ошибка при записи файла {filepath}: {e}")
    
    def _write_dataset(self, f) -> None:
        """
        Записывает описание сетки в формате DATASET STRUCTURED_POINTS.
        
        Args:
            f: Открытый файл для записи
        """
        dims = self.grid.get_dimensions()
        origin = self.grid.get_origin()
        spacing = self.grid.get_spacing()
        
        f.write("DATASET STRUCTURED_POINTS\n")
        f.write(f"DIMENSIONS {dims[0]} {dims[1]} {dims[2]}\n")
        f.write(f"ORIGIN {origin[0]} {origin[1]} {origin[2]}\n")
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
    
    Заготовка для будущей реализации бинарного формата.
    """
    
    def __init__(self, grid: StructuredOrthoGrid):
        """
        Инициализация Legacy BINARY писателя.
        
        Args:
            grid: Структурированная ортогональная сетка
        """
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
