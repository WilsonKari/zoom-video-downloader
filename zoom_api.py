from flask import Flask, request, jsonify
import os
from zoom_downloader import descargar_zoom_api

app = Flask(__name__)

@app.route('/api/descargar-zoom', methods=['POST'])
def api_descargar_zoom():
    # Obtener datos de la solicitud
    data = request.json
    
    # Validar que se proporcionó una URL
    if not data or 'url' not in data:
        return jsonify({
            'success': False,
            'message': 'Se requiere una URL de Zoom'
        }), 400
    
    # Obtener la URL del video
    url_zoom = data['url']
    
    # Obtener la ruta de descarga (opcional)
    ruta_descarga = data.get('ruta_descarga', os.path.join(os.getcwd(), "downloads"))
    
    # Ejecutar la descarga
    resultado = descargar_zoom_api(url_zoom, ruta_descarga)
    
    # Si la descarga fue exitosa, devolver la ruta del archivo
    if resultado['success']:
        return jsonify({
            'success': True,
            'file_path': resultado['file_path'],
            'message': resultado['message']
        }), 200
    else:
        # Si hubo un error, devolver el mensaje de error
        return jsonify({
            'success': False,
            'message': resultado['message']
        }), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    return jsonify({
        'status': 'online',
        'service': 'Zoom Video Downloader API'
    })

if __name__ == '__main__':
    # Asegurarse de que exista el directorio de descargas
    os.makedirs(os.path.join(os.getcwd(), "downloads"), exist_ok=True)
    
    # Iniciar el servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True)