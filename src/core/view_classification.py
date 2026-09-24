#src/core/view_classification
import io
import base64
import rasterio
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import numpy as np
import src.core.app_state as app_state 

def generar_mapa_clasificacion():
    try:
        clasificacion = app_state.imagen_clasificada
        #with rasterio.open(ruta ,"r") as src:
           # clasificacion = src.read(1)
        
        if app_state.radio_value == True:
            colores = ['#010eff', '#008000', '#01f7ff', '#fff201', '#7e7e7e']
        else:
            colores = ['#010eff','#000000','#f44611','#01f7ff','#804000','#7e7e7e']                                        
       
        clasificacion = np.ma.masked_equal(clasificacion, -9999)
        
        cmap_cultivos = ListedColormap(colores)
        cmap_cultivos.set_bad(color="white", alpha=1.0)
        
        # Subimos levemente el DPI a 140 para que al hacer zoom en el Pop-up no se pixelee la leyenda
        fig, ax = plt.subplots(figsize=(6, 6), dpi=600)
        
        ax.imshow(clasificacion, cmap=cmap_cultivos, vmin=0, vmax=len(colores)-1,interpolation='nearest')
        
        if app_state.radio_value == True:
            leyenda_elementos = [
                mpatches.Patch(color='#010eff', label='Agua'),
                mpatches.Patch(color='#008000', label='Cebada'),
                mpatches.Patch(color='#01f7ff', label='Otro'),
                mpatches.Patch(color='#fff201', label='Trigo'),
                mpatches.Patch(color='#7e7e7e', label='Urbano') 
            ]
        else:
            leyenda_elementos = [
                mpatches.Patch(color='#010eff', label='Agua'),
                mpatches.Patch(color='#000000', label='Girasol'),
                mpatches.Patch(color='#f44611', label='Maiz'),
                mpatches.Patch(color='#01f7ff', label='Otro'),
                mpatches.Patch(color='#804000', label='Soja'),
                mpatches.Patch(color='#7e7e7e', label='Urbano') 
            ]
       
        # Ajuste fino de la caja de la leyenda afuera de los ejes del mapa raster
        ax.legend(handles=leyenda_elementos, loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=8)
        ax.axis('off') 
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True,dpi=600)
        buf.seek(0)
        
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        fig.clf()
        plt.close(fig)
        buf.close()
        
        return img_base64
        
    except Exception as e:
        print(f"Error procesando el mapa geoespacial: {e}")
        return None