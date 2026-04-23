"""
Реализация писателя для VTK Legacy ASCII формата (POLYDATA).
"""
from .base_writer import BaseVTKWriter


class LegacyASCIIVTKWriter(BaseVTKWriter):
    """Писатель для VTK Legacy ASCII формата (POLYDATA)."""
    
    VTK_VERSION = "2.0"
    
    def __init__(self, grid):
        super().__init__(grid, file_format="ASCII")
    
    def write(self, filepath: str) -> None:
        path = self._validate_filepath(filepath)
        
        try:
            with open(path, 'w') as f:
                # 1. Заголовок
                f.write(f"# vtk DataFile Version {self.VTK_VERSION}\n")
                f.write(f"{self._get_header()}\n")
                f.write(f"{self.file_format}\n")
                
                # 2. DATASET POLYDATA
                f.write("DATASET POLYDATA\n")
                
                # 3. POINTS
                points = self.grid.get_all_points()
                f.write(f"POINTS {len(points)} float\n")
                for x, y, z in points:
                    f.write(f"{x} {y} {z}\n")
                
                # 4. POLYGONS (Грани)
                polygons = self.grid.get_polygons_connectivity()
                num_polys = len(polygons)
                # Размер данных: кол-во полигонов + сумма всех вершин (у каждого 4 вершины + 1 число размера)
                total_size = sum(len(p) for p in polygons)
                
                f.write(f"POLYGONS {num_polys} {total_size}\n")
                for poly in polygons:
                    # poly выглядит как [4, v0, v1, v2, v3]
                    line = " ".join(map(str, poly))
                    f.write(f"{line}\n")
                
                # 5. CELL_DATA (Данные для граней)
                # Чтобы кубы были видны, дадим им цвет (скаляр)
                f.write(f"\nCELL_DATA {num_polys}\n")
                f.write("SCALARS CellId int 1\n")
                f.write("LOOKUP_TABLE default\n")
                for i in range(num_polys):
                    f.write(f"{i}\n")
                
            print(f"✓ Файл успешно записан: {path}")
            print(f"  Точек: {len(points)}")
            print(f"  Граней (полигонов): {num_polys}")
            
        except IOError as e:
            raise IOError(f"Ошибка при записи файла {filepath}: {e}")


class LegacyBINARYVTKWriter(BaseVTKWriter):
    """Заглушка для бинарного формата."""
    def write(self, filepath: str) -> None:
        raise NotImplementedError("BINARY формат не реализован.")