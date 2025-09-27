"""
Модуль для расчета гистограммы RGB и создания графиков.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class HistogramManager:
    """
    Класс для управления гистограммами RGB.

    Attributes:
        figure (matplotlib.figure.Figure): Фигура для построения гистограммы
        canvas (FigureCanvasTkAgg): Холст для отображения гистограммы в Tkinter
    """

    def __init__(self):
        """Инициализация менеджера гистограмм."""
        self.figure = None
        self.canvas = None

    @staticmethod
    def calculate_rgb_histogram(image):
        """
        Вычисляет гистограмму RGB для изображения.

        Args:
            image (PIL.Image): Изображение для анализа

        Returns:
            tuple: Кортеж с данными гистограммы (r_data, g_data, b_data, total_pixels)
        """
        if image is None:
            return None, None, None, 0

        # Конвертируем изображение в numpy array
        img_array = np.array(image)

        # Если изображение в градациях серого, конвертируем в RGB
        if len(img_array.shape) == 2:
            img_array = np.stack([img_array] * 3, axis=-1)

        # Разделяем каналы
        if img_array.shape[2] == 4:  # Если есть альфа-канал
            r_channel = img_array[:, :, 0]
            g_channel = img_array[:, :, 1]
            b_channel = img_array[:, :, 2]
        else:  # RGB
            r_channel = img_array[:, :, 0]
            g_channel = img_array[:, :, 1]
            b_channel = img_array[:, :, 2]

        # Вычисляем количество пикселей каждого канала
        total_pixels = r_channel.size

        r_pixels = np.sum(r_channel > 128)
        g_pixels = np.sum(g_channel > 128)
        b_pixels = np.sum(b_channel > 128)

        return r_pixels, g_pixels, b_pixels, total_pixels

    def create_histogram(self, parent_frame, r_data, g_data, b_data, total_pixels):
        """
        Создает гистограмму RGB в указанном фрейме.

        Args:
            parent_frame (tk.Frame): Родительский фрейм для гистограммы
            r_data (int): Количество пикселей красного канала
            g_data (int): Количество пикселей зеленого канала
            b_data (int): Количество пикселей синего канала
            total_pixels (int): Общее количество пикселей

        Returns:
            FigureCanvasTkAgg: Холст с гистограммой
        """
        # Очищаем предыдущую гистограмму
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Создаем новую фигуру
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = self.figure.add_subplot(111)

        # Подготавливаем данные для гистограммы
        channels = ['Red', 'Green', 'Blue']
        values = [r_data, g_data, b_data]

        # Рассчитываем проценты
        percentages = [val / total_pixels * 100 if total_pixels > 0 else 0 for val in values]

        # Создаем столбчатую диаграмму
        bars = ax.bar(channels, percentages, color=['red', 'green', 'blue'], alpha=0.7)

        # Настраиваем внешний вид
        ax.set_title('Гистограмма RGB каналов', fontsize=14, fontweight='bold')
        ax.set_ylabel('Процент пикселей (%)', fontsize=10)
        ax.set_ylim(0, 100)

        # Добавляем значения на столбцы
        for bar, percentage, value in zip(bars, percentages, values):
            height = bar.get_height()
            if height < 10:
                y_pos = height + 2
                color = 'black'
                va = 'bottom'
            else:
                y_pos = height / 2
                color = 'white'
                va = 'center'

            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                y_pos,
                f'{percentage:.1f}%\n({value})',
                ha='center',
                va=va,
                fontsize=9,
                color=color,
                fontweight='bold'
            )

        # Добавляем сетку для лучшей читаемости
        ax.grid(True, alpha=0.3, axis='y')

        # Создаем холст для Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, parent_frame)
        self.canvas.draw()

        return self.canvas

    def update_histogram(self, parent_frame, image):
        """
        Обновляет гистограмму на основе текущего изображения.

        Args:
            parent_frame (tk.Frame): Родительский фрейм для гистограммы
            image (PIL.Image): Изображение для анализа

        Returns:
            FigureCanvasTkAgg: Обновленный холст с гистограммой
        """
        r_data, g_data, b_data, total_pixels = self.calculate_rgb_histogram(image)
        return self.create_histogram(parent_frame, r_data, g_data, b_data, total_pixels)