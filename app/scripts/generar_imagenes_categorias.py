from PIL import Image, ImageDraw, ImageFont
import os

# Categorías y colores de fondo
categorias = [
    ("futbol", (46, 204, 113)),
    ("baloncesto", (230, 126, 34)),
    ("tenis", (52, 152, 219)),
    ("natacion", (41, 128, 185)),
    ("ciclismo", (241, 196, 15)),
    ("camping", (39, 174, 96)),
    ("fitness", (155, 89, 182)),
    ("accesorios", (127, 140, 141)),
]

output_dir = os.path.join(os.path.dirname(__file__), "..", "static", "img", "categorias")
os.makedirs(output_dir, exist_ok=True)

for nombre, color in categorias:
    img = Image.new("RGB", (300, 300), color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except OSError:
        font = ImageFont.load_default()
    text = nombre.capitalize()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((300-w)/2, (300-h)/2), text, fill="white", font=font)
    img.save(os.path.join(output_dir, f"{nombre}.jpg"), "JPEG")
print("Imágenes de ejemplo generadas.")
