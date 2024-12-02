import rasterio
from rasterio.plot import reshape_as_image
from PIL import Image
import base64
from io import BytesIO
import numpy as np
import joblib
import os


# Caché para almacenar TIFFs procesados
tiff_cache = {}

# Ruta absoluta para el caché
CACHE_FILE = os.path.abspath("App/data/tiff_cache.pkl")

# Cargar el caché al iniciar si el archivo existe
if os.path.exists(CACHE_FILE):
    try:
        cached_data = joblib.load(CACHE_FILE)
        if cached_data:  # Solo actualizar si no está vacío
            tiff_cache.update(cached_data)
    except Exception as e:
        print("Error al cargar el archivo de caché:", e)

def transformar_tiff(tiff_path):
    """Transforma un archivo TIFF en una imagen base64 y devuelve su extensión geográfica."""
    if tiff_path in tiff_cache:
        print("Retornando TIFF desde caché:", tiff_path)
        return tiff_cache[tiff_path]
    
    with rasterio.open(tiff_path) as src:
        tiff_data = reshape_as_image(src.read())
        bounds = src.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

        # Normalizar a 8 bits
        tiff_data = normalize_to_8bit(tiff_data)

        # Convertir a imagen base64
        pil_img = Image.fromarray(tiff_data)
        buffered = BytesIO()
        pil_img.save(buffered, format="PNG")
        tiff_base64 = base64.b64encode(buffered.getvalue()).decode()
        print("Se procesó la TIFF:", tiff_path)

        # Actualizar y guardar el caché
        tiff_cache[tiff_path] = (tiff_base64, extent)
        save_cache()

    return tiff_base64, extent

def normalize_to_8bit(data):
    """Normaliza los valores de una matriz a un rango de 0 a 255 para imágenes de 8 bits."""
    data = data.astype(np.float32)
    data = (data - data.min()) / (data.max() - data.min()) * 255
    return data.astype(np.uint8)

def save_cache():
    """Guarda el caché en un archivo persistente."""
    try:
        joblib.dump(tiff_cache, CACHE_FILE)
        print("TIFFS guardados en caché:", len(tiff_cache))  # Solo mostramos la cantidad de elementos guardados
        print("Archivo de caché guardado en:", CACHE_FILE)
    except Exception as e:
        print("Error al guardar el archivo de caché:", e)
