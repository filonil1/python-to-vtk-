#!/usr/bin/env python3
"""
VTK Generator - Программа для создания VTK файлов с регулярными ортогональными сетками.

Использование:
    python main.py --length-x 10 --length-y 10 --length-z 10 \
                   --divisions-x 5 --divisions-y 5 --divisions-z 5 \
                   --output output.vtk

Или использование API:
    from core import StructuredOrthoGrid
    from writers import LegacyASCIIVTKWriter
    
    grid = StructuredOrthoGrid(10, 10, 10, 5, 5, 5)
    writer = LegacyASCIIVTKWriter(grid)
    writer.write("output.vtk")
"""

import sys
import argparse
from pathlib import Path

from vtk_generator.core import StructuredOrthoGrid
from vtk_generator.writers import LegacyASCIIVTKWriter


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description='Генератор VTK файлов для регулярных ортогональных сеток',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  Простой пример:
    python main.py --length-x 10 --length-y 10 --length-z 10 \\
                   --divisions-x 5 --divisions-y 5 --divisions-z 5

  Полный пример:
    python main.py --length-x 20 --length-y 15 --length-z 30 \\
                   --divisions-x 10 --divisions-y 7 --divisions-z 15 \\
                   --origin 0 0 0 \\
                   --output my_grid.vtk \\
                   --name "My Custom Grid"
        """
    )
    
    # Обязательные параметры размеров
    parser.add_argument(
        '--length-x', '-lx',
        type=float,
        default=10.0,
        help='Размер сетки по оси X (по умолчанию: 10.0)'
    )
    parser.add_argument(
        '--length-y', '-ly',
        type=float,
        default=10.0,
        help='Размер сетки по оси Y (по умолчанию: 10.0)'
    )
    parser.add_argument(
        '--length-z', '-lz',
        type=float,
        default=10.0,
        help='Размер сетки по оси Z (по умолчанию: 10.0)'
    )
    
    # Параметры разбиения
    parser.add_argument(
        '--divisions-x', '-dx',
        type=int,
        default=5,
        help='Количество разбиений по оси X (по умолчанию: 5)'
    )
    parser.add_argument(
        '--divisions-y', '-dy',
        type=int,
        default=5,
        help='Количество разбиений по оси Y (по умолчанию: 5)'
    )
    parser.add_argument(
        '--divisions-z', '-dz',
        type=int,
        default=5,
        help='Количество разбиений по оси Z (по умолчанию: 5)'
    )
    
    # Начало координат
    parser.add_argument(
        '--origin',
        type=float,
        nargs=3,
        default=[0.0, 0.0, 0.0],
        metavar=('X', 'Y', 'Z'),
        help='Координаты начала сетки (по умолчанию: 0 0 0)'
    )
    
    # Параметры вывода
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output.vtk',
        help='Путь к выходному файлу (по умолчанию: output.vtk)'
    )
    
    parser.add_argument(
        '--name', '-n',
        type=str,
        default='structured_grid',
        help='Название сетки (по умолчанию: structured_grid)'
    )
    
    # Флаг для вывода информации
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Выводить подробную информацию'
    )
    
    # Флаг для примера
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Запустить демонстрацию с примерами'
    )
    
    return parser.parse_args()


def print_header():
    """Выводит заголовок программы."""
    print("\n" + "=" * 70)
    print("VTK GENERATOR - Генератор файлов VTK для ортогональных сеток".center(70))
    print("=" * 70 + "\n")


def create_and_write_grid(length_x, length_y, length_z, div_x, div_y, div_z,
                          origin, output_path, name, verbose=False):
    """
    Создает сетку и записывает ее в VTK файл.
    
    Args:
        length_x, length_y, length_z: Размеры сетки
        div_x, div_y, div_z: Количество разбиений
        origin: Координаты начала
        output_path: Путь для сохранения файла
        name: Название сетки
        verbose: Выводить ли подробную информацию
    """
    try:
        # Создаем сетку
        if verbose:
            print(f"Создание сетки с параметрами:")
            print(f"  Размеры: ({length_x}, {length_y}, {length_z})")
            print(f"  Разбиения: ({div_x}, {div_y}, {div_z})")
            print(f"  Начало: {origin}")
            print(f"  Название: '{name}'\n")
        
        grid = StructuredOrthoGrid(
            length_x=length_x,
            length_y=length_y,
            length_z=length_z,
            divisions_x=div_x,
            divisions_y=div_y,
            divisions_z=div_z,
            origin=tuple(origin),
            name=name
        )
        
        if verbose:
            print(grid)
            print()
        
        # Создаем писателя и записываем файл
        writer = LegacyASCIIVTKWriter(grid)
        writer.write(output_path)
        
        return True
        
    except Exception as e:
        print(f"✗ Ошибка: {e}", file=sys.stderr)
        return False


def run_demo():
    """Запускает демонстрацию с несколькими примерами."""
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ".center(70))
    print("=" * 70 + "\n")
    
    examples = [
        {
            'name': 'Маленькая сетка',
            'lx': 5, 'ly': 5, 'lz': 5,
            'dx': 2, 'dy': 2, 'dz': 2,
            'output': 'demo_small.vtk'
        },
        {
            'name': 'Средняя сетка',
            'lx': 20, 'ly': 20, 'lz': 20,
            'dx': 10, 'dy': 10, 'dz': 10,
            'output': 'demo_medium.vtk'
        },
        {
            'name': 'Неровная сетка',
            'lx': 30, 'ly': 20, 'lz': 10,
            'dx': 6, 'dy': 5, 'dz': 4,
            'output': 'demo_irregular.vtk'
        },
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"Пример {i}: {example['name']}")
        print("-" * 70)
        
        success = create_and_write_grid(
            example['lx'], example['ly'], example['lz'],
            example['dx'], example['dy'], example['dz'],
            (0, 0, 0),
            example['output'],
            example['name'],
            verbose=True
        )
        
        if not success:
            return False
    
    print("\n✓ Все примеры успешно выполнены!\n")
    return True


def main():
    """Главная функция программы."""
    args = parse_arguments()
    
    print_header()
    
    # Если флаг --demo, запускаем демонстрацию
    if args.demo:
        return run_demo()
    
    # Иначе создаем одну сетку с переданными параметрами
    success = create_and_write_grid(
        length_x=args.length_x,
        length_y=args.length_y,
        length_z=args.length_z,
        div_x=args.divisions_x,
        div_y=args.divisions_y,
        div_z=args.divisions_z,
        origin=args.origin,
        output_path=args.output,
        name=args.name,
        verbose=args.verbose
    )
    
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)