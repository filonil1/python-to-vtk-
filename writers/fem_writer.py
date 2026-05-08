"""
Писатель для формата препроцессора FEM (Zset/Zebulo формат).
Генерирует .txt файлы для задач механики деформируемого твердого тела.
"""
from pathlib import Path
from typing import List, Tuple


class FemPreprocessorWriter:
    """
    Генератор входных файлов для FEM-препроцессора.

    Формат включает:
    - Блок /prep: геометрия, сетка, материалы, граничные условия
    - Блок /proc: настройки решателя
    - Блок /post: настройки постпроцессинга
    """

    def __init__(self, grid):
        """
        Инициализация писателя.

        Args:
            grid: Объект сетки StructuredOrthoGrid
        """
        self.grid = grid

    def write(self, filepath: str) -> None:
        """
        Записывает файл в формате FEM препроцессора.

        Args:
            filepath: Путь к выходному файлу
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        points = self.grid.get_all_points()
        cells = self.grid.get_hexahedron_connectivity()
        num_nodes = len(points)
        num_elements = len(cells)

        # Индексы узлов нижней и верхней граней для граничных условий
        nz = self.grid.get_dimensions()[2]
        nx = self.grid.get_dimensions()[0]
        ny = self.grid.get_dimensions()[1]

        bottom_nodes = []  # Узлы где Z = min (закреплены)
        top_nodes = []     # Узлы где Z = max (нагружены)

        bottm_nodes_x= [] # Узлы где x= min (x)
        top_nodes_x = []     # Узлы где x = max ()
        bottm_nodes_y=[]
        top_nodes_y=[]

        for idx, point in enumerate(points):

            if abs(point[2] - self.grid.get_origin()[2]) < 1e-9:
                bottom_nodes.append(idx)
            if abs(point[2] - (self.grid.get_origin()[2] + self.grid.length_z)) < 1e-9:
                top_nodes.append(idx)
            if abs(point[0]-self.grid.get_origin()[0])<1e-9:
                bottm_nodes_x.append(idx)
            if abs(point[0] - (self.grid.get_origin()[0] + self.grid.length_x)) < 1e-9:
                top_nodes_x.append(idx)
            if abs(point[1]-self.grid.get_origin()[1])<1e-9:
                bottm_nodes_y.append(idx)
            if abs(point[1] - (self.grid.get_origin()[1] + self.grid.length_y)) < 1e-9:
                top_nodes_y.append(idx)
        
       
        set_x_min = set(bottm_nodes_x)
        set_x_max = set(top_nodes_x)
        set_y_min = set(bottm_nodes_y)
        set_y_max = set(top_nodes_y)
        
        corners = []
        davka_1 = [] # Периметр (границы)
        davka_2 = [] # Центр (внутренность)

        for node_id in top_nodes:
            # Проверяем, есть ли данный номер узла (node_id) в множествах границ
            on_x_bound = (node_id in set_x_min) or (node_id in set_x_max)
            on_y_bound = (node_id in set_y_min) or (node_id in set_y_max)
            if on_x_bound and on_y_bound:
                corners.append(node_id)
            elif on_x_bound or on_y_bound:
                davka_1.append(node_id) # Узел на краю верхней грани
                
            else:
                davka_2.append(node_id) # Узел внутри верхней грани



        
        with open(path, 'w') as f:
            # ========== БЛОК /PREP ==========
            f.write("/prep\n")
            f.write("SETT OMP 1\n")

            # Количество узлов (комментарий)
            f.write(f"!{num_nodes}\n")

            # Координаты узлов
         
            for i, (x, y, z) in enumerate(points):
                f.write(f"NC {i} {x:.6f} {y:.6f} {z:.6f}\n")
            f.write("@+ node coordinates\n")
            f.write("\n")

            # Элементы
            f.write(f"! {num_elements}\n")
            f.write("ME 0 HEX83\n")
            f.write(f"ETR 0 {num_elements} 0\n")
            f.write(f"EOR 0 {num_elements} 1 1 ! middle rectangle method\n")
            f.write(f"EOR 0 {num_elements} 2 1 ! weighted integration\n")
            f.write("@+ integration options\n")
            f.write("\n")

            # Список элементов
            for i, cell in enumerate(cells):
                # cell = [8, n0, n1, n2, n3, n4, n5, n6, n7]
                nodes_str = " ".join(map(str, cell[1:]))
                f.write(f"EN {i}  {nodes_str}\n")
            f.write("@+ element nodes\n")
            f.write("\n")

            # Материалы
            f.write("MP 0 EM 3 1e-6 1e-6 30000\n")
            f.write("MP 0 PR 3 0.2 0.2 0.2\n")
            f.write(f"EMR 0 {num_elements} 0\n")
            f.write("@+ material parameters\n")
            f.write("\n")

            # База данных (CT scan параметры)
            f.write("DB 0 CT PATH path/to/image/\n")
            f.write("DB 0 CT NAME rough_cropped.raw\n")
            f.write("DB 0 CT TYPE ui8\n")
            f.write("DB 0 CT CARD 447 448 897\n")
            f.write("DB 0 CT ORIG 0.0 0.0 0.0\n")
            f.write("DB 0 CT SIZE 0.06669 0.06669 0.06669\n")
            f.write("DB 1 IA MINQ 30\n")
            f.write(f"EDR 0 {num_elements} 2 0 1\n")
            f.write("@+ scan parameters\n")
            f.write("\n")

            # Граничные условия (DL)
            # Нижняя грань: UZ = 0 (закрепление)
            for node_id in bottom_nodes:
                f.write(f"DL {node_id} UX 0\n")
            f.write("\n")
            for node_id in bottom_nodes:
                f.write(f"DL {node_id} UY 0\n")
            f.write("\n")
            for node_id in bottom_nodes:
                f.write(f"DL {node_id} UZ 0\n")
            f.write("\n")
            for node_id in corners:
                f.write(f"DL {node_id} UZ +1\n")
            
    
        
            # Верхняя грань: UZ = +1 (нагрузка)
            for node_id in davka_1:
                f.write(f"DL {node_id} UZ +2\n")
            f.write("\n")
           
            for node_id in davka_2:
                f.write(f"DL {node_id} UZ +4\n")
            f.write("\n")
            f.write(f'''REE 0.05 @+ no empty elements\n''')

            # Фильтр пустых элементов
            f.write(f"! {num_elements}\n")
            f.write("\n")

            f.write("finish @+ /prep finish\n")

            # ========== БЛОК /PROC ==========
            f.write("/proc\n")
            f.write("\n")
            f.write("SETT OMP 1\n")
            f.write("\n")
            f.write("CGSM @+ global stiffness matrix\n")
            f.write("CGFV @+ global force vector\n")
            f.write("OGSM @+ global stiffness matrix (overrode)\n")
            f.write("CGDV @+ global displacement vector\n")
            f.write("CLNS @+ local nodal state\n")
            f.write("ALVS @+ local volumetric state\n")
            f.write("\n")
            f.write("finish @+ /proc finish\n")

            # ========== БЛОК /POST ==========
            f.write("/post\n")
            f.write("\n")
            f.write("SETT ADD 0\n")
            f.write("SETT VTK 0\n")
            f.write("WVTK ParaView.vtk @+ vtk: HEADER\n")
            f.write("SETT ADD 1\n")
            f.write("SETT VTK 1\n")
            f.write("WVTK ParaView.vtk @+ vtk: POINTS\n")
            f.write("SETT VTK 2\n")
            f.write("WVTK ParaView.vtk @+ vtk: CELLS\n")
            f.write("SETT VTK 3\n")
            f.write("WVTK ParaView.vtk @+ vtk: CELL_TYPES\n")
            f.write("SETT VTK 4\n")
            f.write("WVTK ParaView.vtk @+ vtk: POINT_DATA\n")
            f.write("SETT VTK 5\n")
            f.write("WVTK ParaView.vtk @+ vtk: DISPLACEMENTS\n")
            f.write("!SETT VTK 6\n")
            f.write("!WVTK ParaView.vtk @+ vtk: NODAL_STATE\n")
            f.write("SETT VTK 7\n")
            f.write("WVTK ParaView.vtk @+ vtk: CELL_DATA\n")
            f.write("SETT VTK 8\n")
            f.write("WVTK ParaView.vtk @+ vtk: VOLUMETRIC_STATE\n")
            f.write("\n")
            f.write("finish @+ /post finish\n")
            f.write("end\n")

        print(f"✓ FEM файл успешно записан: {path}")
        print(f"  Узлов: {num_nodes}")
        print(f"  Элементов: {num_elements}")
        print(f"  Закреплено узлов (UZ=0): {len(bottom_nodes)}")
        print(f"  Нагружено узлов (UZ=+1): {len(top_nodes)}")