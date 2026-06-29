"""Splash screen with Civil Service Reviewer 2026 branding."""
import asyncio
import flet as ft
from theme import NAVY, BLUE, GOLD, WHITE, BLUE_50


def build(page: ft.Page, state) -> ft.View:

    async def _navigate():
        await asyncio.sleep(2.0)
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
                # Logo image
                ft.Container(
                    content=ft.Image(
                        src="assets/icon.png",
                        width=160,
                        height=160,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    border_radius=ft.BorderRadius.all(24),
                ),
                ft.Container(height=24),
                ft.Text(
                    "CIVIL SERVICE",
                    size=28, weight=ft.FontWeight.W_900,
                    color=WHITE,
                    text_align=ft.TextAlign.CENTER,
                    font_family="Georgia",
                ),
                ft.Text(
                    "REVIEWER",
                    size=20, weight=ft.FontWeight.W_700,
                    color=GOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=4),
                ft.Row(
                    [
                        ft.Container(width=40, height=2, bgcolor=GOLD + "66"),
                        ft.Text("2026", size=16, weight=ft.FontWeight.W_700,
                                color=GOLD),
                        ft.Container(width=40, height=2, bgcolor=GOLD + "66"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        alignment=ft.Alignment(0, 0),
    )

    body = ft.Container(
        content=ft.Column(
            [
                ft.Container(expand=True),
                logo,
                ft.Container(expand=True),
                ft.ProgressRing(
                    width=24, height=24,
                    stroke_width=3,
                    color=GOLD,
                    bgcolor=WHITE + "22",
                ),
                ft.Container(height=8),
                ft.Text(
                    "Powered by CSC-accredited content",
                    size=11, color=WHITE + "66",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=40),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        bgcolor=NAVY,
        expand=True,
    )

    return ft.View(
        route="/splash",
        controls=[body],
        padding=0,
        bgcolor=NAVY,
    )
