"""Topics screen — subject cards with mastery bars."""
import flet as ft
from theme import (BLUE, BLUE_50, WHITE, DARK, GRAY, GREEN, GREEN_50,
                   ORANGE, ORANGE_50, APP_BG, FONT_DISPLAY, SUBJECTS)
import components as comp


def build(page: ft.Page, state) -> ft.View:

    def subject_card(subj):
        pct = state.subject_mastery_pct(subj)
        acc = state.subject_accuracy(subj)
        lesson_done = state.subject_state(subj).get("lesson_done", False)
        from data.questions import by_subject
        item_count = len(by_subject(subj))
        acc_txt = f"{int(acc*100)}% accuracy" if acc is not None else "Not attempted yet"
        pct_txt = f"{int(pct*100)}% mastery"

        status_color = GREEN if pct >= 0.8 else (ORANGE if pct >= 0.4 else BLUE)
        status_bg = GREEN_50 if pct >= 0.8 else (ORANGE_50 if pct >= 0.4 else BLUE_50)

        def go(_):
            state.current_subject = subj
            page.go("/lesson")

        row_items = [
            ft.Row([
                ft.Icon(ft.Icons.CHECK_ROUNDED if lesson_done else ft.Icons.MENU_BOOK_ROUNDED,
                        color=GREEN if lesson_done else GRAY, size=14),
                ft.Text("Lesson", size=12,
                        color=GREEN if lesson_done else GRAY,
                        weight=ft.FontWeight.W_500),
            ], spacing=4),
            ft.Row([
                ft.Icon(ft.Icons.MENU_BOOK_ROUNDED,
                        color=GREEN if item_count > 0 else GRAY, size=14),
                ft.Text(f"{item_count} items", size=12,
                        color=GREEN if item_count > 0 else GRAY,
                        weight=ft.FontWeight.W_500),
            ], spacing=4),
        ]

        return ft.GestureDetector(
            content=comp.card(
                ft.Column(
                    [
                        ft.Row(
                            [
                                comp.subject_icon(subj, size=44),
                                ft.Column(
                                    [
                                        ft.Text(subj, size=15,
                                                weight=ft.FontWeight.W_700,
                                                color=DARK),
                                        ft.Text(acc_txt, size=12, color=GRAY),
                                    ],
                                    spacing=2, expand=True,
                                ),
                                comp.badge_pill(
                                    pct_txt, status_bg, status_color,
                                ),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=12),
                        comp.progress_bar(pct),
                        ft.Container(height=10),
                        ft.Row(row_items, spacing=16),
                    ],
                ),
                shadow_on=True,
            ),
            on_tap=go,
        )

    controls = [
        ft.Container(height=4),
        ft.Text("Reviewer", size=22, weight=ft.FontWeight.W_800,
                color=DARK, font_family=FONT_DISPLAY),
        ft.Text("Tap a subject to start learning.", size=13, color=GRAY),
        ft.Container(height=16),
        *[ft.Column([subject_card(s), ft.Container(height=10)])
          for s in SUBJECTS],
        ft.Container(height=8),
    ]

    return comp.screen_scaffold(
        page, controls, active_route="/topics",
        scroll=True, padding=20,
    )
