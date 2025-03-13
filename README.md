# Zoom Video Downloader

Herramienta para descargar videos de Zoom usando Playwright en modo headless, ideal para usar como backend o API.

## Características

- Descarga automática de videos de Zoom desde una URL
- Funciona en modo headless (sin interfaz gráfica)
- Incluye API REST con Flask para integraciones
- Manejo de errores y diagnóstico
- Búsqueda de archivos ya descargados para evitar descargas duplicadas

## Requisitos

- Python 3.7+
- Playwright para Python
- Flask (para la API)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/WilsonKari/zoom-video-downloader.git
cd zoom-video-downloader

# Instalar dependencias
pip install playwright flask

# Instalar navegadores de Playwright
python -m playwright install
```

## Uso

### Como script

```python
from zoom_downloader import descargar_video_zoom

# Descargar un video (con interfaz visible)
resultado = descargar_video_zoom(
    "https://us02web.zoom.us/rec/play/tu-url-de-zoom", 
    "./downloads",
    headless=False
)

# Descargar un video (sin interfaz - modo headless)
resultado = descargar_video_zoom(
    "https://us02web.zoom.us/rec/play/tu-url-de-zoom", 
    "./downloads",
    headless=True
)

print(f"Éxito: {resultado['success']}")
print(f"Archivo: {resultado['file_path']}")
print(f"Mensaje: {resultado['message']}")
```

### Como API

```bash
# Iniciar el servidor API
python zoom_api.py
```

Luego puedes hacer solicitudes a la API:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"url":"https://us02web.zoom.us/rec/play/tu-url-de-zoom"}' \
     http://localhost:5000/api/descargar-zoom
```

## Estructura del proyecto

- `zoom_downloader.py`: Script principal para descargar videos de Zoom
- `zoom_api.py`: Implementación de API REST con Flask

## Licencia

MIT