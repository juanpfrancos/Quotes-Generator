import random
import os
from PIL import Image, ImageDraw, ImageFont
from colorsys import hls_to_rgb
import requests
from datetime import datetime

texts = [
    "Elige no estar molesto, y no te molestarás.",
    "La felicidad yace en la virtud, y no en los placeres materiales.",
    "No busques que las cosas sucedan como deseas, sino desea que las cosas sucedan como suceden, y serás feliz.",
    "No son las cosas en sí mismas las que nos perturban, sino nuestras interpretaciones de ellas.",
    "Lo que nos hace sufrir no es lo que nos pasa, sino lo que pensamos acerca de lo que nos pasa.",
    "No dejes que tu felicidad dependa de algo que puedas perder.",
    "Acepta todo lo que te sucede con ecuanimidad y serenidad.",
    "Vive cada día como si fuera el último, pero planifica cada día como si fueras a vivir para siempre.",
    "No lamentes el pasado ni temas el futuro, concentra tu mente en el presente.",
    "El sabio se contenta con lo que le toca sin desear lo que no le toca.",
    "El sufrimiento es el entrenamiento del carácter; el destino es el maestro del alma.",
    "La virtud es la única buena; el vicio es la única maldad.",
    "La adversidad es un espejo en el que la virtud se refleja con mayor claridad.",
    "No busques ser rico, busca ser feliz. La riqueza está en el alma, no en la cuenta bancaria.",
    "La muerte no es temida por aquellos que han aprendido a vivir sabiamente.",
    "No busques cambiar el mundo, cámbiate a ti mismo.",
    "No esperes que los demás actúen según tus deseos, actúa tú mismo según tus principios.",
    "Aprende a soportar con dignidad lo que no puedes evitar cambiar.",
    "La libertad suprema es ser dueño de uno mismo.",
    "Elige siempre la virtud sobre el placer, la paz interior sobre la agitación externa.",
]



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
        font = ImageFont.truetype(temp_font_file, 700)
    except OSError:
        # Utilizar una fuente predeterminada de Pillow como respaldo
        font = ImageFont.load_default()

    # Eliminar el archivo temporal después de cargar la fuente
    os.remove(temp_font_file)

    return font

def generate_image(text, font_name, font_weight, margin_percent=0.005):
    width = 500
    height = 500

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
    max_width = width - 2 * margin
    max_height = height - 2 * margin

    # Dividir el texto en líneas según su longitud
    lines = []
    line = ""
    for word in text.split():
        test_line = line + word + " "
        test_mask = font.getmask(test_line)
        test_width, test_height = test_mask.size
        if test_width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    # Calcular altura total del texto
    total_text_height = sum(font.getmask(line).size[1] for line in lines)

    # Calcular posición inicial de las líneas para centrar verticalmente el texto
    y_offset = (height - total_text_height) // 2

    # Dibujar texto centrado
    for line in lines:
        mask = font.getmask(line)
        text_width, text_height = mask.size
        x = (width - text_width) // 2
        draw.text((x, y_offset), line, font=font, fill=(0, 0, 0, 255))
        y_offset += text_height + 10  # Ajusta el valor "10" según sea necesario

    # Aplicar degradado
    gradient = Image.new("L", (width, height), color=0)
    draw = ImageDraw.Draw(gradient)
    for y in range(height):
        interpolated_color = int((y / height) * (color2[0] - color1[0]) + color1[0])
        draw.line([(0, y), (width, y)], fill=interpolated_color)
    image.putalpha(gradient)

    return image


directory = str(datetime.now())

for i, text in enumerate(texts):
    image = generate_image(text, "Roboto", font_weight=700)
    os.makedirs(directory, exist_ok=True)
    # Guardar la imagen en el directorio
    image.save(f"{directory}/image_{i}.png", optimize=True, quality=95)
