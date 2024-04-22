import io
import os
import requests
from PIL import Image, ImageDraw, ImageFont

data = {
  "texts": [
    "La mente no es una vasija que hay que llenar, sino un fuego que hay que encender.",
    "La ciencia es organizada conocimiento. La sabiduría es organizada vida.",
    "La paz no es la ausencia de conflicto, sino la capacidad de lidiar con él.",
    "El hombre no es nada más que lo que la educación hace de él.",
    "La libertad es la autonomía de la razón.",
    "Obras o muérete.",
    "Actúa de tal modo que puedas querer que la máxima de tu acción se convierta en una ley universal.",
    "La felicidad no es algo que se adquiere, sino algo que se experimenta.",
    "La ignorancia es la madre de la admiración.",
    "No hagas a los demás lo que no quieras que te hagan a ti.",
    "El conocimiento viene, pero la sabiduría tarda.",
    "No se debe vivir para comer, sino comer para vivir.",
    "El que no conoce nada, no ama nada. El que no puede hacer nada, no comprende nada. El que nada comprende, nada vale. Pero el que comprende también ama, observa, ve...",
    "La paz perpetua no es un sueño, sino un ideal que merece esfuerzo.",
    "El hombre es el único animal que necesita ser educado.",
    "La teología es la ciencia de las creencias, no la ciencia de Dios.",
    "Es necesario sostener la moral por las razones que la dan nacimiento; el sentimiento seguirá después.",
    "Es mejor sufrir la injusticia que cometerla.",
    "El hombre es el único animal que necesita ser educado.",
    "La filosofía no es una teoría sino una actitud.",
    "No podemos hacer verdadera justicia sino cuando sentimos compasión.",
    "Saber consiste en ver.",
    "El ser humano es la única criatura que se niega a ser lo que es.",
    "La mente humana se desliza irremediablemente hacia el conocimiento.",
    "La fe sin la razón es ciega, pero la razón sin la fe es vacía.",
    "No estamos en condiciones de juzgar lo que el mundo nos presenta. Nosotros sólo podemos interpretar lo que nos aparece.",
    "La estrella más pequeña ilumina en la más oscura noche.",
    "Nada es tan opuesto a la justicia y a la equidad como el derecho positivo.",
    "La experiencia sin teoría es ciega, pero la teoría sin experiencia es mera especulación.",
    "La metafísica es la ciencia de lo indeterminado."
  ],
  "output_filename": "name",
  "interline_spacing": 2.5,
  "margin": 600,
  "font_url": 'https://raw.githubusercontent.com/google/fonts/main/ufl/ubuntu/Ubuntu-Regular.ttf'
}

def download_font(font_url):
    """Descarga la fuente desde una URL y devuelve un objeto BytesIO."""
    response = requests.get(font_url)
    response.raise_for_status()
    return io.BytesIO(response.content)

def wrap_text(font, text, max_width):
    """Divide el texto en líneas según el ancho máximo y devuelve una lista de líneas."""
    # Divide el texto en palabras
    words = text.split()
    # Inicializa las variables para almacenar las líneas y la línea actual
    lines = []
    line = []
    line_width = 0

    # Itera sobre cada palabra
    for word in words:
        # Obtiene la máscara de la palabra para calcular su ancho
        word_mask = font.getmask(word)
        word_width = word_mask.size[0]
        # Si la palabra cabe en la línea actual, agrégala a la línea y actualiza su ancho
        if line_width + word_width <= max_width:
            line.append(word)
            line_width += word_width + font.getmask(' ').size[0]
        # Si la palabra no cabe en la línea actual, agrega la línea actual a la lista de líneas,
        # inicializa una nueva línea con la palabra actual y actualiza su ancho
        else:
            lines.append(' '.join(line))
            line = [word]
            line_width = word_width

    # Agrega la última línea a la lista de líneas
    lines.append(' '.join(line))
    return lines

def create_text_image(text, output_filename, font_url, bg_color=(255, 255, 255), text_color=(0, 0, 0), font_size=100, interline_spacing=2.5, margin=100):
    # Descargar la fuente y crear un objeto ImageFont
    font_data = download_font(font_url)
    font = ImageFont.truetype(font_data, font_size)

    # Calcular las dimensiones del texto y dividirlo en líneas
    max_width = 3000 - 2 * margin  # Ancho máximo de la imagen (resta los márgenes)
    lines = wrap_text(font, text, max_width)
    num_lines = len(lines)

    # Calcular las dimensiones de la imagen cuadrada
    line_height = font.getmask('A').size[1]
    text_height = line_height * num_lines * interline_spacing
    image_size = max(max_width + 2 * margin, int(text_height) + 2 * margin)

    # Crear una nueva imagen cuadrada
    image = Image.new('RGB', (image_size, image_size), bg_color)

    # Dibujar el texto centrado en la imagen
    draw = ImageDraw.Draw(image)
    line_offset = (interline_spacing - 1) * line_height / 2
    y_start = (image_size - text_height) // 2
    for i, line in enumerate(lines):
        line_mask = font.getmask(line)
        text_width, _ = line_mask.size
        x = margin + (max_width - text_width) // 2
        y = y_start + i * line_height * interline_spacing + line_offset
        draw.text((x, y), line, font=font, fill=text_color)

    os.makedirs("images", exist_ok=True)
    # Guardar la imagen en el disco
    image.save(f"images/{output_filename}", optimize=True, quality=95)

if __name__ == '__main__':
    for i, text in enumerate(data["texts"]):
        create_text_image(text, f"{data['output_filename']}_{str(i)}.png", font_url=data["font_url"], bg_color=(255, 255, 255), text_color=(0, 0, 0), font_size=100, interline_spacing=2.5, margin=100)
