#app/src/router
import flet as ft

from src.views.home_view import pantalla_inicio
from src.views.upload_view import pantalla_upload
from src.views.result_view import pantalla_resultado


def navigate_to(page: ft.Page, route: str):

    page.views.clear()

    if route == "/home":

        page.views.append(
            pantalla_inicio(page, navigate_to)
        )

    elif route == "/upload":

        page.views.append(
            pantalla_upload(page, navigate_to)
        )

    elif route == "/result":

        page.views.append(
            pantalla_resultado(page, navigate_to)
        )

    page.update()

