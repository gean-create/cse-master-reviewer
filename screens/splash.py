"""Splash screen — white background with logo, always checks login."""
import asyncio
import flet as ft
from theme import NAVY, BLUE, GOLD, WHITE, GRAY_SOFT


def build(page: ft.Page, state) -> ft.View:

    async def _navigate():
        await asyncio.sleep(2.0)
        # Always require proper email login — never skip to home
        # only go to home if they have a verified email profile
        profile = state.data.get("profile")
        if not profile or not profile.get("email"):
            # Not properly logged in — always go to login
            if not state.onboarded:
                page.go("/onboarding")
            else:
                page.go("/login")
        else:
            page.go("/home")

    page.run_task(_navigate)

    body = ft.Container(
        content=ft.Column(
            [
                ft.Container(expand=True),
                # Logo on WHITE background — exactly as provided
                ft.Container(
                    content=ft.Image(
                        src="assets/icon.png",
                        width=220,
                        height=220,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(height=32),
                ft.Text(
                    "Your free reviewer for the",
                    size=13,
                    color=GRAY_SOFT,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Philippine Civil Service Exam",
                    size=15,
                    weight=ft.FontWeight.W_700,
                    color=NAVY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(expand=True),
                ft.ProgressRing(
                    width=24, height=24,
                    stroke_width=3,
                    color=GOLD,
                    bgcolor=GOLD + "22",
                ),
                ft.Container(height=8),
                ft.Text(
                    "100% Free for all Filipinos 🇵🇭",
                    size=11,
                    color=GRAY_SOFT,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=48),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        bgcolor=WHITE,
        expand=True,
        padding=ft.Padding.all(40),
    )

    return ft.View(
        route="/splash",
        controls=[body],
        padding=0,
        bgcolor=WHITE,
    )
