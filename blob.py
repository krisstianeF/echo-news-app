from PIL import Image, ImageDraw
import io
import base64
import sqlite3


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


'''def crop_image(input_path, output_path, width, height):
    # Открываем изображение
    image = Image.open(input_path)

    # Получаем текущие размеры изображения
    current_width, current_height = image.size

    # Вычисляем координаты для обрезки
    left = (current_width - width) / 2
    top = (current_height - height) / 2
    right = (current_width + width) / 2
    bottom = (current_height + height) / 2

    # Обрезка изображения
    cropped_image = image.crop((left, top, right, bottom))

    # Создаем маску с закругленными углами
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=255)

    # Применяем маску к изображению
    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    result.paste(cropped_image, (0, 0), mask)

    # Сохраняем обрезанное изображение
    cropped_image.save(output_path)'''

def crop_image(input_path, output_path, width, height, radius):
    # Открываем изображение
    image = Image.open(input_path)

    # Получаем текущие размеры изображения
    current_width, current_height = image.size

    # Вычисляем координаты для обрезки
    left = (current_width - width) / 2
    top = (current_height - height) / 2
    right = (current_width + width) / 2
    bottom = (current_height + height) / 2

    # Обрезка изображения
    cropped_image = image.crop((left, top, right, bottom))

    # Создаем маску с закругленными углами
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=255)

    # Применяем маску к изображению
    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    result.paste(cropped_image, (0, 0), mask)

    # Сохраняем измененное изображение
    result.save(output_path)

sqlite_connection = sqlite3.connect('echo_database.db')
cursor = sqlite_connection.cursor()

select = f"""SELECT image FROM article WHERE articleID = 1;"""
cursor.execute(select)
image = cursor.fetchone()
blob_image = image[0]
png_data = blob_to_png(blob_image)

with open('article_image.png', 'wb') as f:
    f.write(png_data)