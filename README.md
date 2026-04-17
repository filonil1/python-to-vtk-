# VTK Generator - Генератор VTK файлов

Профессиональный инструмент для создания VTK файлов с регулярными ортогональными сетками в Legacy ASCII формате.

## 📋 Структура проекта

```
vtk_generator/
├── main.py                          # Главный скрипт
├── core/
│   ├── __init__.py                 # Инициализация пакета
│   ├── base_grid.py                # Абстрактный базовый класс для сеток
│   └── structured_grid.py          # Класс для структурированной сетки
├── writers/
│   ├── __init__.py                 # Инициализация пакета
│   ├── base_writer.py              # Абстрактный базовый класс для писателей
│   └── legacy_ascii_writer.py      # Реализация Legacy ASCII формата
└── README.md                        # Этот файл
```

## 🎯 Ключевые особенности

- **Объектно-ориентированный дизайн** с использованием наследования
- **Модульная архитектура** - легко добавлять новые форматы
- **Полная валидация** входных данных
- **Подробное логирование** и информационные сообщения
- **Legacy ASCII VTK формат** - совместимость с VTK 2.0+
- **Структурированная сетка** типа STRUCTURED_POINTS

## 🏗️ Архитектура

### Иерархия классов

```
BaseGrid (абстрактный)
  └── StructuredOrthoGrid (конкретная реализация)

BaseVTKWriter (абстрактный)
  └── LegacyASCIIVTKWriter (конкретная реализация)
```

### Основные классы

#### `StructuredOrthoGrid`
Представляет регулярную ортогональную сетку в 3D пространстве.

**Параметры:**
- `length_x, length_y, length_z` - размеры сетки по осям
- `divisions_x, divisions_y, divisions_z` - количество интервалов по каждой оси
- `origin` - координаты начальной точки сетки
- `name` - название сетки

**Методы:**
- `get_dimensions()` - возвращает (nx, ny, nz) - количество точек
- `get_spacing()` - возвращает (dx, dy, dz) - шаги сетки
- `get_number_of_points()` - общее количество точек
- `get_number_of_cells()` - общее количество ячеек
- `get_point_coordinates(i, j, k)` - координаты точки по индексам
- `get_all_points()` - список всех координат точек
- `get_grid_info()` - полная информация о сетке

#### `LegacyASCIIVTKWriter`
Записывает сетку в VTK Legacy ASCII формате.

**Методы:**
- `write(filepath)` - записывает файл

## 📖 Примеры использования

### Использование через командную строку

#### Простой пример
```bash
python vtk_generator/main.py --length-x 10 --length-y 10 --length-z 10 \
               --divisions-x 5 --divisions-y 5 --divisions-z 5
```

#### С дополнительными параметрами
```bash
python vtk_generator/main.py --length-x 20 --length-y 15 --length-z 30 \
               --divisions-x 10 --divisions-y 7 --divisions-z 15 \
               --origin 0 0 0 \
               --output my_grid.vtk \
               --name "My Custom Grid" \
               --verbose
```

#### Демонстрация
```bash
python vtk_generator/main.py --demo
```

### Использование API (в коде Python)

#### Простой пример
```python
from vtk_generator.core import StructuredOrthoGrid
from vtk_generator.writers import LegacyASCIIVTKWriter

# Создаем сетку 10x10x10 с 5 разбиениями по каждой оси
grid = StructuredOrthoGrid(
    length_x=10.0,
    length_y=10.0,
    length_z=10.0,
    divisions_x=5,
    divisions_y=5,
    divisions_z=5,
    origin=(0.0, 0.0, 0.0),
    name="my_grid"
)

# Выводим информацию о сетке
print(grid)
print("\nИнформация о сетке:")
info = grid.get_grid_info()
for key, value in info.items():
    print(f"  {key}: {value}")

# Записываем в VTK файл
writer = LegacyASCIIVTKWriter(grid)
writer.write("output.vtk")
```

#### Получение координат точек
```python
from vtk_generator.core import StructuredOrthoGrid

grid = StructuredOrthoGrid(10, 10, 10, 2, 2, 2)

# Координаты конкретной точки
coords = grid.get_point_coordinates(1, 1, 1)
print(f"Точка [1,1,1]: {coords}")  # (5.0, 5.0, 5.0)

# Все координаты
all_points = grid.get_all_points()
for i, point in enumerate(all_points):
    print(f"Точка {i}: {point}")
```

#### Получение информации о сетке
```python
from vtk_generator.core import StructuredOrthoGrid

grid = StructuredOrthoGrid(20, 15, 30, 10, 7, 15)

dims = grid.get_dimensions()          # (11, 8, 16)
points = grid.get_number_of_points()  # 1408
cells = grid.get_number_of_cells()    # 1050
bounds = grid.get_bounds()            # (0.0, 20.0, 0.0, 15.0, 0.0, 30.0)
spacing = grid.get_spacing()          # (2.0, ~2.14, 2.0)
```

## 🔄 Рабочий процесс

```
┌─────────────────────────────────────────────────────────┐
│  Пользователь вводит параметры (a, b, c, na, nb, nc)  │
└──────────────────────┬──────────────────────────────────┘
                       ▼
        ┌──────────────────────────────┐
        │  StructuredOrthoGrid         │
        │  - Создание сетки            │
        │  - Валидация параметров      │
        │  - Вычисление координат      │
        └──────────────┬───────────────┘
                       ▼
        ┌──────────────────────────────┐
        │  LegacyASCIIVTKWriter        │
        │  - Форматирование данных     │
        │  - Запись в файл             │
        └──────────────┬───────────────┘
                       ▼
        ┌──────────────────────────────┐
        │  output.vtk (VTK файл)       │
        │  - Legacy ASCII формат       │
        │  - STRUCTURED_POINTS тип     │
        └──────────────────────────────┘
```

## 📊 Формат VTK файла

Созданный VTK файл имеет следующую структуру:

```
# vtk DataFile Version 2.0
VTK file generated by VTK Generator (grid: my_grid)
ASCII
DATASET STRUCTURED_POINTS
DIMENSIONS 6 6 6
ORIGIN 0.0 0.0 0.0
SPACING 2.0 2.0 2.0
```

Где:
- **DIMENSIONS** - количество точек по каждой оси (nx, ny, nz)
- **ORIGIN** - координаты начальной точки (x0, y0, z0)
- **SPACING** - интервалы между соседними точками (dx, dy, dz)

## ✨ Преимущества использования наследования

1. **Легко расширять** - добавление нового формата требует только создания нового класса
2. **Код переиспользуется** - базовые методы в родительских классах
3. **Полиморфизм** - можно использовать различные писатели с одной сеткой
4. **Чистота кода** - разделение ответственности между классами
5. **Тестируемость** - каждый класс отвечает за одно

## 🚀 Примеры запуска

### Пример 1: Маленькая сетка
```bash
python vtk_generator/main.py -lx 5 -ly 5 -lz 5 -dx 2 -dy 2 -dz 2 -o small.vtk
```

### Пример 2: Большая неравномерная сетка
```bash
python vtk_generator/main.py --length-x 100 --length-y 50 --length-z 75 \
               --divisions-x 50 --divisions-y 25 --divisions-z 30 \
               --output large_grid.vtk --verbose
```

### Пример 3: Сетка с смещением от начала координат
```bash
python vtk_generator/main.py --length-x 10 --length-y 10 --length-z 10 \
               --divisions-x 5 --divisions-y 5 --divisions-z 5 \
               --origin 10 20 30 \
               --output offset_grid.vtk
```

## 🧪 Тестирование

Для проверки корректности генерируемых файлов:

1. **Визуализация в ParaView:**
   ```bash
   paraview output.vtk
   ```

2. **Проверка структуры файла:**
   ```bash
   head -20 output.vtk
   ```

3. **Проверка в Python:**
   ```python
   from vtk_generator.core import StructuredOrthoGrid
   grid = StructuredOrthoGrid(10, 10, 10, 5, 5, 5)
   assert grid.get_number_of_points() == 6*6*6
   assert grid.get_number_of_cells() == 5*5*5
   ```

## 📝 Валидация параметров

Программа проверяет:
- ✓ Размеры сетки должны быть положительными
- ✓ Количество разбиений должно быть положительным
- ✓ Заголовок не превышает 256 символов
- ✓ Тип сетки соответствует писателю
- ✓ Выходная директория создается автоматически

## 🔗 Соотношение между параметрами

```
Входные параметры (задает пользователь):
  - a, b, c       (размеры по X, Y, Z)
  - na, nb, nc    (количество разбиений)

Вычисляемые параметры:
  - nx = na + 1   (количество точек по X)
  - ny = nb + 1   (количество точек по Y)
  - nz = nc + 1   (количество точек по Z)
  
  - dx = a / na   (шаг по X)
  - dy = b / nb   (шаг по Y)
  - dz = c / nc   (шаг по Z)

Итоговые параметры:
  - Всего точек: nx * ny * nz
  - Всего ячеек: na * nb * nc
```

## 📦 Требования

- Python 3.6+
- Только встроенные модули (pathlib, abc, argparse)

## 📄 Лицензия

Открытый проект для образовательных целей.

## 👥 Автор

Создано как пример объектно-ориентированного программирования на Python с использованием наследования и модульной архитектуры.
