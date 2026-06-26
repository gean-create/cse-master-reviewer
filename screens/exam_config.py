"""Exam Config — choose Professional or Sub-Professional before starting exam."""
import flet as ft
from theme import (BLUE, BLUE_50, BLUE_700, WHITE, DARK, GRAY, RED,
                   RED_50, APP_BG, FONT_DISPLAY, BORDER)
import components as comp

CONFIGS = {
    "Professional": {
        "track": "Professional",
        "total": 170,
        "duration_min": 190,
        "categories": [
            ("Vocabulary", 20),
            ("Grammar & Correct Usage", 20),
            ("Reading Comprehension", 10),
            ("Word Analogy", 10),
            ("Numerical Ability", 20),
            ("Word Problems", 10),
            ("Data Interpretation", 10),
            ("Logical Reasoning", 20),
            ("Philippine Constitution", 15),
            ("RA 6713 / Code of Conduct", 10),
            ("Human Rights", 10),
            ("Environmental Management", 15),
        ],
    },
    "Sub-Professional": {
        "track": "Sub-Professional",
        "total": 165,
        "duration_min": 160,
        "categories": [
            ("Vocabulary", 20),
            ("Grammar & Correct Usage", 20),
            ("Reading Comprehension", 10),
            ("Numerical Ability", 25),
            ("Filing", 20),
            ("Coding", 20),
            ("Records Management", 15),
            ("Office Procedures", 15),
            ("General Information", 20),
        ],
    },
}


def build(page: ft.Page, state) -> ft.View:
    selected = [state.track if state.track in CONFIGS else "Professional"]
    allow_back = [True]

    def on_back(_):
        page.go("/home")

    def select(track):
        selected[0] = track
        page.update()

    def on_start(_):
        # Premium gate — mock exam is premium only
        if not state.can_access_premium():
            page.show_dialog(ft.AlertDialog(
                title=ft.Text("Premium Feature", weight=ft.FontWeight.W_700),
                content=ft.Text(
                    "The full mock exam requires a Premium account.\n\n"
                    "Upgrade for ₱150/year — less than ₱13/month!",
                    size=13,
                ),
                actions=[
                    comp.ghost_button("Cancel", on_click=lambda _: page.pop_dialog()),
                    comp.primary_button("Upgrade Now", expand=False,
                                        on_click=lambda _: [page.pop_dialog(), page.go("/upgrade")]),
                ],
            ))
            return
        cfg = CONFIGS[selected[0]]
        state.exam_config = cfg
        state.active_mode = "exam"
        page.go("/mock_exam")

    def track_card(track):
        cfg = CONFIGS[track]
        is_sel = track == selected[0]
        h, m = divmod(cfg["duration_min"], 60)
        dur_txt = f"{h}h {m}m" if m else f"{h}h"

        return ft.GestureDetector(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.MILITARY_TECH_ROUNDED if track == "Professional"
                                else ft.Icons.SCHOOL_ROUNDED,
                                color=WHITE if is_sel else BLUE, size=24),
                            bgcolor=BLUE if is_sel else BLUE_50,
                            border_radius=ft.BorderRadius.all(12),
                            padding=ft.Padding.all(10),
                        ),
                        ft.Column([
                            ft.Text(track, size=16, weight=ft.FontWeight.W_700,
                                    color=WHITE if is_sel else DARK),
                            ft.Text(f"{cfg['total']} items • {dur_txt}",
                                    size=12, color=(WHITE + "CC") if is_sel else GRAY),
                        ], spacing=2, expand=True),
                        ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED if is_sel
                                else ft.Icons.RADIO_BUTTON_UNCHECKED_OUTLINED,
                                color=WHITE if is_sel else GRAY, size=22),
                    ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Container(height=12),
                    ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_ROUNDED,
                                    color=WHITE if is_sel else BLUE, size=12),
                            ft.Text(f"{cat} — {n} items", size=11,
                                    color=(WHITE + "DD") if is_sel else GRAY),
                        ], spacing=6)
                        for cat, n in cfg["categories"]
                    ], spacing=4),
                ]),
                bgcolor=BLUE if is_sel else WHITE,
                border=ft.Border.all(2 if is_sel else 1, BLUE if is_sel else BORDER),
                border_radius=ft.BorderRadius.all(16),
                padding=ft.Padding.all(18),
                shadow=ft.BoxShadow(blur_radius=16,
                                    color=ft.Colors.with_opacity(0.18 if is_sel else 0.06, BLUE),
                                    offset=ft.Offset(0, 4)),
            ),
            on_tap=lambda _, t=track: select(t),
        )

    backtrack_toggle = [True]

    def toggle_back(_):
        backtrack_toggle[0] = not backtrack_toggle[0]
        page.update()

    notice = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_ROUNDED, color=BLUE, size=16),
            ft.Text("This simulation mirrors the actual CSC exam format.",
                    size=12, color=GRAY, expand=True),
        ], spacing=8),
        bgcolor=BLUE_50,
        border_radius=ft.BorderRadius.all(10),
        padding=ft.Padding.all(12),
    )

    controls = [
        comp.top_bar(page, "Choose Exam Track", on_back=on_back),
        ft.Container(height=8),
        ft.Text("Select your Civil Service Exam level.", size=13, color=GRAY),
        ft.Container(height=20),
        track_card("Professional"),
        ft.Container(height=12),
        track_card("Sub-Professional"),
        ft.Container(height=20),
        notice,
        ft.Container(height=28),
        comp.cta_button("Start Exam", on_click=on_start, expand=True),
        ft.Container(height=16),
    ]
    return comp.screen_scaffold(page, controls, active_route=None, scroll=True, padding=20)
