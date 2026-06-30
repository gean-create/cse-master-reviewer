"""
CSC Exam Schedule — Timeline view of past and upcoming exams.
Auto-calculated from official CSC pattern (2nd Sunday of March & August).
"""
import flet as ft
import datetime as dt
from theme import (NAVY, BLUE, BLUE_50, GOLD, GOLD_50, WHITE, APP_BG,
                   GRAY, GRAY_SOFT, BORDER, GREEN, GREEN_50, RED, RED_50, ORANGE)
import components as comp
from free_config import get_exam_schedule, days_until_exam


def build(page: ft.Page, state) -> ft.View:
    today = dt.date.today()
    all_exams = get_exam_schedule(years_ahead=2)

    def on_back(_):
        page.go("/home")

    def status_badge(exam):
        exam_date = dt.date.fromisoformat(exam["date"])
        days = (exam_date - today).days
        if days < 0:
            return comp.badge_pill("COMPLETED", GRAY_SOFT + "22", GRAY_SOFT,
                                   icon=ft.Icons.CHECK_CIRCLE_ROUNDED)
        elif days == 0:
            return comp.badge_pill("TODAY", RED_50, RED,
                                   icon=ft.Icons.NOTIFICATIONS_ACTIVE_ROUNDED)
        elif days <= 30:
            return comp.badge_pill("REGISTRATION CLOSING SOON", ORANGE + "22", ORANGE,
                                   icon=ft.Icons.WARNING_AMBER_ROUNDED)
        else:
            return comp.badge_pill("UPCOMING", BLUE_50, BLUE,
                                   icon=ft.Icons.SCHEDULE_ROUNDED)

    def exam_row(exam, is_last=False):
        exam_date = dt.date.fromisoformat(exam["date"])
        app_start = dt.date.fromisoformat(exam["application_start"])
        app_end = dt.date.fromisoformat(exam["application_end"])
        is_past = exam_date < today
        dot_color = GRAY_SOFT if is_past else (
            RED if (exam_date - today).days <= 30 else BLUE)

        return ft.Row([
            # Timeline rail
            ft.Column([
                ft.Container(
                    width=14, height=14,
                    bgcolor=dot_color,
                    border_radius=ft.BorderRadius.all(7),
                    border=ft.Border.all(3, WHITE),
                    shadow=ft.BoxShadow(blur_radius=4,
                                        color=dot_color + "66"),
                ),
                ft.Container(
                    width=2, height=110,
                    bgcolor=BORDER,
                ) if not is_last else ft.Container(width=2, height=0),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            ft.Container(width=12),
            # Card
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(exam_date.strftime("%B %d, %Y"),
                                size=15, weight=ft.FontWeight.W_800,
                                color=NAVY if not is_past else GRAY_SOFT),
                        ft.Container(expand=True),
                        status_badge(exam),
                    ]),
                    ft.Text(exam["label"], size=12, color=GRAY,
                            weight=ft.FontWeight.W_600),
                    ft.Text(exam["description"], size=11, color=GRAY_SOFT),
                    ft.Container(height=8),
                    ft.Row([
                        ft.Icon(ft.Icons.EDIT_CALENDAR_ROUNDED,
                                color=GRAY_SOFT, size=13),
                        ft.Text(
                            f"Apply: {app_start.strftime('%b %d')} – {app_end.strftime('%b %d, %Y')}",
                            size=11, color=GRAY,
                        ),
                    ], spacing=6),
                    ft.Row([
                        ft.Icon(ft.Icons.DESCRIPTION_ROUNDED,
                                color=GRAY_SOFT, size=13),
                        ft.Text("Mode: Paper and Pencil Test (CSE-PPT)",
                                size=11, color=GRAY),
                    ], spacing=6),
                ], spacing=3),
                bgcolor=WHITE,
                border=ft.Border.all(1, BORDER),
                border_radius=ft.BorderRadius.all(14),
                padding=ft.Padding.all(14),
                expand=True,
                opacity=0.55 if is_past else 1.0,
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.START)

    timeline_items = []
    for i, exam in enumerate(all_exams):
        timeline_items.append(exam_row(exam, is_last=(i == len(all_exams) - 1)))
        timeline_items.append(ft.Container(height=4))

    info_card = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_ROUNDED, color=BLUE, size=16),
            ft.Text(
                "Schedule is auto-calculated using the CSC's official pattern: "
                "2nd Sunday of March and 2nd Sunday of August each year. "
                "Always confirm exact dates at csc.gov.ph.",
                size=11, color=GRAY, expand=True,
            ),
        ], spacing=8),
        bgcolor=BLUE_50,
        border_radius=ft.BorderRadius.all(10),
        padding=ft.Padding.all(12),
    )

    controls = [
        comp.top_bar(page, "CSC Exam Schedule", on_back=on_back,
                    subtitle="Professional & Sub-Professional CSE-PPT"),
        ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=12),
                    info_card,
                    ft.Container(height=16),
                    ft.Text("Timeline", size=14,
                            weight=ft.FontWeight.W_800, color=NAVY),
                    ft.Container(height=12),
                    *timeline_items,
                    ft.Container(height=20),
                ],
                scroll=ft.ScrollMode.AUTO, expand=True,
            ),
            padding=ft.Padding.all(20),
            expand=True,
        ),
    ]

    return ft.View(
        route="/schedule",
        controls=[ft.Column(controls, spacing=0, expand=True)],
        padding=0,
        bgcolor=APP_BG,
    )
