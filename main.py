#!/usr/bin/env python3
"""
Главный скрипт VTK/FEM Generator.
Генерирует сетки в формате VTK (для ParaView) или FEM Preprocessor (для Zset/Zebulo).
"""

import argparse
import sys
from pathlib import Path

# Импорты из пакетов
from core import StructuredOrthoGrid
from writers import LegacyASCIIVTKWriter, FemPreprocessorWriter


def parse_args():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Генератор регулярных ортогональных сеток (VTK / FEM)"
    )
    
    # Параметры сетки
    parser.add_argument("-lx", "--length-x", type=float, required=True, help="Размер по X")
    parser.add_argument("-ly", "--length-y", type=float, required=True, help="Размер по Y")
    parser.add_argument("-lz", "--length-z", type=float, required=True, help="Размер по Z")
    parser.add_argument("-dx", "--divisions-x", type=int, required=True, help="Разбиения по X")
    parser.add_argument("-dy", "--divisions-y", type=int, required=True, help="Разбиения по Y")
    parser.add_argument("-dz", "--divisions-z", type=int, required=True, help="Разбиения по Z")
    
    # Дополнительные параметры
    parser.add_argument("--origin", type=float, nargs=3, default=[0.0, 0.0, 0.0], help="Начало координат (x y z)")
    parser.add_argument("-n", "--name", type=str, default="grid", help="Название сетки")
    parser.add_argument("-o", "--output", type=str, default="output.vtk", help="Имя выходного файла")
    parser.add_argument("-v", "--verbose", action="store_true", help="Подробный вывод")
    parser.add_argument("--demo", action="store_true", help="Запуск демонстрационного режима")
    
    return parser.parse_args()


def run_demo():
    """Демонстрационный режим."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИОННЫЙ РЕЖИМ")
    print("=" * 60)
    
    grid = StructuredOrthoGrid(
        length_x=10.0, length_y=10.0, length_z=10.0,
        divisions_x=2, divisions_y=2, divisions_z=2,
        origin=(0.0, 0.0, 0.0),
        name="demo_grid"
    )
    
    if args.verbose:
        print(grid)
    
    # Генерация VTK
    writer_vtk = LegacyASCIIVTKWriter(grid)
    writer_vtk.write("demo_output.vtk")
    
    # Генерация FEM
    writer_fem = FemPreprocessorWriter(grid)
    writer_fem.write("demo_preprocessor.txt")
    
    print("Демонстрация завершена! Созданы файлы: demo_output.vtk, demo_preprocessor.txt")


def main():
    """Основная функция."""
    global args
    args = parse_args()
    
    if args.demo:
        run_demo()
        return

    # Создание сетки
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
        print(f"❌ Ошибка валидации: {e}")
        sys.exit(1)

    if args.verbose:
        print(grid)

    # Определение типа файла по расширению
    output_path = Path(args.output)
    extension = output_path.suffix.lower()

    try:
        if extension == ".vtk":
            # Генерация VTK файла
            writer = LegacyASCIIVTKWriter(grid)
            writer.write(args.output)
            
        elif extension in [".txt", ".dat", ".inp", ".zmat"]:
            # Генерация FEM препроцессора
            writer = FemPreprocessorWriter(grid)
            writer.write(args.output)
            
        else:
            print(f"⚠️ Неизвестное расширение '{extension}'. По умолчанию генерируется VTK.")
            writer = LegacyASCIIVTKWriter(grid)
            writer.write(args.output)
            
    except Exception as e:
        print(f"\n❌ Ошибка при записи файла: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()