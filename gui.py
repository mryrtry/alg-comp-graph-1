"""
Модуль графического интерфейса приложения.
Содержит все виджеты и управление интерфейсом.
"""

import tkinter as tk
from tkinter import ttk
import threading


class MainApplication:
    """
    Главный класс приложения, управляющий интерфейсом.

    Attributes:
        root (tk.Tk): Главное окно приложения
        image_manager (ImageManager): Менеджер изображений
        histogram_manager (HistogramManager): Менеджер гистограмм
    """

    def __init__(self, root, image_manager, histogram_manager):
        """
        Инициализация главного приложения.

        Args:
            root (tk.Tk): Главное окно
            image_manager (ImageManager): Менеджер изображений
            histogram_manager (HistogramManager): Менеджер гистограмм
        """
        self.root = root
        self.image_manager = image_manager
        self.histogram_manager = histogram_manager

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        """Настраивает пользовательский интерфейс."""
        # Устанавливаем стиль ttk
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10))

        # Главный контейнер
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Настраиваем веса строк и столбцов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=0)

        # Создаем области для изображения и гистограммы
        self.create_image_section(main_container)
        self.create_histogram_section(main_container)
        self.create_control_buttons(main_container)

    def create_image_section(self, parent):
        """
        Создает секцию для отображения изображения.

        Args:
            parent (ttk.Frame): Родительский фрейм
        """
        # Фрейм для изображения
        image_frame = ttk.LabelFrame(parent, text="Изображение", padding="5")
        image_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        image_frame.columnconfigure(0, weight=1)
        image_frame.rowconfigure(0, weight=1)

        # Холст для отображения изображения
        self.image_canvas = tk.Canvas(
            image_frame,
            bg='white',
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.image_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Метка для информации об изображении
        self.image_info_label = ttk.Label(image_frame, text="Загрузка...", background='#f0f0f0')
        self.image_info_label.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def create_histogram_section(self, parent):
        """
        Создает секцию для отображения гистограммы.

        Args:
            parent (ttk.Frame): Родительский фрейм
        """
        # Фрейм для гистограммы
        histogram_frame = ttk.LabelFrame(parent, text="Гистограмма RGB", padding="5")
        histogram_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        histogram_frame.columnconfigure(0, weight=1)
        histogram_frame.rowconfigure(0, weight=1)

        # Контейнер для гистограммы (будет заполнен позже)
        self.histogram_container = ttk.Frame(histogram_frame)
        self.histogram_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.histogram_container.columnconfigure(0, weight=1)
        self.histogram_container.rowconfigure(0, weight=1)

    def create_control_buttons(self, parent):
        """
        Создает панель управления с кнопками.

        Args:
            parent (ttk.Frame): Родительский фрейм
        """
        # Фрейм для кнопок
        button_frame = ttk.Frame(parent, padding="5")
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        # Кнопка "Сменить изображение"
        self.next_image_btn = ttk.Button(
            button_frame,
            text="Сменить изображение",
            command=self.switch_image
        )
        self.next_image_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Кнопка "Загрузить своё"
        self.load_image_btn = ttk.Button(
            button_frame,
            text="Загрузить своё изображение",
            command=self.load_custom_image
        )
        self.load_image_btn.pack(side=tk.LEFT)

        # Кнопка "Обновить"
        self.refresh_btn = ttk.Button(
            button_frame,
            text="Обновить отображение",
            command=self.update_display
        )
        self.refresh_btn.pack(side=tk.RIGHT)

    def switch_image(self):
        """
        Обрабатывает нажатие кнопки смены изображения.
        """

        def switch_thread():
            self.next_image_btn.config(state='disabled')
            if self.image_manager.switch_to_next_image():
                self.update_display()
            self.next_image_btn.config(state='normal')

        # Запускаем в отдельном потоке чтобы не блокировать интерфейс
        threading.Thread(target=switch_thread, daemon=True).start()

    def load_custom_image(self):
        """
        Обрабатывает нажатие кнопки загрузки пользовательского изображения.
        """

        def load_thread():
            self.load_image_btn.config(state='disabled')
            if self.image_manager.load_custom_image():
                self.update_display()
            self.load_image_btn.config(state='normal')

        # Запускаем в отдельном потоке чтобы не блокировать интерфейс
        threading.Thread(target=load_thread, daemon=True).start()

    def update_display(self):
        """
        Обновляет отображение изображения и гистограммы.
        """
        # Получаем размеры холста для масштабирования
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()

        # Если холст еще не отрисован, используем стандартные размеры
        if canvas_width < 10:
            canvas_width = 400
            canvas_height = 300

        # Масштабируем и отображаем изображение
        photo_image = self.image_manager.get_scaled_image(canvas_width - 10, canvas_height - 10)

        if photo_image:
            # Очищаем холст
            self.image_canvas.delete("all")

            # Отображаем изображение по центру
            x = canvas_width // 2
            y = canvas_height // 2
            self.image_canvas.create_image(x, y, image=photo_image)

            # Обновляем информацию об изображении
            image = self.image_manager.current_image
            if image:
                width, height = image.size
                self.image_info_label.config(
                    text=f"Размер: {width}×{height} пикселей | Формат: {image.format or 'N/A'}"
                )

        # Обновляем гистограмму
        image_data = self.image_manager.get_image_data()
        if image_data:
            self.histogram_manager.update_histogram(self.histogram_container, image_data)
            histogram_canvas = self.histogram_manager.canvas
            if histogram_canvas:
                histogram_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Планируем следующее обновление для корректного масштабирования
        self.root.after(100, self.finalize_display)

    def finalize_display(self):
        """
        Завершающее обновление отображения после полной отрисовки интерфейса.
        """
        # Повторно обновляем для корректного масштабирования
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()

        if canvas_width > 10 and canvas_height > 10:
            photo_image = self.image_manager.get_scaled_image(canvas_width - 10, canvas_height - 10)
            if photo_image:
                self.image_canvas.delete("all")
                x = canvas_width // 2
                y = canvas_height // 2
                self.image_canvas.create_image(x, y, image=photo_image)