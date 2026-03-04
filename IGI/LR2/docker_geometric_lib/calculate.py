import os
import json
import sys
import argparse

# Добавляем путь к библиотеке, чтобы ее можно было импортировать
sys.path.append('/app')

# Импортируем наши функции
from geometric_lib.circle import area as circle_area, perimeter as circle_perimeter
from geometric_lib.square import area as square_area, perimeter as square_perimeter

def calculate_from_args(figure, value):
    """Расчет на основе аргументов командной строки."""
    if figure == 'circle':
        print(f"Круг: Радиус = {value}")
        print(f"  Площадь (S): {circle_area(value)}")
        print(f"  Периметр (P): {circle_perimeter(value)}")
    elif figure == 'square':
        print(f"Квадрат: Сторона = {value}")
        print(f"  Площадь (S): {square_area(value)}")
        print(f"  Периметр (P): {square_perimeter(value)}")
    else:
        print(f"Неизвестная фигура: {figure}")

def calculate_from_env():
    """Расчет на основе переменных окружения."""
    figure = os.getenv('FIGURE')
    try:
        value = float(os.getenv('VALUE'))
        calculate_from_args(figure, value)
    except (TypeError, ValueError):
        print("Ошибка: Не заданы или некорректны переменные окружения FIGURE и VALUE.")

def calculate_from_file(file_path):
    """Расчет на основе JSON-файла."""
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
        figure = config.get('figure')
        value = config.get('value')
        if figure and value:
            calculate_from_args(figure, float(value))
        else:
            print("Ошибка: В файле конфигурации отсутствуют поля 'figure' или 'value'.")
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
    except json.JSONDecodeError:
        print("Ошибка: Не удалось распарсить JSON файл.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Расчет геометрических параметров.')
    parser.add_argument('--figure', choices=['circle', 'square'], help='Тип фигуры (circle или square)')
    parser.add_argument('--value', type=float, help='Значение параметра (радиус или сторона)')
    parser.add_argument('--env', action='store_true', help='Использовать переменные окружения')
    parser.add_argument('--file', type=str, help='Путь к JSON файлу конфигурации')

    args = parser.parse_args()

    if args.env:
        calculate_from_env()
    elif args.file:
        calculate_from_file(args.file)
    elif args.figure and args.value:
        calculate_from_args(args.figure, args.value)
    else:
        print("Использование: python calculate.py --figure <circle|square> --value <число>")
        print("       или: python calculate.py --env")
        print("       или: python calculate.py --file <путь_к_файлу>")