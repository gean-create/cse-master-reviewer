"""Achievements screen — badge grid, locked vs unlocked."""
import flet as ft
from theme import (BLUE, BLUE_50, BLUE_700, WHITE, DARK, GRAY,
                   GRAY_SOFT, GOLD, APP_BG, FONT_DISPLAY)
import components as comp
from state import ACHIEVEMENT_DEFS


ICON_MAP = {
    "QUIZ_ROUNDED": ft.Icons.QUIZ_ROUNDED,
    "LOCAL_FIRE_DEPARTMENT_ROUNDED": ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED,
    "EMOJI_EVENTS_ROUNDED": ft.Icons.EMOJI_EVENTS_ROUNDED,
    "MILITARY_TECH_ROUNDED": ft.Icons.MILITARY_TECH_ROUNDED,
    "STAR_ROUNDED": ft.Icons.STAR_ROUNDED,
    "ASSIGNMENT_ROUNDED": ft.Icons.ASSIGNMENT_ROUNDED,
    "PUBLIC_ROUNDED": ft.Icons.PUBLIC_ROUNDED,
    "STYLE_ROUNDED": ft.Icons.STYLE_ROUNDED,
}


def build(page: ft.Page, state) -> ft.View:
    unlocked = state.unlocked_achievements()

    def on_back(_):
        page.go("/profile")

    def badge_card(ach):
        aid = ach["id"]
        is_unlocked = aid in unlocked
        icon = ICON_MAP.get(ach.get("icon", ""), ft.Icons.STAR_ROUNDED)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(
                            icon,
                            color=WHITE if is_unlocked else GRAY_SOFT,
                            size=28,
                        ),
                        bgcolor=GOLD if is_unlocked else BLUE_50,
                        border_radius=ft.BorderRadius.all(18),
                        padding=ft.Padding.all(16),
                        opacity=1.0 if is_unlocked else 0.5,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        ach["title"],
                        size=12, weight=ft.FontWeight.W_700,
                        color=DARK if is_unlocked else GRAY_SOFT,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        ach["desc"],
                        size=10, color=GRAY if is_unlocked else GRAY_SOFT,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=4),
                    ft.Icon(
                        ft.Icons.LOCK_OUTLINE_ROUNDED if not is_unlocked
                        else ft.Icons.CHECK_CIRCLE_ROUNDED,
                        color=GRAY_SOFT if not is_unlocked else GOLD,
                        size=14,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            bgcolor=WHITE,
            border_radius=ft.BorderRadius.all(16),
            padding=ft.Padding.all(14),
            border=ft.Border.all(
                2 if is_unlocked else 1,
                GOLD if is_unlocked else BLUE_50,
            ),
            shadow=ft.BoxShadow(
                blur_radius=8,
                color=ft.Colors.with_opacity(0.06, "#000000"),
                offset=ft.Offset(0, 2),
            ) if is_unlocked else None,
        )

    grid = ft.GridView(
        runs_count=2,
        max_extent=200,
        spacing=12,
        run_spacing=12,
    )
    grid.controls = [badge_card(a) for a in ACHIEVEMENT_DEFS]

    unlocked_count = len(unlocked)
    total_count = len(ACHIEVEMENT_DEFS)

    controls = [
        comp.top_bar(page, "Achievements", on_back=on_back),
        ft.Container(height=8),
        ft.Text(
            f"{unlocked_count} / {total_count} unlocked",
            size=13, color=GRAY,
        ),
        ft.Container(height=4),
        comp.progress_bar(unlocked_count / max(total_count, 1), color=GOLD),
        ft.Container(height=20),
        grid,
        ft.Container(height=16),
    ]

    return comp.screen_scaffold(
        page, controls, active_route=None,
        scroll=True, padding=20,
    )
