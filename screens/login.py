"""Login — local profile creation (no backend auth)."""
import flet as ft
from theme import (BLUE, BLUE_50, WHITE, DARK, GRAY, GRAY_SOFT,
                   APP_BG, RED, FONT_DISPLAY, BORDER)
import components as comp


TRACKS = ["Professional", "Sub-Professional"]


def build(page: ft.Page, state) -> ft.View:
    selected_track = [TRACKS[0]]
    error_ref = ft.Ref[ft.Text]()

    name_field = ft.TextField(
        label="Your Full Name",
        hint_text="e.g. Juan Dela Cruz",
        border_color=BORDER,
        focused_border_color=BLUE,
        border_radius=ft.BorderRadius.all(12),
        bgcolor=WHITE,
        color=DARK,
        label_style=ft.TextStyle(color=GRAY),
        cursor_color=BLUE,
    )

    def track_chip(t):
        selected = t == selected_track[0]
        return ft.GestureDetector(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.CHECK_ROUNDED if selected else ft.Icons.RADIO_BUTTON_UNCHECKED_OUTLINED,
                            color=BLUE if selected else GRAY_SOFT,
                            size=18,
                        ),
                        ft.Text(t, size=14,
                                color=BLUE if selected else GRAY,
                                weight=ft.FontWeight.W_600 if selected else ft.FontWeight.W_400),
                    ],
                    spacing=8,
                ),
                bgcolor=BLUE_50 if selected else WHITE,
                border=ft.Border.all(2 if selected else 1,
                                     BLUE if selected else BORDER),
                border_radius=ft.BorderRadius.all(12),
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            ),
            on_tap=lambda _, tr=t: _select_track(tr),
        )

    track_row = ft.Row(spacing=12)

    def _select_track(t):
        selected_track[0] = t
        track_row.controls = [track_chip(tr) for tr in TRACKS]
        page.update()

    track_row.controls = [track_chip(tr) for tr in TRACKS]

    def on_start(_):
        name = name_field.value.strip() if name_field.value else ""
        if not name:
            error_ref.current.value = "Please enter your name."
            error_ref.current.visible = True
            page.update()
            return
        error_ref.current.visible = False
        state.create_profile(name, selected_track[0])
        state.start_trial_if_new()
        page.go("/home")

    header = ft.Column(
        [
            ft.Container(
                content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=WHITE, size=36),
                bgcolor=BLUE,
                border_radius=ft.BorderRadius.all(20),
                padding=ft.Padding.all(20),
            ),
            ft.Container(height=20),
            ft.Text("Welcome!", size=28, weight=ft.FontWeight.W_800,
                    color=DARK, font_family=FONT_DISPLAY),
            ft.Text("Set up your reviewer profile\nto get started.",
                    size=14, color=GRAY, text_align=ft.TextAlign.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4,
    )

    error_text = ft.Text("", color=RED, size=12, ref=error_ref, visible=False)

    form = ft.Column(
        [
            ft.Text("Full Name", size=13, weight=ft.FontWeight.W_600, color=DARK),
            name_field,
            ft.Container(height=8),
            ft.Text("Exam Track", size=13, weight=ft.FontWeight.W_600, color=DARK),
            track_row,
            error_text,
        ],
        spacing=8,
    )

    body = ft.Container(
        content=ft.Column(
            [
                ft.Container(expand=True),
                header,
                ft.Container(height=36),
                form,
                ft.Container(height=24),
                comp.primary_button("Start Reviewing", on_click=on_start,
                                    expand=True, icon=ft.Icons.ARROW_FORWARD_ROUNDED),
                ft.Container(expand=True),
            ],
            expand=True,
        ),
        padding=ft.Padding.all(28),
        expand=True,
        bgcolor=APP_BG,
    )

    return ft.View(
        route="/login",
        controls=[body],
        padding=0,
        bgcolor=APP_BG,
    )
