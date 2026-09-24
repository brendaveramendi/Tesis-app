"""
# =====================================================
# PANTALLA 3: RESULTADO
# =====================================================
import flet as ft 
from src.config.theme import COLOR_NEON
from assets.components.components import (borde_azul,
                                              boton_principal,
                                              resultado_texto)
import src.core.app_state as app_state
from src.core.classification import save_image
# =====================================================
# PANTALLA 3: RESULTADO
# =====================================================
def pantalla_resultado(page,navigate_to):
    async def handle_save_file(e: ft.Event[ft.Button]):
        save_file_path = await ft.FilePicker().save_file()
        save_image(save_file_path,app_state.metadata,app_state.imagen_clasificada)
    
    async def view_classification(e: ft.Event[ft.Button]):
        return ft.Image(
            src=r"C:\Python\TESIS\app\assets\images\Imagen_Clasificada_BT_Confianza_0.8_Fina.tif",
            width=600,
            height=600,
            fit="cover"
        )
    return ft.View(
        route="/result",
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK, 
                on_click=lambda e: navigate_to(page, "/upload"),
                icon_color="white"
            ),
            bgcolor="transparent",
            elevation=0
        ),
        controls=[
            ft.Container(
                expand=True,
                padding=30,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.Alignment(-1, -1),
                    end=ft.alignment.Alignment(1, 1),
                    colors=["#020617", "#0F172A"]
                ),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text(
                            "CLASIFICACIÓN DE CULTIVOS - RESULTADOS",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_NEON,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=20),
                        
                        # IMAGEN RESULTADO
                        ft.Container(
                            width=500,
                            height=280,
                            border_radius=20,
                            border=borde_azul(),                                
                            content=ft.Image(
                                src=r"C:\Python\TESIS\app\assets\images\tecnologia-fondo-mapa-mundo-que-puede-buscar-direcciones-traves-internet-todo-momento_111088-1367.webp",
                                width=500,
                                height=280,
                                fit="cover"
                            )
                        ),
                        ft.Container(height=15),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color="#22C55E", size=30),
                                resultado_texto
                            ]
                        ),
                        ft.Container(height=10),
                        # ACCIONES
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                            boton_principal("GUARDAR CLASIFICACIÓN", handle_save_file),
                            boton_principal("VER CLASIFICACIÓN", view_classification)
                            ]
                        ),
                        ft.Container(height=15),
                        
                    ]
                )
            )
        ]
    )
""" 
#Resultado antes de agregar
"""
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import numpy as np

ruta = r"C:\Python\TESIS\app\assets\images\Imagen_Clasificada_BT_Confianza_0.8_Fina.tif"
# 1. Abrir la imagen raster .tif de la clasificación
with rasterio.open(ruta) as src:
    clasificacion = src.read(1)  

def viewer():
    # 2. Definir tu paleta de colores personalizada
    colores = ['#010eff', '#008000', '#01f7ff','#fff201','#7e7e7e'] # Gris, Amarillo, Azul
    cmap_cultivos = ListedColormap(colores)
    
    # 3. Configurar los límites para que cada color calce justo con el ID del mapa
    # Si tus valores van de 0 a 2, los límites de los bins deben ser [-0.5, 0.5, 1.5, 2.5]
    valores_unicos = np.unique(clasificacion)
    bounds = np.arange(len(colores) + 1) - 0.5
    
    # 4. Graficar la clasificación
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Usamos ax.imshow para tener control total de los colores y la leyenda
    image = ax.imshow(clasificacion, cmap=cmap_cultivos, vmin=0, vmax=len(colores)-1)
    #['#010eff', '#008000', '#01f7ff','#fff201','#7e7e7e']
    # 5. Crear una leyenda personalizada "facha"
    leyenda_elementos = [
        mpatches.Patch(color='#010eff', label='Agua'),
        mpatches.Patch(color='#008000', label='Cebada'),
        mpatches.Patch(color='#01f7ff', label='Otro'),
        mpatches.Patch(color='#fff201', label='Trigo'),
        mpatches.Patch(color='#7e7e7e', label='Trigo')
    ]
    ax.legend(handles=leyenda_elementos, loc='upper right', bbox_to_anchor=(1.3, 1))

    plt.title("Clasificación de Cobertura Terrestre / Cultivos", fontsize=14, pad=15)
    plt.axis('off') # Opcional: oculta los ejes de píxeles si no los necesitás
    plt.show()
""" 
###VIEW_CLASSIFICATION
###############################################
## View_classification
#src/core/view_classification
import flet as ft
import io
import base64
import rasterio
import matplotlib
matplotlib.use('Agg')  # CRITICAL: Evita que Matplotlib intente abrir ventanas externas
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import numpy as np

from src.config.theme import COLOR_NEON
from assets.components.components import (
    borde_azul,
    boton_principal,
    resultado_texto
)
import src.core.app_state as app_state
from src.core.classification import save_image

# =====================================================
# MOTOR DE RENDERIZADO GEOESPACIAL (MATPLOTLIB)
# =====================================================
def generar_mapa_clasificacion(ruta_tif):
    try:
        with rasterio.open(ruta_tif) as src:
            clasificacion = src.read(1)
        colores = ['#010eff', '#008000', '#01f7ff', '#fff201', '#7e7e7e']
       
        clasificacion = np.ma.masked_equal(clasificacion, -9999)
        
        cmap_cultivos = ListedColormap(colores)
        cmap_cultivos.set_bad(color="white")
        
        fig, ax = plt.subplots(figsize=(6, 6), dpi=120)
        
        ax.imshow(clasificacion, cmap=cmap_cultivos, vmin=0, vmax=len(colores)-1)
        
        leyenda_elementos = [
            mpatches.Patch(color='#010eff', label='Agua'),
            mpatches.Patch(color='#008000', label='Cebada'),
            mpatches.Patch(color='#01f7ff', label='Otro'),
            mpatches.Patch(color='#fff201', label='Trigo'),
            mpatches.Patch(color='#7e7e7e', label='Urbano') 
        ]
       
        ax.legend(handles=leyenda_elementos, loc='upper right', bbox_to_anchor=(1.25, 1), fontsize=8)
        ax.axis('off') 
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        
       
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        
        fig.clf()
        plt.close(fig)
        buf.close()
        
        return img_base64
        
    except Exception as e:
        print(f"Error procesando el mapa geoespacial: {e}")
        return None
#Pantalla correcta de result_view

#src/views/result_view
import flet as ft
from src.config.theme import COLOR_NEON
from assets.components.components import (
    borde_azul,
    boton_principal,
    resultado_texto
)
import src.core.app_state as app_state
from src.core.classification import save_image


def pantalla_resultado(page, navigate_to):
    # Imagen que se muestra inicialmente
    imagen_resultado = ft.Image(
        src=r"C:\Python\TESIS\app\assets\images\tecnologia-fondo-mapa-mundo-que-puede-buscar-direcciones-traves-internet-todo-momento_111088-1367.webp",
        width=500,
        height=280,
        fit="cover"
    )

    async def handle_save_file(e):
        save_file_path = await ft.FilePicker().save_file()

        if save_file_path:
            save_image(
                save_file_path,
                app_state.metadata,
                app_state.imagen_clasificada
            )

    async def view_classification(e):
        # Cambiar la imagen mostrada

        imagen_resultado.src = (
            r"C:\Python\TESIS\app\assets\images\Imagen_Clasificada_BT_Confianza_0.8_Fina.tif"
        )
        page.update()

    return ft.View(
        route="/result",
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: navigate_to(page, "/upload"),
                icon_color="white"
            ),
            bgcolor="transparent",
            elevation=0
        ),
        controls=[
            ft.Container(
                expand=True,
                padding=30,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.Alignment(-1, -1),
                    end=ft.alignment.Alignment(1, 1),
                    colors=["#020617", "#0F172A"]
                ),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text(
                            "CLASIFICACIÓN DE CULTIVOS - RESULTADOS",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_NEON,
                            text_align=ft.TextAlign.CENTER
                        ),

                        ft.Container(height=20),

                        # CONTENEDOR DE IMAGEN
                        ft.Container(
                            width=500,
                            height=280,
                            border_radius=20,
                            border=borde_azul(),
                            content=imagen_resultado
                        ),

                        ft.Container(height=15),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.CHECK_CIRCLE,
                                    color="#22C55E",
                                    size=30
                                ),
                                resultado_texto
                            ]
                        ),

                        ft.Container(height=10),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                boton_principal(
                                    "GUARDAR CLASIFICACIÓN",
                                    handle_save_file
                                ),
                                boton_principal(
                                    "VER CLASIFICACIÓN",
                                    view_classification
                                )
                            ]
                        ),

                        ft.Container(height=15),
                    ]
                )
            )
        ]
    )
##########################################################################
##Imagen pequeña
#src/views/result_view
import flet as ft
from src.config.theme import COLOR_NEON
from assets.components.components import (
    borde_azul,
    boton_principal,
    resultado_texto
)
import src.core.app_state as app_state
from src.core.classification import save_image
from src.core.view_classification import generar_mapa_clasificacion

def pantalla_resultado(page, navigate_to):

    # Imagen placeholder que se muestra inicialmente (Mapa base)
    imagen_resultado = ft.Image(
        src=r"C:\Python\TESIS\app\assets\images\tecnologia-fondo-mapa-mundo-que-puede-buscar-direcciones-traves-internet-todo-momento_111088-1367.webp",
        width=500,
        height=280,
        fit="cover"
    )
    spinner_carga = ft.ProgressRing(color=COLOR_NEON, visible=False)
    # Marco contenedor dinámico
    marco_imagen = ft.Container(
        width=500,
        height=280,
        border_radius=20,
        border=borde_azul(),
        content=imagen_resultado
    )

    async def handle_save_file(e):
        save_file_path = await ft.FilePicker().save_file()
        if save_file_path:
            save_image(
                save_file_path,
                app_state.metadata,
                app_state.imagen_clasificada
            )

    async def view_classification(e):
        # 1. Animación de carga en lo que Rasterio procesa la matriz de píxeles
        e.control.disabled = True
        marco_imagen.content = ft.ProgressRing(color=COLOR_NEON)
        page.update()

        # Ruta absoluta de tu TIFF
        ruta_tiff = r"C:\Python\TESIS\app\assets\images\Imagen_Clasificada_BT_Confianza_0.8_Fina.tif"
        
        # 2. Llamamos al motor de renderizado
        imagen_string = generar_mapa_clasificacion(ruta_tiff)
        
        if imagen_string:
            marco_imagen.content = ft.Image(
            src=f"data:image/png;base64,{imagen_string}", 
            width=500,
            height=280,
            fit="contain"
            )
            marco_imagen.update()
        else:
            # Si falla el renderizado devolvemos el placeholder y avisamos
            marco_imagen.content = imagen_resultado
            page.snack_bar = ft.SnackBar(ft.Text("No se pudo leer o procesar el archivo raster .tif"))
            page.snack_bar.open = True

        # 4. Reactivamos botón y refrescamos toda la UI
        e.control.disabled = False
        page.update()

    return ft.View(
        route="/result",
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: navigate_to(page, "/upload"),
                icon_color="white"
            ),
            bgcolor="transparent",
            elevation=0
        ),
        controls=[
            ft.Container(
                expand=True,
                padding=30,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.Alignment(-1, -1),
                    end=ft.alignment.Alignment(1, 1),
                    colors=["#020617", "#0F172A"]
                ),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text(
                            "CLASIFICACIÓN DE CULTIVOS - RESULTADOS",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_NEON,
                            text_align=ft.TextAlign.CENTER
                        ),

                        ft.Container(height=20),

                        # CONTENEDOR DE IMAGEN (Asignado al componente dinámico)
                        marco_imagen,

                        ft.Container(height=15),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.CHECK_CIRCLE,
                                    color="#22C55E",
                                    size=30
                                ),
                                resultado_texto
                            ]
                        ),

                        ft.Container(height=10),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                boton_principal(
                                    "GUARDAR CLASIFICACIÓN",
                                    handle_save_file
                                ),
                                boton_principal(
                                    "VER CLASIFICACIÓN",
                                    view_classification
                                )
                            ]
                        ),

                        ft.Container(height=15),
                    ]
                )
            )
        ]
    )
    
