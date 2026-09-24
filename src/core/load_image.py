# src/core/load_image.py
import rasterio

def obtener_metadatos_raster(directorio_imagen_satelital: str) -> tuple:
    with rasterio.open(directorio_imagen_satelital) as imagen_satelital:
        imagen_a_clasificar = imagen_satelital.read()
        metadata_original = imagen_satelital.profile
        nodata = imagen_satelital.nodata
        
    return imagen_a_clasificar, metadata_original, nodata


    

         
     

     




