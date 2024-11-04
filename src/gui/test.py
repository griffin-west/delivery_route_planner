import flet as ft

from title_bar import TitleBar

def main(page: ft.Page):

    page.bgcolor = ft.colors.SURFACE_VARIANT

    title_bar = TitleBar()

ft.app(main)