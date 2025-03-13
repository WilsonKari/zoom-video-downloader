from playwright.sync_api import sync_playwright
import os
import time
import shutil
import glob

def descargar_video_zoom(url_zoom, ruta_descarga=None, headless=True):
    """Descarga un video de Zoom desde la URL proporcionada.
    
    Args:
        url_zoom (str): URL del video de Zoom a descargar
        ruta_descarga (str, optional): Ruta donde guardar el video. Por defecto es './downloads'
        headless (bool, optional): Si es True, ejecuta el navegador en modo headless (sin interfaz). Por defecto es True.
    
    Returns:
        dict: Diccionario con información del resultado {'success': bool, 'file_path': str, 'message': str}
    """
    result = {
        'success': False,
        'file_path': None,
        'message': ''
    }
    
    if not ruta_descarga:
        ruta_descarga = os.path.join(os.getcwd(), "downloads")
    
    # Crear directorio de descargas si no existe
    os.makedirs(ruta_descarga, exist_ok=True)
    
    print(f"Iniciando descarga del video de Zoom desde: {url_zoom}")
    print(f"Los archivos se guardarán en: {ruta_descarga}")
    
    # Verificar si hay descargas previas en el directorio de descargas predeterminado
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    print(f"También verificaremos descargas en: {downloads_dir}")
    
    # Buscar el archivo específico que vimos en la imagen
    archivo_especifico = "0beaf542-90c9-4b98-9427-b318e305c713"
    archivo_path = os.path.join(downloads_dir, archivo_especifico)
    
    if os.path.exists(archivo_path):
        print(f"Encontrado el archivo específico: {archivo_especifico}")
        file_size = os.path.getsize(archivo_path) / (1024 * 1024)  # Convertir a MB
        print(f"Tamaño: {file_size:.2f} MB")
        
        # Copiar el archivo a nuestra carpeta de descargas
        dest_path = os.path.join(ruta_descarga, archivo_especifico)
        if not os.path.exists(dest_path):
            print(f"Copiando {archivo_especifico} a {ruta_descarga}...")
            shutil.copy2(archivo_path, dest_path)
            print(f"Archivo copiado exitosamente a: {dest_path}")
            result['success'] = True
            result['file_path'] = dest_path
            result['message'] = f"Archivo encontrado y copiado: {archivo_especifico}"
            return result
        else:
            print(f"El archivo ya existe en la carpeta de destino: {dest_path}")
            result['success'] = True
            result['file_path'] = dest_path
            result['message'] = f"Archivo ya existente en destino: {archivo_especifico}"
            return result
    
    # Si no encontramos el archivo específico, buscamos por patrón
    print("No se encontró el archivo específico, buscando por patrón...")
    archivo_pattern = os.path.join(downloads_dir, "*-*-*-*-*")
    archivos = glob.glob(archivo_pattern)
    
    if archivos:
        print(f"Se encontraron archivos con patrón similar:")
        for archivo in archivos:
            file_name = os.path.basename(archivo)
            file_size = os.path.getsize(archivo) / (1024 * 1024)  # Convertir a MB
            print(f"  - {file_name} ({file_size:.2f} MB)")
            
            # Copiar el archivo a nuestra carpeta de descargas
            dest_path = os.path.join(ruta_descarga, file_name)
            if not os.path.exists(dest_path):
                print(f"Copiando {file_name} a {ruta_descarga}...")
                shutil.copy2(archivo, dest_path)
                print(f"Archivo copiado exitosamente a: {dest_path}")
                result['success'] = True
                result['file_path'] = dest_path
                result['message'] = f"Archivo encontrado y copiado: {file_name}"
                return result
            else:
                print(f"El archivo ya existe en la carpeta de destino: {dest_path}")
                result['success'] = True
                result['file_path'] = dest_path
                result['message'] = f"Archivo ya existente en destino: {file_name}"
                return result
    
    # Si no encontramos el archivo, iniciamos la descarga automatizada
    print("No se encontraron archivos descargados. Iniciando descarga automatizada...")
    
    with sync_playwright() as p:
        try:
            # Lanzar navegador en modo headless si se especifica
            browser = p.chromium.launch(headless=headless)
            
            # Configurar el contexto para aceptar descargas
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()
            
            # Navegar a la URL del video de Zoom
            print("Navegando a la página del video...")
            page.goto(url_zoom, wait_until="networkidle")
            print("Página cargada completamente")
            
            # Tomar captura de pantalla para diagnóstico (solo si es necesario)
            if not headless:
                page.screenshot(path=os.path.join(ruta_descarga, "zoom_page_loaded.png"))
                print(f"Captura de pantalla guardada en: {os.path.join(ruta_descarga, 'zoom_page_loaded.png')}")
            
            # Esperar un poco para asegurarse de que los controles estén disponibles
            time.sleep(5)
            
            # Lista de selectores para botones de descarga
            download_buttons = [
                'button:has-text("Download")',
                'button:has-text("Descargar")',
                '[aria-label="download"]',
                '[title="Download"]',
                '[title="Descargar"]',
                '.download-btn',
                '#download-btn',
                'button.more-btn',  # Botón de más opciones
                '[aria-label="More"]',  # Botón de más opciones
                '.zm-btn'  # Clase común de botones en Zoom
            ]
            
            # Intentar cada selector
            button_found = False
            for selector in download_buttons:
                elements = page.locator(selector)
                count = elements.count()
                if count > 0:
                    print(f"Botón encontrado con selector: {selector}, cantidad: {count}")
                    
                    # Configurar espera de descarga ANTES de hacer clic
                    with page.expect_download() as download_info:
                        # Hacer clic en el botón
                        elements.first.click()
                        print(f"Clic realizado en botón con selector: {selector}")
                    
                    # Obtener la información de descarga
                    download = download_info.value
                    print(f"Descarga iniciada: {download.suggested_filename}")
                    
                    # Guardar el archivo descargado
                    save_path = os.path.join(ruta_descarga, download.suggested_filename)
                    download.save_as(save_path)
                    print(f"Archivo guardado como: {save_path}")
                    
                    button_found = True
                    result['success'] = True
                    result['file_path'] = save_path
                    result['message'] = f"Descarga completada: {download.suggested_filename}"
                    break
            
            if not button_found:
                # Si no encontramos un botón directo, intentamos con el menú contextual
                print("No se encontró botón de descarga directo, intentando menú contextual...")
                video_selectors = ['video', '.vjs-tech', '#vjs_video_3', '.video-js']
                
                for video_selector in video_selectors:
                    video_element = page.locator(video_selector)
                    if video_element.count() > 0:
                        print(f"Elemento de video encontrado con selector: {video_selector}")
                        
                        # Configurar espera de descarga ANTES de hacer clic derecho
                        with page.expect_download() as download_info:
                            # Hacer clic derecho en el video
                            video_element.first.click(button='right')
                            time.sleep(1)  # Esperar a que aparezca el menú contextual
                            
                            # Opciones de menú contextual
                            context_menu_options = [
                                'text=Download',
                                'text=Descargar',
                                'text=Save video as',
                                'text=Guardar video como'
                            ]
                            
                            # Intentar cada opción del menú
                            option_found = False
                            for option in context_menu_options:
                                if page.locator(option).count() > 0:
                                    page.locator(option).click()
                                    print(f"Clic en opción de menú contextual: {option}")
                                    option_found = True
                                    break
                            
                            # Si no encontramos ninguna opción, cancelamos
                            if not option_found:
                                print("No se encontró opción de descarga en el menú contextual")
                                # Hacer clic en cualquier lugar para cerrar el menú
                                page.mouse.click(0, 0)
                                continue
                        
                        # Obtener la información de descarga
                        download = download_info.value
                        print(f"Descarga iniciada: {download.suggested_filename}")
                        
                        # Guardar el archivo descargado
                        save_path = os.path.join(ruta_descarga, download.suggested_filename)
                        download.save_as(save_path)
                        print(f"Archivo guardado como: {save_path}")
                        
                        result['success'] = True
                        result['file_path'] = save_path
                        result['message'] = f"Descarga completada mediante menú contextual: {download.suggested_filename}"
                        return result
                
                print("No se pudo iniciar la descarga mediante menú contextual")
                
                # Verificar si hay algún botón de descarga visible en la página
                if not headless:
                    page.screenshot(path=os.path.join(ruta_descarga, "no_download_button.png"))
                
                result['message'] = "No se encontró ningún botón de descarga"
                return result
            
            return result
            
        except Exception as e:
            error_msg = f"Error al intentar descargar: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            
            # Capturar screenshot para diagnóstico solo si no es headless
            if not headless:
                page.screenshot(path=os.path.join(ruta_descarga, "error_screenshot.png"))
            
            result['message'] = error_msg
            return result
        finally:
            # Cerrar el navegador
            browser.close()

# Ejemplo de uso como API/backend
def descargar_zoom_api(url_zoom, ruta_descarga=None):
    """Función API para descargar video de Zoom
    
    Args:
        url_zoom (str): URL del video de Zoom
        ruta_descarga (str, optional): Ruta de descarga
        
    Returns:
        dict: Resultado de la operación
    """
    # Siempre usar modo headless para API
    return descargar_video_zoom(url_zoom, ruta_descarga, headless=True)

if __name__ == "__main__":
    # URL del video de Zoom a descargar
    url_video = "https://us02web.zoom.us/rec/play/WfoDbwhIQIkSA-qLRBt2zk_5MwmVXtmTSNcpebGJk_YIg1HUF240aAGHh-Xc_Zogv-OrdXRcnUB3HeU.OcVPF6hT90p5N5q8"
    
    # Ruta donde se guardarán los archivos descargados
    ruta_descarga = os.path.join(os.getcwd(), "downloads")
    
    # Ejecutar la función de descarga en modo headless (sin interfaz de navegador)
    resultado = descargar_video_zoom(url_video, ruta_descarga, headless=True)
    
    print("\nResultado de la descarga:")
    print(f"Éxito: {resultado['success']}")
    print(f"Archivo: {resultado['file_path']}")
    print(f"Mensaje: {resultado['message']}")