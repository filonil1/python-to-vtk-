from .base_writer import BaseVTKWriter


class LegacyASCIITXTWriter(BaseVTKWriter):
    """Писатель для txt gerasimov."""
    
    VTK_VERSION = "2.0"
    
    def __init__(self, grid):
        super().__init__(grid, file_format="ASCII")
    
    def write(self, filepath: str) -> None:
        path = self._validate_filepath(filepath)
        
        try:
            with open(path, 'w') as f:
                # 1. Заголовок
                
          
                
                # 2. DATASET POLYDATA
                f.write("/prep\n")
                f.write("/SETT OMP 1\n")

                f.write('!7936\n')
                
                # 3. POINTS
                points = self.grid.get_all_points()
                f.write(f"NC {len(points)} float\n")
                max_z = max([p[2] for p in points])
                min_z = min([p[2] for p in points])
                max_mass=[]
                mix_mass=[]



                for i, p in enumerate(points):
                    f.write(f"NC {i} {p[0]} {p[1]} {p[2]}\n")
                    if max_z==p[2]: max_mass.append(i)
                    if min_z==p[2]: mix_mass.append(i)  



                
                f.write("@+ node coordinates")

               # 4. CELLS (Гексаэдры) - ИСПОЛЬЗУЕМ get_hexahedron_connectivity
                cells = self.grid.get_hexahedron_connectivity()
                num_cells = len(cells)
                list_size = sum(len(c) for c in cells)

                s = f"""
                
! {num_cells+1} 
ME 0 HEX83 
ETR 0 {num_cells} 0 
EOR 0 {num_cells} 1 1 ! middle rectangle method 
EOR 0 {num_cells} 2 1 ! weighted integration 
@+ integration options 
\r
"""
                f.write(s)
                
                for i, cell in enumerate(cells):
                    line = " ".join(map(str, cell))
                    f.write(f"EN {i} {line}\n")
                f.write("@+ element nodes")

                s = f"""
                
MP 0 EM 3 1e-6 1e-6 30000
MP 0 PR 3 0.2 0.2 0.2
EMR 0 6749 0
@+ material parameters

DB 0 CT PATH path/to/image/
DB 0 CT NAME rough_cropped.raw
DB 0 CT TYPE ui8
DB 0 CT CARD 447 448 897
DB 0 CT ORIG 0.0 0.0 0.0
DB 0 CT SIZE 0.06669 0.06669 0.06669
DB 1 IA MINQ 30
EDR 0 6749 2 0 1
@+ scan parameters

\r
"""
                f.write(s)
                for i in mix_mass:
                    f.write(f"DL {i} UZ 0 \n")
                f.write(f" \n")
                for i in max_mass:
                    f.write(f"DL {i} UZ +1 \n")
                f.write(f" \n")

                s = f"""
                
! {num_cells+1} 

finish @+ /prep finish
/proc

SETT OMP 1

CGSM @+ global stiffness matrix
CGFV @+ global force vector
OGSM @+ global stiffness matrix (overrode)
CGDV @+ global displacement vector
CLNS @+ local nodal state
ALVS @+ local volumetric state

finish @+ /proc finish
/post

SETT ADD 0
SETT VTK 0
WVTK ParaView.vtk @+ vtk: HEADER
SETT ADD 1
SETT VTK 1
WVTK ParaView.vtk @+ vtk: POINTS
SETT VTK 2
WVTK ParaView.vtk @+ vtk: CELLS
SETT VTK 3
WVTK ParaView.vtk @+ vtk: CELL_TYPES
SETT VTK 4
WVTK ParaView.vtk @+ vtk: POINT_DATA
SETT VTK 5
WVTK ParaView.vtk @+ vtk: DISPLACEMENTS
!SETT VTK 6
!WVTK ParaView.vtk @+ vtk: NODAL_STATE
SETT VTK 7
WVTK ParaView.vtk @+ vtk: CELL_DATA
SETT VTK 8
WVTK ParaView.vtk @+ vtk: VOLUMETRIC_STATE

finish @+ /post finish
end 
\r
"""
                f.write(s)

                    


                print(f"✓ Файл успешно записан: {path}")
                print(f"  Точек: {len(points)}")
                print(f"  Объемных ячеек (гексаэдров): {num_cells}")
            
        except IOError as e:
            raise IOError(f"Ошибка при записи файла {filepath}: {e}")


class LegacyBINARYVTKWriter(BaseVTKWriter):
    def write(self, filepath: str) -> None:
        raise NotImplementedError("BINARY формат не реализован.")
