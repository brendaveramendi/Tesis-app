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

    # Imagen placeholder inicial
    imagen_resultado = ft.Image(
        src=r"C:\Python\TESIS\app\assets\images\tecnologia-fondo-mapa-mundo-que-puede-buscar-direcciones-traves-internet-todo-momento_111088-1367.webp",
        width=500,
        height=280,
        fit="cover"
    )
    
    marco_imagen = ft.Container(
        width=500,
        height=280,
        border_radius=20,
        border=borde_azul(),
        content=imagen_resultado
    )

    mapa_base64_holder = [None]

    # =====================================================
    # FUNCIÓN PARA MOSTRAR POP-UP CON ZOOM INTERACTIVO
    # =====================================================
    def abrir_popup_zoom(e):
        if not mapa_base64_holder[0]:
            return

        visor = ft.InteractiveViewer(
           min_scale=0.5,
           max_scale=5.0,
           boundary_margin=20,
           content=ft.Image(
               src=f"data:image/png;base64,{mapa_base64_holder[0]}",
               fit="contain"
          )
    )

        dialogo = ft.AlertDialog(
        title=ft.Text(
            "Vista Interactiva",
            color="white"
        ),
        content=ft.Container(
            width=900,
            height=700,
            bgcolor="#0F172A",
            border=borde_azul(),
            border_radius=10,
            content=visor
        ),
        actions=[
            ft.TextButton(
                "Cerrar",
                on_click=lambda e: page.pop_dialog()
            )
        ],
        bgcolor="#020617"
    )
        page.show_dialog(dialogo)
        
    async def handle_save_file(e):
        save_file_path = await ft.FilePicker().save_file()
        if save_file_path:
            save_image(save_file_path, app_state.metadata, app_state.imagen_clasificada)

    async def view_classification(e):
      e.control.disabled = True

      marco_imagen.content = ft.ProgressRing(
        color=COLOR_NEON
      )

      page.update()

   
      imagen_string = generar_mapa_clasificacion()

      if imagen_string:

        mapa_base64_holder[0] = imagen_string

        marco_imagen.content = ft.GestureDetector(
            on_tap=abrir_popup_zoom,
            mouse_cursor=ft.MouseCursor.CLICK,
            content=ft.Image(
                src=f"data:image/png;base64,{imagen_string}",
                width=500,
                height=280,
                fit="contain"
            )
        )
        page.snack_bar = ft.SnackBar(
            ft.Text(
                "Mapa cargado. Haz clic para abrir la vista interactiva."
            )
        )

        page.snack_bar.open = True

      else:
        page.snack_bar = ft.SnackBar(
            ft.Text(
                "No se pudo procesar el raster."
            )
        )
        page.snack_bar.open = True

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
                        marco_imagen,
                        ft.Container(height=15),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color="#22C55E", size=30),
                                resultado_texto
                            ]
                        ),
                        ft.Container(height=10),
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