"""Splash screen — auto-navigates after 1.5 s."""
import asyncio
import flet as ft
from theme import BLUE, BLUE_700, WHITE, GOLD, FONT_DISPLAY


def build(page: ft.Page, state) -> ft.View:

    async def _navigate():
        await asyncio.sleep(1.5)
        if not state.onboarded:
            page.go("/onboarding")
        elif not state.is_logged_in:
            page.go("/login")
        else:
            page.go("/home")

    page.run_task(_navigate)

    logo = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("CSE", size=36, weight=ft.FontWeight.W_800,
                                    color=WHITE, font_family=FONT_DISPLAY),
                    bgcolor=WHITE + "22",
                    border_radius=ft.BorderRadius.all(20),
                    padding=ft.Padding.symmetric(horizontal=24, vertical=16),
                ),
                ft.Container(height=16),
                ft.Text("Master Reviewer", size=22, weight=ft.FontWeight.W_700,
                        color=WHITE, font_family=FONT_DISPLAY),
                ft.Text("Philippine Civil Service Exam", size=13,
                        color=WHITE + "BB"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        alignment=ft.Alignment(0, 0),
    )

    spinner = ft.ProgressRing(
        width=28, height=28,
        stroke_width=3,
        color=GOLD,
        bgcolor=WHITE + "33",
    )

    body = ft.Container(
        content=ft.Column(
            [logo, ft.Container(height=60), spinner],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[BLUE, BLUE_700],
        ),
        expand=True,
        alignment=ft.Alignment(0, 0),
    )

    return ft.View(
        route="/splash",
        controls=[body],
        padding=0,
        bgcolor=BLUE,
    )
