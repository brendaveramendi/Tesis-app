# src/views/upload_view.py

# =====================================================
# PANTALLA 2: UPLOAD
# =====================================================
import asyncio
import flet as ft
from src.config.theme import COLOR_NEON
from assets.components.components import (
    borde_azul,
    boton_principal_modificado
)
from src.core.load_image import obtener_metadatos_raster
from src.core.classification import image_classification
import src.core.app_state as app_state

def pantalla_upload(page: ft.Page, navigate_to):
    # ==========================
    # POPUP CARGA
    # ==========================
    barra_progreso = ft.ProgressBar(
    width=300,
    value=app_state.progreso_clasificacion,
    color="#22C55E"
    )

    texto_progreso = ft.Text(
    f"{app_state.progreso_clasificacion}%",
    size=14,
    weight=ft.FontWeight.BOLD
    )
    loading_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Clasificando imagen", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                #ft.ProgressRing(width=40, height=40, color="#22C55E"),
                barra_progreso,
                texto_progreso,
                ft.Container(height=10),
                ft.Text("Procesando imagen satelital...", size=14),
                ft.Text("Ejecutando Voting Classifier por lotes", size=12, color="#94A3B8")
            ],
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # ==========================
    # CANCELAR
    # ==========================
    async def cancelar_proceso(e):
        app_state.cancelar_clasificacion = True
        loading_dialog.open = False
        page.update()

    loading_dialog.actions = [
        ft.TextButton(
            "Cancelar",
            on_click=cancelar_proceso
        )
    ]
    if loading_dialog not in page.overlay:
        page.overlay.append(loading_dialog)
    

    # ==========================================
    # INTERMEDIARIO QUE ACTUALIZA LOS CONTROLES
    # ==========================================
    def notificar_flet():
        # Lee el progreso actual desde app_state y altera los controles en pantalla
        barra_progreso.value = app_state.progreso_clasificacion
        texto_progreso.value = f"{int(app_state.progreso_clasificacion * 100)}%"
        
        # Ejecuta la actualización visual de forma segura fuera del hilo de cálculo
        async def actualizar_interfaz():
            page.update()
        page.run_task(actualizar_interfaz)
    # ==========================
    # CLASIFICAR
    # ==========================
    async def clasificar_y_navegar(e):
        app_state.cancelar_clasificacion = False
        
        loading_dialog.open = True
        page.update()

        try:
            # hilo secundario
            await asyncio.to_thread(image_classification, on_progress=notificar_flet)

            # Cerrar 
            loading_dialog.open = False
            page.update()

            # Cerrar 
            loading_dialog.open = False
            page.update()

           
            if not app_state.cancelar_clasificacion:
                navigate_to(page, "/result")

        except Exception as ex:
            loading_dialog.open = False
            page.update()
            print(f" Error durante la clasificación: {ex}")
    

    # ==========================
    # BOTÓN CLASIFICAR
    # ==========================
    boton_clasificar = ft.Container(
        visible=False,
        content=boton_principal_modificado(
            "CLASIFICAR CULTIVO",
            clasificar_y_navegar
        )
    )

    # ==========================
    # SELECCIONAR TIFF
    # ==========================
    async def handle_pick_files(e):
        files = await ft.FilePicker().pick_files(
            allowed_extensions=["tif", "tiff"]
        )

        if files:
            (
                app_state.imagen,
                app_state.metadata,
                app_state.nodata
            ) = obtener_metadatos_raster(files[0].path)

            boton_clasificar.visible = True
            page.update()

    # ==========================
    # VISTA
    # ==========================
    return ft.View(
        route="/upload",
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="white",
                on_click=lambda e: navigate_to(page, "/home")
            ),
            bgcolor="transparent",
            elevation=0
        ),
        controls=[
            ft.Container(
                expand=True,
                padding=40,
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
                            "SUBIR IMAGEN SATELITAL (.TIF)",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_NEON,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=30),
                        ft.Container(
                            width=700,
                            height=260,
                            border_radius=25,
                            border=borde_azul(3),
                            on_click=handle_pick_files,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.SATELLITE_ALT,
                                        size=80,
                                        color="#67E8F9"
                                    ),
                                    ft.Text(
                                        "DROP-OUT ZONE",
                                        size=32,
                                        weight=ft.FontWeight.BOLD,
                                        color="#BAE6FD"
                                    ),
                                    ft.Text(
                                        "SUBA ARCHIVO (.TIF)",
                                        size=22,
                                        color="white"
                                    ),
                                    ft.Text(
                                        "GeoTIFF soportado",
                                        size=16,
                                        color="#CBD5E1"
                                    )
                                ]
                            )
                        ),
                        ft.Container(height=30),
                        boton_clasificar
                    ]
                )
            )
        ]
    )

