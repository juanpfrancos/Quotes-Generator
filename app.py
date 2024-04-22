import json
import random
import os
from PIL import Image, ImageDraw, ImageFont
from colorsys import hls_to_rgb
import requests
import io
from datetime import datetime

texts = ["Primer texto para la imagen",
        "Segundo texto para la imagen",
        "Tercer texto para la imagen",
        "Cuarto texto para la imagen"]



def download_font(font_name, font_weight):
    font_url = f"https://fonts.googleapis.com/css2?family={font_name}:wght@{font_weight}&display=swap"
    response = requests.get(font_url)
    font_src = response.content.decode("utf-8").split("@font-face")[1].split("src:")[1].split(";")[0].replace("url(", "").replace(")", "").strip()

    # Extraer el ID de la fuente
    font_id = font_src.split("/")[-1].split(".")[0]

    # Construir la URL para descargar la fuente en formato TTF
    ttf_url = f"https://fonts.gstatic.com/s/roboto/{font_id}/{font_id}_{font_weight}.ttf"

    font_data = requests.get(ttf_url).content

    # Guardar fuente temporalmente
    temp_font_file = "temp_font.ttf"
    with open(temp_font_file, "wb") as f:
        f.write(font_data)

    # Cargar fuente desde el archivo temporal
    try:
        font = ImageFont.truetype(temp_font_file, 96)
    except OSError:
        # Utilizar una fuente predeterminada de Pillow como respaldo
        font = ImageFont.load_default()

    # Eliminar el archivo temporal después de cargar la fuente
    os.remove(temp_font_file)

    return font

def generate_image(text, font_name, font_weight, margin_percent=0.1):
    width = 1080
    height = 1080

    # Colores pastel aleatorios
    hue = random.uniform(0, 1)
    lightness = random.uniform(0.8, 1)
    saturation = random.uniform(0.2, 0.4)
    rgb = hls_to_rgb(hue, lightness, saturation)
    color1 = tuple(int(round(c * 255)) for c in rgb)
    color2 = tuple(int(round(c * 255 * 0.9)) for c in rgb)

    # Crear imagen
    image = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(image)

    # Obtener fuente
    font = download_font(font_name, font_weight)

    # Calcular ancho y alto del texto con margen interno
    margin = int(min(width, height) * margin_percent)
    text_width, text_height = font.getsize(text)
    max_width = width - 2 * margin
    max_height = height - 2 * margin

    # Ajustar tamaño de fuente si es necesario
    while text_width > max_width or text_height > max_height:
        font = ImageFont.truetype(font.font_file, font.size - 1)
        text_width, text_height = font.getsize(text)

    # Dibujar texto centrado
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0, 255))

    # Aplicar degradado
    gradient = Image.new("L", (width, height), color=0)
    draw = ImageDraw.Draw(gradient)
    for y in range(height):
        interpolated_color = int((y / height) * (color2[0] - color1[0]) + color1[0])
        draw.line([(0, y), (width, y)], fill=interpolated_color)
    image.putalpha(gradient)

    return image

for i, text in enumerate(texts):
    image = generate_image(text, "Roboto", font_weight=700)
    directory = str(datetime.now())
    os.makedirs(directory, exist_ok=True)

    # Guardar la imagen en el directorio
    image.save(f"{directory}/image_{i}.png", optimize=True, quality=95)
