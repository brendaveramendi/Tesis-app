import flet as ft
from src.config.theme import COLOR_BOTON

# =====================================================
 # COMPONENTES REUTILIZABLES
# =====================================================
def borde_azul(grosor=2)-> ft.Border:
    return  ft.Border(
        left=ft.BorderSide(grosor, "#38BDF8"),
        top=ft.BorderSide(grosor, "#38BDF8"),
        right=ft.BorderSide(grosor, "#38BDF8"),
        bottom=ft.BorderSide(grosor, "#38BDF8"),
    )
def boton_principal(texto, funcion, icono=None)-> ft.Container:
    return ft.Container(
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color="#38BDF8"
        ),
        content=ft.Button(
            content=ft.Text(
                value=texto,
                size=20,
                weight=ft.FontWeight.BOLD,
                color="white"
            ),
            icon=icono,
            on_click=funcion,
            width=350,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=COLOR_BOTON,
                shape=ft.RoundedRectangleBorder(radius=20),
                mouse_cursor=ft.MouseCursor.CLICK
            )
        )
    )
    
#=====================================================
# BOTON DOS_ESTADOS
#====================================================
def boton_principal_modificado(texto, funcion, icono=None, disabled=False) -> ft.Container:
    # Definimos colores según el estado
    COLOR_ACTIVO = "#0EA5E9"  # Tu color de botón normal (ej: Celeste/Azul)
    COLOR_MUTED = "#334155"   # Gris oscuro para el estado deshabilitado
    
    return ft.Container(
        # La sombra solo brilla si el botón está activo
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color="#38BDF8" if not disabled else ft.Colors.TRANSPARENT
        ),
        content=ft.Button(
            content=ft.Text(
                value=texto,
                size=24,
                weight=ft.FontWeight.BOLD,
                color="white" if not disabled else "#94A3B8"
            ),
            icon=icono,
            on_click=funcion if not disabled else None, # Bloquea el click nativo
            disabled=disabled,
            width=450,
            height=80,
            style=ft.ButtonStyle(
                bgcolor=COLOR_ACTIVO if not disabled else COLOR_MUTED,
                shape=ft.RoundedRectangleBorder(radius=20),
                mouse_cursor=ft.MouseCursor.CLICK
            )
        )
    )
    
#
#Boton clasificar
#
boton_clasificar=    ft.Container(
                                visible=False,
                                content=boton_principal_modificado(
                                    "CLASIFICAR CULTIVO",
                                    lambda e: navigate_to(page, "/result")
                                   )
                                ),
# =====================================================
# VARIABLES DE ESTADO (ESTÁTICOS DE INTERFAZ)
# =====================================================
cultivo_texto = ft.Text(
    value="Cultivo seleccionado: Invernal",
    color="white",
    size=18,
     weight=ft.FontWeight.BOLD
)

resultado_texto = ft.Text(
    value="Análisis completado",
    color="#4ADE80",
    size=22,
    weight=ft.FontWeight.BOLD
)

def seleccionar_fina(e):
    cultivo_texto.value = "Cultivo seleccionado: Invernal"
    cultivo_texto.update()

def seleccionar_gruesa(e):
    cultivo_texto.value = "Cultivo seleccionado: Estival"
    cultivo_texto.update()
