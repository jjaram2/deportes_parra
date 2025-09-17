
import os
import sys
import subprocess
from app import create_app, db



# Ejecutar el script de descarga de imágenes antes de iniciar la app
def descargar_imagenes():
    """Ejecuta el script de descarga de imágenes de productos."""
    script_path = os.path.join(os.path.dirname(__file__), 'app', 'scripts', 'descargar_imagenes_productos.py')
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error ejecutando el script de descarga de imágenes: {e}")

descargar_imagenes()

app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    