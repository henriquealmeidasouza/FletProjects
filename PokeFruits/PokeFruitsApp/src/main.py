import flet as ft
from view import MainScreen


def main(page: ft.Page):
    page.title = "PokeFruits"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False
    page.add(MainScreen())


if __name__ == "__main__":
    ft.run(main)
