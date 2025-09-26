"""
Основной модуль приложения.
Создает главное окно и связывает все компоненты приложения.
"""

import tkinter as tk
from gui import MainApplication
from image_manager import ImageManager
from histogram import HistogramManager


def main():
    """
    Точка входа в приложение.
    Инициализирует главное окно и запускает основной цикл.
    """
    # Создание главного окна
    root = tk.Tk()
    root.title("Анализатор изображений с гистограммой RGB")
    root.geometry("1000x700")
    root.resizable(False, False)
    root.minsize(800, 600)

    # Создание менеджеров
    image_manager = ImageManager()
    histogram_manager = HistogramManager()

    # Создание главного приложения
    MainApplication(root, image_manager, histogram_manager)

    # Запуск основного цикла
    root.mainloop()


if __name__ == "__main__":
    main()