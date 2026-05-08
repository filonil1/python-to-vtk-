"""
Писатели для различных форматов: VTK и FEM Preprocessor (.txt).
"""
from .base_writer import BaseVTKWriter
from pathlib import Path


class LegacyASCIIVTKWriter(BaseVTKWriter):
    """Записывает сетку в формате VTK Legacy ASCII (UNSTRUCTURED_GRID)."""
    
    VTK_VERSION = "2.0"
    
    def __init__(self, grid):
        super().__init__(grid, file_format="ASCII")
    
    def write(self, filepath: str) -> None:
        path = self._validate_filepath(filepath)
        try:
            with open(path, 'w') as f:
                f.write(f"# vtk DataFile Version {self.VTK_VERSION}\n")
                f.write(f"{self._get_header()}\n")
                f.write(f"{self.file_format}\n")
                f.write("DATASET UNSTRUCTURED_GRID\n")
                
                points = self.grid.get_all_points()
                f.write(f"POINTS {len(points)} float\n")
                for x, y, z in points:
                    f.write(f"{x:.6f} {y:.6f} {z:.6f}\n")
                
                cells = self.grid.get_hexahedron_connectivity()
                num_cells = len(cells)
                list_size = sum(len(c) for c in cells)
                
                f.write(f"CELLS {num_cells} {list_size}\n")
                for cell in cells:
                    f.write(" ".join(map(str, cell)) + "\n")
                
                f.write(f"CELL_TYPES {num_cells}\n")
                for _ in range(num_cells):
                    f.write("12\n")
                
                f.write(f"\nCELL_DATA {num_cells}\n")
                f.write("SCALARS CellId int 1\n")
                f.write("LOOKUP_TABLE default\n")
                for i in range(num_cells):
                    f.write(f"{i}\n")
                
            print(f"✓ VTK файл записан: {path}")
            print(f"  Точек: {len(points)}, Ячеек: {num_cells}")
        except IOError as e:
            raise IOError(f"Ошибка записи VTK: {e}")


class FemPreprocessorWriter:
    """
    Генерирует TXT файл для препроцессора МКЭ (формат Zset/Zebulo style).
    Формат включает настройки OMP, узлы, элементы HEX8, материалы и постпроцессинг.
    """
    
    def __init__(self, grid):
        self.grid = grid
    
    def write(self, filepath: str) -> None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Получаем данные
        points = self.grid.get_all_points()
        cells = self.grid.get_hexahedron_connectivity()
        
        num_nodes = len(points)
        num_elements = len(cells)
        
        # Размеры сетки для параметров материала (примерные)
        dx, dy, dz = self.grid.get_spacing()
        vol_elem = dx * dy * dz
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                # --- Блок /prep ---
                f.write("/prep\n")
                f.write("SETT OMP 1\n")
                f.write(f"! {num_nodes} количество узлов (NC = node coordinates)\n")
                f.write("! NC это point new cell\n")
                f.write("@+ node coordinates\n")
                
                # Координаты узлов (нумерация с 1 для совместимости с некоторыми солверами, 
                # но в примере ниже используем 0-based индексы для узлов внутри элементов, 
                # а список координат просто по порядку)
                # В формате Zset обычно: NodeID X Y Z
                for i, (x, y, z) in enumerate(points):
                    # Нумерация узлов часто начинается с 1 в таких файлах
                    f.write(f"{i+1} {x:.6f} {y:.6f} {z:.6f}\n")
                
                f.write("\n")
                f.write(f"! {num_elements} количество элементов (HEX8)\n")
                f.write("ME 0 HEX8 3\n") # HEX8, 3 степени свободы (UX, UY, UZ)
                f.write(f"ETR 0 {num_elements-1} 0\n") # Element Type Range
                
                # Параметры интеграции
                f.write(f"EOR 0 {num_elements-1} 0 1 ! middle rectangle method\n")
                f.write(f"EOR 0 {num_elements-1} 1 1 ! weighted integration\n")
                f.write("@+ integration options\n")
                f.write("EN this cell\n")
                f.write("\n@+ element nodes\n")
                
                # Список узлов для каждого элемента
                # В формате prep: ElementID Node1 Node2 ... Node8
                # Наши ячейки имеют формат [8, n0, n1, ..., n7], где индексы 0-based.
                # Добавим 1 к индексам узлов, если солвер требует 1-based нумерацию.
                for i, cell in enumerate(cells):
                    # cell[0] это 8, остальное индексы
                    nodes_indices = [str(n + 1) for n in cell[1:]] # Перевод в 1-based
                    f.write(f"{i+1} {' '.join(nodes_indices)}\n")
                
                f.write("\n@+ material parameters\n")
                # Параметры материала (Young's Modulus, Poisson, Density и т.д.)
                # MP <mat_id> <param_type> <dim> <values...>
                f.write("MP 0 EM 3 1e-6 1e-6 30000\n") # Модуль Юнга (пример)
                f.write("MP 0 PR 3 0.2 0.2 0.2\n")     # Коэфф. Пуассона
                f.write(f"EMR 0 {num_elements-1} 0\n") # Назначение материала элементам
                
                f.write("\n@+ scan parameters (Database)\n")
                # Пример подключения растрового изображения или данных
                f.write("DB 0 CT PATH path/to/image/data.base\n")
                f.write("DB 0 CT NAME rough_cropped.raw\n")
                f.write("DB 0 CT TYPE ui8\n")
                # Вычисляем кардинальность исходя из размеров сетки (примерно)
                nx, ny, nz = self.grid.get_dimensions()
                f.write(f"DB 0 CT CARD {nx} {ny} {nz}\n")
                origin = self.grid.get_origin()
                f.write(f"DB 0 CT ORIG {origin[0]:.1f} {origin[1]:.1f} {origin[2]:.1f}\n")
                spacing = self.grid.get_spacing()
                f.write(f"DB 0 CT SIZE {spacing[0]:.5f} {spacing[1]:.5f} {spacing[2]:.5f}\n")
                f.write("DB 1 IA MINQ 30\n")
                
                f.write(f"EDR 0 {num_elements-1} 2 0 1\n")
                
                f.write("\nDL ux uy uz 0\n") # Граничные условия (нет сил)
                f.write(f"REE 0.05\n")      # Фильтр пустых элементов
                f.write("finish\n")
                f.write("@+ /prep finish\n")
                
                # --- Блок /proc ---
                f.write("\n/proc\n")
                f.write("SETT OMP 1\n")
                f.write("CGSM\n") # Global Stiffness Matrix
                f.write("CGFV\n") # Global Force Vector
                f.write("OGSM\n") # Override GSM
                f.write("CGDV\n") # Global Displacement Vector
                f.write("CLNS\n") # Local Nodal State
                f.write("ALVS\n") # Local Volumetric State
                f.write("finish\n")
                f.write("@+ /proc finish\n")
                
                # --- Блок /post ---
                f.write("\n/post\n")
                f.write("SETT ADD 0\n")
                f.write("SETT VTK 0\n")
                f.write("WVTK ParaView.vtk\n")
                f.write("@+ vtk: HEADER\n")
                
                steps = [
                    (1, "POINTS"),
                    (2, "CELLS"),
                    (3, "CELL_TYPES"),
                    (4, "POINT_DATA"),
                    (5, "DISPLACEMENTS"),
                    (7, "CELL_DATA"),
                    (8, "VOLUMETRIC_STATE")
                ]
                
                for step, name in steps:
                    f.write(f"SETT ADD 1\n")
                    f.write(f"SETT VTK {step}\n")
                    f.write(f"WVTK ParaView.vtk\n")
                    f.write(f"@+ vtk: {name}\n")
                
                f.write("finish\n")
                f.write("@+ /post finish\n")
                f.write("end\n")
                
            print(f"✓ TXT файл препроцессора записан: {path}")
            print(f"  Узлов: {num_nodes}, Элементов: {num_elements}")
            
        except IOError as e:
            raise IOError(f"Ошибка записи TXT: {e}")


class LegacyBINARYVTKWriter(BaseVTKWriter):
    def write(self, filepath: str) -> None:
        raise NotImplementedError("BINARY формат не реализован.")
