#!/usr/bin/env python3
"""
VTK Generator - Главный скрипт для создания VTK файлов.

Профессиональный инструмент для создания VTK файлов с регулярными
ортогональными сетками в Legacy ASCII формате.

Примеры использования:
    python main.py --length-x 10 --length-y 10 --length-z 10 \\
                   --divisions-x 5 --divisions-y 5 --divisions-z 5

    python main.py --demo
"""

import argparse
import sys
from pathlib import Path

# Добавляем корень проекта в путь импорта
sys.path.insert(0, str(Path(__file__).parent))

from core import StructuredOrthoGrid
from writers import LegacyASCIIVTKWriter


def parse_args():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Генератор VTK файлов с регулярными ортогональными сетками",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s -lx 10 -ly 10 -lz 10 -dx 5 -dy 5 -dz 5
  %(prog)s --length-x 20 --length-y 15 --length-z 30 --divisions-x 10 --divisions-y 7 --divisions-z 15 --output grid.vtk
  %(prog)s --demo
        """
    )

    # Параметры размеров
    parser.add_argument(
        '-lx', '--length-x', type=float, required=False,
        help='Размер сетки по оси X'
    )
    parser.add_argument(
        '-ly', '--length-y', type=float, required=False,
        help='Размер сетки по оси Y'
    )
    parser.add_argument(
        '-lz', '--length-z', type=float, required=False,
        help='Размер сетки по оси Z'
    )

    # Параметры разбиений
    parser.add_argument(
        '-dx', '--divisions-x', type=int, required=False,
        help='Количество разбиений по оси X'
    )
    parser.add_argument(
        '-dy', '--divisions-y', type=int, required=False,
        help='Количество разбиений по оси Y'
    )
    parser.add_argument(
        '-dz', '--divisions-z', type=int, required=False,
        help='Количество разбиений по оси Z'
    )

    # Дополнительные параметры
    parser.add_argument(
        '-o', '--origin', nargs=3, type=float, default=[0.0, 0.0, 0.0],
        metavar=('X', 'Y', 'Z'),
        help='Начальная точка сетки (по умолчанию: 0 0 0)'
    )
    parser.add_argument(
        '-n', '--name', type=str, default='grid',
        help='Название сетки (по умолчанию: grid)'
    )
    parser.add_argument(
        '-O', '--output', type=str, default='output.vtk',
        help='Имя выходного файла (по умолчанию: output.vtk)'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Вывод подробной информации'
    )
    parser.add_argument(
        '--demo', action='store_true',
        help='Запустить демонстрационный режим'
    )

    return parser.parse_args()


def run_demo():
    """Запускает демонстрационный режим."""
    print("=" * 60)
    print("VTK Generator - Демонстрационный режим")
    print("=" * 60)

    # Создаем демонстрационную сетку
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

    print("\n" + str(grid))
    print("\nИнформация о сетке:")
    info = grid.get_grid_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    # Записываем в файл
    writer = LegacyASCIIVTKWriter(grid)
    output_file = "demo_output.vtk"
    writer.write(output_file)

    # Показываем содержимое файла
    print(f"\nСодержимое файла {output_file}:")
    print("-" * 40)
    with open(output_file, 'r') as f:
        print(f.read())

    print("=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


def main():
    """Основная функция."""
    args = parse_args()

    # Демонстрационный режим
    if args.demo:
        run_demo()
        return

    # Проверка обязательных параметров
    required_params = [
        args.length_x, args.length_y, args.length_z,
        args.divisions_x, args.divisions_y, args.divisions_z
    ]

    if any(param is None for param in required_params):
        print("Ошибка: Необходимо указать размеры и разбиения сетки.")
        print("Используйте --help для получения справки или --demo для демонстрации.")
        sys.exit(1)

    # Создаем сетку
    try:
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
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        sys.exit(1)

    # Выводим информацию о сетке
    if args.verbose:
        print(str(grid))
        print()

    # Записываем в файл
    writer = LegacyASCIIVTKWriter(grid)
    try:
        writer.write(args.output)
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()