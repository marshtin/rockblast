import rasterio
from rasterio.plot import reshape_as_image
from PIL import Image
import base64
from io import BytesIO

def transformar_tiff(tiff_path):
    with rasterio.open(tiff_path) as src:
        # Leer datos y obtener las dimensiones del TIFF
        tiff_data = reshape_as_image(src.read())
        bounds = src.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

        # Convertir TIFF a imagen PIL y luego a base64
        pil_img = Image.fromarray(tiff_data)
        buffered = BytesIO()
        pil_img.save(buffered, format="PNG")
        tiff_base64 = base64.b64encode(buffered.getvalue()).decode()

    return tiff_base64, extent
