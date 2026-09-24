# src/views/home_view.py
import flet as ft
from src.config.theme import COLOR_NEON
from assets.components.components import (borde_azul, boton_principal, cultivo_texto)
import src.core.app_state as app_state

def pantalla_inicio(page: ft.Page, navigate_to) -> ft.View:
    def cambiar_cultivo(e):
        if e.control.value == "invernal":
            cultivo_texto.value = "Cultivo seleccionado: Invernal"
            app_state.radio_value = True
        elif e.control.value == "estival":
            cultivo_texto.value = "Cultivo seleccionado: Estival"
            app_state.radio_value = False
        cultivo_texto.update()
        
    def cambiar_campana(e):
        app_state.campana_seleccionada = e.control.value
        print(f"Campaña guardada en el estado: {app_state.campana_seleccionada}")

    # 1. Selector de Campaña estilizado
    selector_campana = ft.Dropdown(
        label="Campaña Agrícola",
        hint_text="Seleccione un año",
        value="2022/2023",
        width=240,
        color="white",
        label_style=ft.TextStyle(color="#94A3B8", size=14),
        hint_style=ft.TextStyle(color="#64748B"),
        border_color="#334155",  # Borde inicial sutil
        focused_border_color=COLOR_NEON,
        bgcolor="#0F172A",  # Fondo interno oscuro para que no trasluzca
        border_radius=12,
        on_select=cambiar_campana,
        options=[
            ft.dropdown.Option("2019/2020"),
            ft.dropdown.Option("2020/2021"),
            ft.dropdown.Option("2021/2022"),
            ft.dropdown.Option("2022/2023"),
            ft.dropdown.Option("2023/2024"),
        ]
    )

    return ft.View(
        route="/home",
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
                            "LAND COVER CLASSIFIER",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_NEON,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "ANÁLISIS DE IMÁGENES SATELITALES",
                            size=15,
                            italic=True,
                            color="#94A3B8"
                        ),
                        ft.Container(height=15),
                        
                        #Mapa
                       # ft.Container(
                        #    width=900,
                         #   height=180,
                          #  border_radius=20,
                           # border=borde_azul(),
                            #shadow=ft.BoxShadow(blur_radius=25, color="rgba(56, 189, 248, 0.3)"),
                            #content=ft.Image(
                             #   src=r"C:\Python\TESIS\app\assets\images\Tierra.png",
                              #  fit="cover"
                            #)
                            ft.Stack(
                            controls=[
                                # Capa Fondo: La Imagen del Mapa
                                ft.Container(
                                    width=900,
                                    height=180,  
                                    border_radius=20,
                                    border=borde_azul(),
                                    shadow=ft.BoxShadow(blur_radius=25, color="rgba(56, 189, 248, 0.3)"),
                                    content=ft.Image(
                                        src=r"C:\Python\TESIS\app\assets\images\Tierra.png",
                                        fit="COVER"
                                    )
                                ),
                                # Capa Superior: El Botón centrado
                                ft.Container(
                                    width=900,
                                    height=180,
                                    alignment=ft.Alignment.CENTER,  # Centra el botón exactamente a la mitad de la imagen
                                    content=boton_principal(
                                        "EMPEZAR CLASIFICACIÓN",
                                        lambda e: navigate_to(page, "/upload"),
                                        ft.Icons.PLAY_ARROW
                                    )
                                )
                            ]
                         ),
                        
                        ft.Container(height=20),
                        ft.Container(
                         width=700,
                         bgcolor="#1E293B",
                         padding=20,
                         border_radius=20,
                         border=ft.Border.all(1, "#334155"),
                         shadow=ft.BoxShadow(
                             blur_radius=15,
                             spread_radius=1,
                             color="#00000055"
                         ),
                         content=ft.Column(
                             spacing=20,
                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                             controls=[
                                 ft.Text(
                                     "CONFIGURACIÓN DE CLASIFICACIÓN",
                                     color=COLOR_NEON,
                                     size=18,
                                     weight=ft.FontWeight.BOLD
                                 ),

                                 ft.Divider(color="#334155"),

                                 ft.Row(
                                     alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                     vertical_alignment=ft.CrossAxisAlignment.START,
                                     controls=[
                                         ft.Column(
                                             spacing=10,
                                             controls=[
                                                 ft.Text(
                                                     "Campaña Agrícola",
                                                     color="white",
                                                     weight=ft.FontWeight.BOLD
                                                 ),
                                                 selector_campana,
                                             ]
                                         ),

                                         ft.VerticalDivider(width=1),

                                         ft.Column(
                                             spacing=10,
                                             controls=[
                                                 ft.Text(
                                                     "Tipo de Cultivo",
                                                     color="white",
                                                     weight=ft.FontWeight.BOLD
                                                 ),

                                                 ft.RadioGroup(
                                                     value="invernal",
                                                     on_change=cambiar_cultivo,
                                                     content=ft.Column(
                                                         spacing=10,
                                                         controls=[
                                                             ft.Radio(
                                                                 value="invernal",
                                                                 label="🌾 Invernal",
                                                                 fill_color="#22C55E"
                                                             ),
                                                             ft.Radio(
                                                                 value="estival",
                                                                 label="🌽 Estival",
                                                                 fill_color="#F59E0B"
                                                             )
                                                         ]
                                                     )
                                                 )
                                             ]
                                         )
                                     ]
                                 )
                             ]
                         )
                     ),
                    
                        
                    #ft.Container(height=30),
                    cultivo_texto,
                    ft.Container(height=10),
                    # BOTÓN EMPEZAR
                    #boton_principal(
                     #"EMPEZAR CLASIFICACIÓN",
                      #   lambda e: navigate_to(page, "/upload"),
                       #  ft.Icons.PLAY_ARROW
                       #)    
                    
                    ]
                )
            )
        ]
    )