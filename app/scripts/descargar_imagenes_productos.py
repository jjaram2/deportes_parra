import os
import requests

# Diccionario de productos y URLs de imágenes libres de derechos (ejemplo Unsplash)
IMAGENES = {}

# Define la carpeta donde se guardarán las imágenes
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/img/productos')

# Asegúrate de que la carpeta existe
os.makedirs(CARPETA, exist_ok=True)

def descargar_imagen(nombre_img, url_img):
    """Descarga una imagen desde la URL y la guarda en la carpeta especificada."""
    ruta = os.path.join(CARPETA, nombre_img)
    
    # Verificar si el archivo ya existe
    if os.path.exists(ruta):
        print(f"{nombre_img} ya existe, omitiendo...")
        return
    
    try:
        # Realizar la solicitud HTTP para obtener la imagen
        r = requests.get(url_img, timeout=10)
        
        # Verificar si la solicitud fue exitosa
        if r.status_code == 200:
            with open(ruta, 'wb') as f:
                f.write(r.content)
            print(f"Descargada: {nombre_img}")
        else:
            print(f"No se pudo descargar {nombre_img}: status {r.status_code}")
    
    except requests.exceptions.RequestException as e:
        # Manejo de errores en caso de que falle la descarga
        print(f"Error descargando {nombre_img}: {e}")
    except (OSError, IOError) as e:
        # Manejo de errores en el sistema de archivos
        print(f"Error al guardar {nombre_img}: {e}")

if __name__ == "__main__":
    for nombre_img, url_img in IMAGENES.items():
        descargar_imagen(nombre_img, url_img)
    print("Descarga automática de imágenes completada.")
