"""Onboarding — 3 slides with dot pagination."""
import flet as ft
from theme import (BLUE, BLUE_50, WHITE, DARK, GRAY, APP_BG,
                   FONT_DISPLAY, RED, GREEN)
import components as comp


SLIDES = [
    {
        "icon": ft.Icons.SCHOOL_ROUNDED,
        "color": BLUE,
        "title": "Study Smarter",
        "body": ("Master all four CSE subjects with structured lessons, "
                 "a Brainbox-style reviewer book, and timed practice quizzes."),
    },
    {
        "icon": ft.Icons.TRENDING_UP_ROUNDED,
        "color": GREEN,
        "title": "Track Your Progress",
        "body": ("See your readiness score grow, spot your weak areas, "
                 "and keep your daily streak alive."),
    },
    {
        "icon": ft.Icons.EMOJI_EVENTS_ROUNDED,
        "color": RED,
        "title": "Pass the Exam",
        "body": ("Simulate the real Civil Service Exam with a timed "
                 "mock test and get detailed results instantly."),
    },
]


def build(page: ft.Page, state) -> ft.View:
    idx = [0]          # mutable container so closures can mutate

    # ── Dot indicators ──────────────────────────────────────────
    def dots():
        return ft.Row(
            [
                ft.Container(
                    width=24 if i == idx[0] else 8,
                    height=8,
                    border_radius=ft.BorderRadius.all(4),
                    bgcolor=BLUE if i == idx[0] else BLUE_50,
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                )
                for i in range(len(SLIDES))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        )

    # ── Slide content ───────────────────────────────────────────
    def slide_card(s):
        return ft.Column(
            [
                ft.Container(
                    content=ft.Icon(s["icon"], color=WHITE, size=56),
                    bgcolor=s["color"],
                    border_radius=ft.BorderRadius.all(32),
                    padding=ft.Padding.all(32),
                    shadow=ft.BoxShadow(
                        blur_radius=24,
                        color=ft.Colors.with_opacity(0.25, s["color"]),
                        offset=ft.Offset(0, 8),
                    ),
                ),
                ft.Container(height=32),
                ft.Text(s["title"], size=26, weight=ft.FontWeight.W_800,
                        color=DARK, font_family=FONT_DISPLAY,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=12),
                ft.Text(s["body"], size=14, color=GRAY,
                        text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    slide_col = ft.Column(
        [slide_card(SLIDES[0])],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    dot_row_ref = ft.Ref[ft.Row]()

    dot_container = ft.Container(content=dots(), ref=dot_row_ref)

    def refresh():
        slide_col.controls = [slide_card(SLIDES[idx[0]])]
        dot_container.content = dots()
        page.update()

    def on_next(_):
        if idx[0] < len(SLIDES) - 1:
            idx[0] += 1
            refresh()
        else:
            _finish()

    def on_skip(_):
        _finish()

    def _finish():
        state.onboarded = True
        state.save_bg()
        page.go("/login")

    next_btn = comp.primary_button(
        "Next", on_click=on_next, expand=True,
        icon=ft.Icons.ARROW_FORWARD_ROUNDED,
    )

    skip_btn = comp.ghost_button("Skip", on_click=on_skip)

    body = ft.Container(
        content=ft.Column(
            [
                ft.Row([skip_btn], alignment=ft.MainAxisAlignment.END),
                ft.Container(expand=True, content=slide_col,
                             alignment=ft.Alignment(0, 0)),
                dot_container,
                ft.Container(height=24),
                next_btn,
                ft.Container(height=16),
            ],
            expand=True,
        ),
        padding=ft.Padding.all(24),
        expand=True,
        bgcolor=APP_BG,
    )

    return ft.View(
        route="/onboarding",
        controls=[body],
        padding=0,
        bgcolor=APP_BG,
    )
