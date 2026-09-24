import numpy as np
import rasterio
import joblib
from tqdm import tqdm
import warnings
from dotenv import load_dotenv
from pathlib import Path
import os
import src.core.app_state as app_state

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="sklearn"
)
def model_selection() -> tuple:
    load_dotenv()  

    BASE_DIR = Path(os.environ["TESIS_BASE_DIR"])   
    if app_state.radio_value == True:
        voting = joblib.load(
        f"{BASE_DIR}\src\models\B1B2B3B4B5B6B7B8BB9B11B12_N_W_B_R_G_boost_0.80_FILTRO_FINA.pkl"
        )
        scaler = joblib.load(
            f"{BASE_DIR}\src\models\standar\B1B2B3B4B5B6B7B8BB9B11B12_N_W_B_R_G_STANDAR_0.80_FILTRO_FINA.pkl"
         ) 
        UMBRAL_CONFIANZA = 0.80
        INDICE_OTRO = 2 
        print(UMBRAL_CONFIANZA,INDICE_OTRO)
    else:
         voting = joblib.load(
            rf"{BASE_DIR}\app\src\models\B1B2B3B4B5B6B7B8BB9B11B12_N_W_B_R_G_MODELO_0.80_FILTRO_gruesa.pkl"
            )
         scaler = joblib.load(
            rf"{BASE_DIR}\app\src\models\standar\B1B2B3B4B5B6B7B8BB9B11B12_N_W_B_R_G_STANDAR_0.80_FILTRO_gruesa.pkl"
         )  
         UMBRAL_CONFIANZA = 0.8
         INDICE_OTRO = 3
         print(UMBRAL_CONFIANZA,INDICE_OTRO)
    return voting,scaler, UMBRAL_CONFIANZA, INDICE_OTRO

def save_image(salida, metadata_original, imagen_clasificada):
    if not salida:
        print("No se seleccionó ninguna ruta de guardado.")
        return
    if not salida.lower().endswith(('.tif', '.tiff')):
        salida += ".tif"

    print(f" Guardando: {salida}")
    with rasterio.open(salida, "w", **metadata_original) as dst:
        dst.write(imagen_clasificada.astype(rasterio.int32), 1)
    


def image_classification(on_progress=None):
    imagen_a_clasificar = app_state.imagen
    metadata_original = app_state.metadata
    nodata = app_state.nodata
    voting,scaler,UMBRAL_CONFIANZA, INDICE_OTRO = model_selection()
    batch_size = 10000

    clases_predichas = []
    if nodata is not None:
        mascara_nodata = (imagen_a_clasificar[0] == nodata)
    else:
        mascara_nodata = np.all(imagen_a_clasificar == 0,axis=0)

    imagen_a_clasificar = imagen_a_clasificar.reshape(
        (imagen_a_clasificar.shape[0], -1)).T

    imagen_a_clasificar = scaler.transform(imagen_a_clasificar)

    total_batches = len(range(0, len(imagen_a_clasificar), batch_size))
    for index, i in enumerate( tqdm(range(0,len(imagen_a_clasificar),batch_size),desc="Clasificando")):
        if app_state.cancelar_clasificacion:
            
            return

        batch = imagen_a_clasificar[i:i + batch_size]

        probas = voting.predict_proba(batch)
        
        app_state.progreso_clasificacion = (
        (index + 1) / total_batches)
        
        # --- NOTIFICAR
        if on_progress:
            # Optimizamos reduciendo los llamados de actualización a Flet
            if index % 5 == 0 or app_state.progreso_clasificacion >= 1.0:
                on_progress()
        
        indices_ganadores = np.argmax(probas,axis=1)

        seguridad_maxima = np.max(
            probas,
            axis=1
        )

        etiquetas_finales = np.where(
            seguridad_maxima >= UMBRAL_CONFIANZA,
            indices_ganadores,
            INDICE_OTRO
        )

        clases_predichas.extend(
            etiquetas_finales
        )
      

    clases_predichas = np.array(
        clases_predichas
    )

    imagen_clasificada = clases_predichas.reshape(
        (
            metadata_original["height"],
            metadata_original["width"]
        )
    )

    imagen_clasificada[
        mascara_nodata
    ] = -9999

    metadata_original.update(
        count=1,
        dtype=rasterio.int32,
        nodata=-9999
    )
    app_state.imagen_clasificada = imagen_clasificada
    app_state.metadata = metadata_original
    
    app_state.clasificacion_terminada = True
    print("Clasificación finalizada")
    