import rasterio
from rasterio.plot import reshape_as_image
from PIL import Image
import base64
from io import BytesIO
import numpy as np
def transformar_tiff(tiff_path):
    """
    Transforma un archivo TIFF en una imagen base64 y devuelve su extensión geográfica.

    Args:
        tiff_path (str): Ruta del archivo TIFF.

    Returns:
        tuple: Imagen en base64 (str) y la extensión geográfica del TIFF (list).
    """
    with rasterio.open(tiff_path) as src:
        # Leer datos y obtener las dimensiones del TIFF
        tiff_data = reshape_as_image(src.read())
        bounds = src.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

        # Normalizar los datos a 8 bits
        tiff_data = normalize_to_8bit(tiff_data)

        # Convertir TIFF a imagen PIL y luego a base64
        pil_img = Image.fromarray(tiff_data)
        buffered = BytesIO()
        pil_img.save(buffered, format="PNG")
        tiff_base64 = base64.b64encode(buffered.getvalue()).decode()

    return tiff_base64, extent



 # ---------------TRANSFORMACIÓN DE TIFF A PNG PARA LOS GRAFICOS------------------
def normalize_to_8bit(data):
    #Normaliza los valores de una matriz a un rango de 0 a 255 para imágenes de 8 bits.
    data = data.astype(np.float32)
    data = (data - data.min()) / (data.max() - data.min()) * 255
    return data.astype(np.uint8)