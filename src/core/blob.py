from PIL import Image, ImageDraw
import io
import base64
from concurrent.futures import ThreadPoolExecutor
import os

def convert_to_binary(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def blob_to_png(blob_data):
    if blob_data != None:
        # Декодируем BLOB данные из base64, если они закодированы
        if isinstance(blob_data, str):
            blob_data = base64.b64decode(blob_data)

        # Создаем объект BytesIO из BLOB данных
        blob_io = io.BytesIO(blob_data)

        # Открываем изображение с помощью Pillow
        image = Image.open(blob_io)

        # Создаем объект BytesIO для сохранения PNG
        png_io = io.BytesIO()

        # Сохраняем изображение в формате PNG
        image.save(png_io, format='PNG')

        # Получаем байтовые данные PNG
        png_data = png_io.getvalue()

        with open('article_image.png', 'wb') as f:
            f.write(png_data)
    else:
        png_data = None

    return png_data

def crop_image(input_path, output_path, width, height, radius):
    # Открываем изображение
    image = Image.open(input_path)

    # Получаем текущие размеры изображения
    current_width, current_height = image.size

    # Вычисляем новые размеры, сохраняя пропорции
    aspect_ratio = min(width / current_width, height / current_height)
    new_width = int(current_width * aspect_ratio)
    new_height = int(current_height * aspect_ratio)

    # Изменяем размер изображения, сохраняя пропорции
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Вычисляем координаты для обрезки
    left = (new_width - width) / 2
    top = (new_height - height) / 2
    right = (new_width + width) / 2
    bottom = (new_height + height) / 2

    # Обрезка изображения
    cropped_image = resized_image.crop((left, top, right, bottom))

    # Создаем маску с закругленными углами
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=255)

    # Применяем маску к изображению
    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    result.paste(cropped_image, (0, 0), mask)

    # Сохраняем измененное изображение
    result.save(output_path, quality=10)
