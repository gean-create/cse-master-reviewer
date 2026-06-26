"""Profile screen — user stats, settings, logout."""
import flet as ft
from theme import (BLUE, BLUE_50, BLUE_700, WHITE, DARK, GRAY,
                   GOLD, RED, RED_50, APP_BG, FONT_DISPLAY, BORDER)
import components as comp


def build(page: ft.Page, state) -> ft.View:
    name = state.name or "Reviewer"
    track = (state.data.get("profile") or {}).get("track", "Professional")
    readiness = state.readiness_score()
    total_q = state.total_questions_answered()
    streak = state.streak_count

    # ── Avatar & name ─────────────────────────────────────────────
    initials = "".join(w[0].upper() for w in name.split()[:2])

    avatar_card = comp.gradient_card(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.CircleAvatar(
                            content=ft.Text(initials, size=22,
                                            weight=ft.FontWeight.W_700,
                                            color=BLUE),
                            bgcolor=WHITE,
                            radius=36,
                        ),
                        ft.Column(
                            [
                                ft.Text(name, size=18,
                                        weight=ft.FontWeight.W_700,
                                        color=WHITE,
                                        font_family=FONT_DISPLAY),
                                comp.badge_pill(
                                    track, WHITE + "22", WHITE,
                                    icon=ft.Icons.MILITARY_TECH_ROUNDED,
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
        ),
    )

    # ── Stats row ────────────────────────────────────────────────
    def stat_box(label, val, color=BLUE, bg=BLUE_50):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(val, size=20, weight=ft.FontWeight.W_800,
                            color=color, font_family=FONT_DISPLAY),
                    ft.Text(label, size=10, color=GRAY),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            bgcolor=bg, expand=True,
            border_radius=ft.BorderRadius.all(14),
            padding=ft.Padding.symmetric(horizontal=8, vertical=12),
        )

    stats = ft.Row(
        [
            stat_box("Readiness", f"{int(readiness*100)}%"),
            stat_box("Questions", str(total_q), BLUE, BLUE_50),
            stat_box("Streak", f"{streak}d",
                     ft.Colors.ORANGE_700, "#FEF3E2"),
        ],
        spacing=10,
    )

    # ── Settings list ────────────────────────────────────────────
    def settings_item(icon, label, on_tap, color=DARK, bg_icon=BLUE_50, icon_color=BLUE):
        return ft.GestureDetector(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(icon, color=icon_color, size=20),
                            bgcolor=bg_icon,
                            border_radius=ft.BorderRadius.all(10),
                            padding=ft.Padding.all(8),
                        ),
                        ft.Text(label, size=14, color=color,
                                weight=ft.FontWeight.W_500, expand=True),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED,
                                color=GRAY, size=18),
                    ],
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=WHITE,
                border_radius=ft.BorderRadius.all(12),
                padding=ft.Padding.symmetric(horizontal=14, vertical=12),
            ),
            on_tap=on_tap,
        )

    def go_achievements(_):
        page.go("/achievements")

    def go_analytics(_):
        page.go("/analytics")

    def on_reset(_):
        def _confirm(_):
            page.close_dialog()
            state.reset_progress()
            state.save_bg()
            page.go("/home")

        def _cancel(_):
            page.close_dialog()

        dlg = ft.AlertDialog(
            title=ft.Text("Reset Progress?", weight=ft.FontWeight.W_700),
            content=ft.Text(
                "All quiz history, mastery scores, and streak data will be erased. "
                "Your profile name will be kept.",
                size=13,
            ),
            actions=[
                comp.ghost_button("Cancel", on_click=_cancel),
                comp.cta_button("Reset", on_click=_confirm),
            ],
        )
        page.show_dialog(dlg)

    def on_logout(_):
        def _confirm(_):
            page.close_dialog()
            state.log_out()
            state.save_bg()
            page.go("/login")

        def _cancel(_):
            page.close_dialog()

        dlg = ft.AlertDialog(
            title=ft.Text("Log Out?", weight=ft.FontWeight.W_700),
            content=ft.Text("Your profile will be removed from this device.", size=13),
            actions=[
                comp.ghost_button("Cancel", on_click=_cancel),
                comp.cta_button("Log Out", on_click=_confirm),
            ],
        )
        page.show_dialog(dlg)

    settings = ft.Column(
        [
            settings_item(ft.Icons.EMOJI_EVENTS_ROUNDED,
                          "Achievements", go_achievements,
                          icon_color=GOLD, bg_icon="#FEF9EC"),
            ft.Container(height=8),
            settings_item(ft.Icons.BAR_CHART_ROUNDED,
                          "Analytics", go_analytics),
            ft.Container(height=8),
            settings_item(ft.Icons.REFRESH_ROUNDED,
                          "Reset Progress", on_reset,
                          color=ft.Colors.ORANGE_700,
                          bg_icon="#FEF3E2",
                          icon_color=ft.Colors.ORANGE_700),
            ft.Container(height=8),
            settings_item(ft.Icons.LOGOUT_ROUNDED,
                          "Log Out", on_logout,
                          color=RED, bg_icon=RED_50, icon_color=RED),
        ],
    )

    controls = [
        ft.Container(height=4),
        avatar_card,
        ft.Container(height=12),
        stats,
        ft.Container(height=24),
        ft.Text("Settings", size=14, weight=ft.FontWeight.W_700, color=DARK),
        ft.Container(height=10),
        settings,
        ft.Container(height=20),
        ft.Text("CSE Master Reviewer v1.0",
                size=11, color=GRAY,
                text_align=ft.TextAlign.CENTER),
        ft.Container(height=16),
    ]

    return comp.screen_scaffold(
        page, controls, active_route="/profile",
        scroll=True, padding=20,
    )
