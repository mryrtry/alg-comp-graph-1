"""
Модуль для управления изображениями.
Отвечает за загрузку, переключение и масштабирование изображений.
"""

import os
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox


class ImageManager:
    """
    Класс для управления изображениями приложения.

    Attributes:
        current_image_index (int): Индекс текущего изображения в карусели
        image_paths (list): Список путей к предустановленным изображениям
        current_image (PIL.Image): Текущее загруженное изображение
        current_photo_image (ImageTk.PhotoImage): Изображение для отображения в Tkinter
    """

    def __init__(self):
        """Инициализация менеджера изображений."""
        self.current_image_index = 0
        self.image_paths = self._get_default_images()
        self.current_image = None
        self.current_photo_image = None

        # Загружаем первое изображение по умолчанию
        if self.image_paths:
            self.load_image(self.image_paths[0])

    @staticmethod
    def _get_default_images():
        """
        Получает список путей к изображениям по умолчанию.

        Returns:
            list: Список путей к изображениям в папке images
        """
        # Создаем папку images если её нет
        if not os.path.exists("images"):
            os.makedirs("images")

        # Ищем изображения в папке
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        image_paths = []

        for file in os.listdir("images"):
            if file.lower().endswith(image_extensions):
                image_paths.append(os.path.join("images", file))

        # Если изображений нет, создаем сообщение
        if not image_paths:
            print("В папке 'images' не найдено изображений. Добавьте изображения для работы приложения.")

        return image_paths

    def load_image(self, image_path):
        """
        Загружает изображение из указанного пути.

        Args:
            image_path (str): Путь к файлу изображения

        Returns:
            bool: Успешно ли загружено изображение
        """
        try:
            self.current_image = Image.open(image_path)
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")
            return False

    def get_scaled_image(self, max_width, max_height):
        """
        Масштабирует изображение для отображения с сохранением пропорций.

        Args:
            max_width (int): Максимальная ширина области отображения
            max_height (int): Максимальная высота области отображения

        Returns:
            ImageTk.PhotoImage: Масштабированное изображение для Tkinter
        """
        if self.current_image is None:
            return None

        # Вычисляем новые размеры с сохранением пропорций
        original_width, original_height = self.current_image.size
        ratio = min(max_width / original_width, max_height / original_height)

        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        # Масштабируем изображение
        scaled_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.current_photo_image = ImageTk.PhotoImage(scaled_image)

        return self.current_photo_image

    def switch_to_next_image(self):
        """
        Переключает на следующее изображение в карусели.

        Returns:
            bool: Успешно ли переключено изображение
        """
        if not self.image_paths:
            messagebox.showwarning("Предупреждение", "Нет доступных изображений в папке 'images'")
            return False

        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        return self.load_image(self.image_paths[self.current_image_index])

    def load_custom_image(self):
        """
        Загружает пользовательское изображение через диалог выбора файла.

        Returns:
            bool: Успешно ли загружено изображение
        """
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Все файлы", "*.*")
            ]
        )

        if file_path:
            return self.load_image(file_path)
        return False

    def get_image_data(self):
        """
        Возвращает данные текущего изображения для анализа.

        Returns:
            PIL.Image: Текущее изображение или None если изображение не загружено
        """
        return self.current_image