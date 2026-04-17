#!/usr/bin/env python3
"""Главный скрипт VTK Generator.

Профессиональный инструмент для создания VTK файлов с регулярными
ортогональными сетками в Legacy ASCII формате.
"""

import argparse
import sys
from pathlib import Path

# Добавляем родительскую директорию в path для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))

from vtk_generator.core import StructuredOrthoGrid
from vtk_generator.writers import LegacyASCIIVTKWriter


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки.
    
    Returns:
        Namespace с аргументами
    """
    parser = argparse.ArgumentParser(
        description="VTK Generator - Генератор VTK файлов с регулярными ортогональными сетками",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s --length-x 10 --length-y 10 --length-z 10 --divisions-x 5 --divisions-y 5 --divisions-z 5
  %(prog)s -lx 20 -ly 15 -lz 30 -dx 10 -dy 7 -dz 15 --origin 0 0 0 --output my_grid.vtk
  %(prog)s --demo
        """
    )
    
    # Параметры размеров
    size_group = parser.add_argument_group("Размеры сетки")
    size_group.add_argument(
        "--length-x", "-lx",
        type=float,
        required=False,
        help="Размер сетки по оси X"
    )
    size_group.add_argument(
        "--length-y", "-ly",
        type=float,
        required=False,
        help="Размер сетки по оси Y"
    )
    size_group.add_argument(
        "--length-z", "-lz",
        type=float,
        required=False,
        help="Размер сетки по оси Z"
    )
    
    # Параметры разбиений
    div_group = parser.add_argument_group("Количество разбиений")
    div_group.add_argument(
        "--divisions-x", "-dx",
        type=int,
        required=False,
        help="Количество интервалов (ячеек) по оси X"
    )
    div_group.add_argument(
        "--divisions-y", "-dy",
        type=int,
        required=False,
        help="Количество интервалов (ячеек) по оси Y"
    )
    div_group.add_argument(
        "--divisions-z", "-dz",
        type=int,
        required=False,
        help="Количество интервалов (ячеек) по оси Z"
    )
    
    # Дополнительные параметры
    parser.add_argument(
        "--origin",
        type=float,
        nargs=3,
        default=[0.0, 0.0, 0.0],
        metavar=("X", "Y", "Z"),
        help="Координаты начальной точки сетки (по умолчанию: 0 0 0)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output.vtk",
        help="Путь к выходному файлу (по умолчанию: output.vtk)"
    )
    parser.add_argument(
        "--name", "-n",
        type=str,
        default="grid",
        help="Название сетки (по умолчанию: grid)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Вывод подробной информации"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Запустить демонстрационный режим"
    )
    
    return parser.parse_args()


def run_demo() -> None:
    """Запускает демонстрационный режим."""
    print("=" * 60)
    print("VTK Generator - Демонстрационный режим")
    print("=" * 60)
    
    # Создаем демонстрационную сетку
    print("\n1. Создание сетки 10x10x10 с 5 разбиениями по каждой оси...")
    grid = StructuredOrthoGrid(
        length_x=10.0,
        length_y=10.0,
        length_z=10.0,
        divisions_x=5,
        divisions_y=5,
        divisions_z=5,
        origin=(0.0, 0.0, 0.0),
        name="demo_grid"
    )
    
    # Выводим информацию о сетке
    print(f"\n2. Информация о сетке:")
    print(f"   {grid}")
    
    info = grid.get_grid_info()
    print(f"\n3. Детальная информация:")
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    # Показываем примеры координат
    print(f"\n4. Примеры координат точек:")
    print(f"   Точка [0,0,0]: {grid.get_point_coordinates(0, 0, 0)}")
    print(f"   Точка [2,2,2]: {grid.get_point_coordinates(2, 2, 2)}")
    print(f"   Точка [5,5,5]: {grid.get_point_coordinates(5, 5, 5)}")
    
    # Записываем в файл
    print(f"\n5. Запись в VTK файл...")
    writer = LegacyASCIIVTKWriter(grid)
    writer.write("demo_output.vtk")
    
    # Показываем содержимое файла
    print(f"\n6. Содержимое созданного файла:")
    print("-" * 40)
    with open("demo_output.vtk", 'r') as f:
        print(f.read())
    print("-" * 40)
    
    print("\n✓ Демонстрация завершена успешно!")
    print("=" * 60)


def main() -> int:
    """Главная функция.
    
    Returns:
        Код возврата (0 - успех, 1 - ошибка)
    """
    args = parse_args()
    
    # Демонстрационный режим
    if args.demo:
        run_demo()
        return 0
    
    # Проверка обязательных параметров
    required_params = [
        args.length_x, args.length_y, args.length_z,
        args.divisions_x, args.divisions_y, args.divisions_z
    ]
    
    if any(param is None for param in required_params):
        print("Ошибка: Необходимо указать все параметры размеров и разбиений.")
        print("Используйте --help для получения справки.")
        print("\nИли запустите демонстрационный режим: python main.py --demo")
        return 1
    
    try:
        # Создаем сетку
        if args.verbose:
            print(f"Создание сетки '{args.name}'...")
        
        grid = StructuredOrthoGrid(
            length_x=args.length_x,
            length_y=args.length_y,
            length_z=args.length_z,
            divisions_x=args.divisions_x,
            divisions_y=args.divisions_y,
            divisions_z=args.divisions_z,
            origin=tuple(args.origin),
            name=args.name
        )
        
        if args.verbose:
            print(f"\nИнформация о сетке:")
            print(f"  {grid}")
            info = grid.get_grid_info()
            print(f"  Размеры: {info['dimensions']}")
            print(f"  Количество точек: {info['number_of_points']}")
            print(f"  Количество ячеек: {info['number_of_cells']}")
            print(f"  Границы: {info['bounds']}")
            print(f"  Шаги: {info['spacing']}")
        
        # Записываем в файл
        if args.verbose:
            print(f"\nЗапись в файл: {args.output}")
        
        writer = LegacyASCIIVTKWriter(grid)
        writer.write(args.output)
        
        if args.verbose:
            print("\n✓ Генерация завершена успешно!")
        
        return 0
        
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        return 1
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
