import io
import os
import requests
from PIL import Image, ImageDraw, ImageFont

def download_font(font_url):
    """Descarga la fuente desde una URL y devuelve un objeto BytesIO."""
    response = requests.get(font_url)
    response.raise_for_status()
    return io.BytesIO(response.content)

def wrap_text(font, text, max_width):
    """Divide el texto en líneas según el ancho máximo y devuelve una lista de líneas."""
    words = text.split()
    lines = []
    line = []
    line_width = 0

    for word in words:
        word_mask = font.getmask(word)
        word_width = word_mask.size[0]
        if line_width + word_width <= max_width:
            line.append(word)
            line_width += word_width + font.getmask(' ').size[0]
        else:
            lines.append(' '.join(line))
            line = [word]
            line_width = word_width

    lines.append(' '.join(line))
    return lines


def create_text_image(text, output_filename, bg_color=(255, 255, 255), text_color=(0, 0, 0), font_url='https://raw.githubusercontent.com/google/fonts/main/ufl/ubuntu/Ubuntu-Regular.ttf', font_size=100, interline_spacing=2.5, margin=100):
    # Descargar la fuente y crear un objeto ImageFont
    font_data = download_font(font_url)
    font = ImageFont.truetype(font_data, font_size)

    # Calcular las dimensiones del texto y dividirlo en líneas
    max_width = 3000 - 2 * margin  # Ancho máximo de la imagen (resta los márgenes)
    lines = wrap_text(font, text, max_width)
    num_lines = len(lines)

    # Calcular las dimensiones de la imagen cuadrada
    line_height = font.getmask('A').size[1]
    image_size = max(max_width + 2 * margin, int(line_height * num_lines * interline_spacing) + 2 * margin)

    # Crear una nueva imagen cuadrada
    image = Image.new('RGB', (image_size, image_size), bg_color)

    # Dibujar el texto centrado en la imagen
    draw = ImageDraw.Draw(image)
    line_offset = (interline_spacing - 1) * line_height / 2
    text_height = line_height * num_lines * interline_spacing
    for i, line in enumerate(lines):
        line_mask = font.getmask(line)
        text_width, _ = line_mask.size
        x = margin + (max_width - text_width) // 2
        y = margin + (image_size - text_height) // 2 + i * line_height * interline_spacing + line_offset
        draw.text((x, y), line, font=font, fill=text_color)

    # Guardar la imagen en el disco
    image.save(output_filename)



if __name__ == '__main__':
    quote = "Esta es una frase cotidiana muy destacada. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl ut ultricies lacinia, nisl nisi aliquet nisl, eget aliquam nisl nisl eget nisl. Curabitur et nisl nulla. Sed aliquam porttitor tortor, ac ullamcorper lacus interdum at. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
    output_filename = "image_with_text.jpg"
    create_text_image(quote, output_filename, interline_spacing=2.5, margin=100)

