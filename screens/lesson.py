"""Lesson screen — structured lesson content per subject."""
import flet as ft
from theme import (BLUE, BLUE_50, WHITE, DARK, GRAY, GREEN,
                   APP_BG, FONT_DISPLAY, BORDER)
import components as comp
from data.lessons import LESSONS


def build(page: ft.Page, state) -> ft.View:
    subj = state.current_subject
    lesson = LESSONS.get(subj, {})

    def on_continue(_):
        state.mark_lesson_done(subj)
        state.save_bg()
        page.go("/flashcards")

    def on_back(_):
        page.go("/topics")

    points = lesson.get("points", [])
    point_items = [
        ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.CHECK_ROUNDED,
                                    color=WHITE, size=12),
                    bgcolor=BLUE,
                    border_radius=ft.BorderRadius.all(10),
                    width=22, height=22,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Text(pt, size=13, color=DARK, expand=True),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        for pt in points
    ]

    example_box = ft.Container(
        content=ft.Column(
            [
                ft.Text(lesson.get("example_label", "Example"),
                        size=12, weight=ft.FontWeight.W_700, color=BLUE),
                ft.Container(height=4),
                ft.Text(lesson.get("example", ""), size=13, color=DARK),
            ],
        ),
        bgcolor=BLUE_50,
        border_radius=ft.BorderRadius.all(12),
        padding=ft.Padding.all(14),
        border=ft.Border(left=ft.BorderSide(4, BLUE)),
    )

    tip_box = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LIGHTBULB_ROUNDED, color=ft.Colors.AMBER, size=18),
                ft.Text(lesson.get("tip", ""), size=12, color=DARK,
                        expand=True, italic=True),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        bgcolor="#FFFBEA",
        border_radius=ft.BorderRadius.all(10),
        padding=ft.Padding.all(12),
    )

    controls = [
        comp.top_bar(page, lesson.get("title", subj), on_back=on_back),
        ft.Container(height=12),
        comp.subject_icon(subj, size=52),
        ft.Container(height=12),
        ft.Text(lesson.get("title", subj), size=22,
                weight=ft.FontWeight.W_800, color=DARK,
                font_family=FONT_DISPLAY),
        ft.Container(height=8),
        ft.Text(lesson.get("intro", ""), size=14, color=GRAY),
        ft.Container(height=20),
        ft.Text("Key Points", size=14, weight=ft.FontWeight.W_700, color=DARK),
        ft.Container(height=8),
        ft.Column(point_items, spacing=10),
        ft.Container(height=20),
        example_box,
        ft.Container(height=12),
        tip_box,
        ft.Container(height=28),
        comp.primary_button(
            "Continue to Flashcards",
            on_click=on_continue,
            expand=True,
            icon=ft.Icons.ARROW_FORWARD_ROUNDED,
        ),
        ft.Container(height=16),
    ]

    return comp.screen_scaffold(
        page, controls, active_route=None,
        scroll=True, padding=20,
    )
