# src/main.py
import flet as ft
from src.config.theme import (COLOR_FONDO, COLOR_NEON, COLOR_BOTON, 
                              ANCHO_VENTANA, ALTO_VENTANA)
from src.router.router import navigate_to

def main(page: ft.Page):
    # =====================================================
    # CONFIGURACIÓN DE LA PÁGINA
    # =====================================================
    page.title = "Land Cover Classifier"
    page.window.icon = r"C:\Python\TESIS\app\assets\icons\logo.ico"
    page.window_maximized = True
    page.window_min_width = 1024
    page.window_min_height = 768
    page.update()
    page.bgcolor = "#020817"
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    
    navigate_to(page, "/home")

ft.run(main)