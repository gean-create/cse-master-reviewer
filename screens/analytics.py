"""Analytics screen — overall stats, weekly bar chart, strongest/weakest."""
import flet as ft
from theme import (BLUE, BLUE_50, WHITE, DARK, GRAY, GREEN, GREEN_50,
                   RED, RED_50, ORANGE, ORANGE_50, APP_BG,
                   FONT_DISPLAY, PASSING_SCORE, SUBJECTS)
import components as comp


def build(page: ft.Page, state) -> ft.View:
    overall = state.overall_accuracy()
    total_q = state.total_questions_answered()
    streak = state.streak_count
    weekly = state.weekly_activity()
    strongest, weakest = state.strongest_weakest()

    # ── Summary cards ────────────────────────────────────────────
    def stat_pill(label, value, color=BLUE, bg=BLUE_50):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(value, size=22, weight=ft.FontWeight.W_800,
                            color=color, font_family=FONT_DISPLAY),
                    ft.Text(label, size=11, color=GRAY),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            bgcolor=bg,
            border_radius=ft.BorderRadius.all(14),
            padding=ft.Padding.symmetric(horizontal=12, vertical=14),
            expand=True,
        )

    acc_txt = f"{int(overall*100)}%" if overall is not None else "—"
    stats_row = ft.Row(
        [
            stat_pill("Accuracy", acc_txt,
                      GREEN if (overall or 0) >= PASSING_SCORE else BLUE,
                      GREEN_50 if (overall or 0) >= PASSING_SCORE else BLUE_50),
            stat_pill("Questions", str(total_q)),
            stat_pill("Streak", f"{streak}d", ORANGE, ORANGE_50),
        ],
        spacing=10,
    )

    # ── Weekly bar chart ─────────────────────────────────────────
    max_count = max((c for _, c in weekly), default=1) or 1
    bar_max_h = 80

    bars = []
    for day, count in weekly:
        h = max(4, int(count / max_count * bar_max_h)) if count else 4
        bars.append(
            ft.Column(
                [
                    ft.Text(str(count) if count else "", size=10, color=GRAY),
                    ft.Container(
                        width=28, height=h,
                        bgcolor=BLUE if count else BLUE_50 + "88",
                        border_radius=ft.BorderRadius.only(
                            top_left=4, top_right=4),
                    ),
                    ft.Text(day, size=10, color=GRAY),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            )
        )

    chart_card = comp.card(
        ft.Column(
            [
                ft.Text("This Week", size=14, weight=ft.FontWeight.W_700,
                        color=DARK),
                ft.Container(height=12),
                ft.Row(
                    bars,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
        ),
    )

    # ── Subject breakdown ────────────────────────────────────────
    def subj_row(s):
        acc = state.subject_accuracy(s)
        pct = state.subject_mastery_pct(s)
        acc_txt = f"{int(acc*100)}%" if acc is not None else "—"
        bar_color = (GREEN if (acc or 0) >= PASSING_SCORE else
                     ORANGE if (acc or 0) >= 0.5 else RED)
        return ft.Column(
            [
                ft.Row(
                    [
                        comp.subject_icon(s, size=32),
                        ft.Column(
                            [
                                ft.Text(s, size=12,
                                        weight=ft.FontWeight.W_600,
                                        color=DARK),
                                ft.Text(f"Accuracy: {acc_txt}",
                                        size=11, color=GRAY),
                            ],
                            spacing=0, expand=True,
                        ),
                        ft.Text(f"{int(pct*100)}%", size=14,
                                weight=ft.FontWeight.W_700,
                                color=bar_color),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                comp.progress_bar(pct, color=bar_color, height=5),
            ],
            spacing=6,
        )

    subj_cards = ft.Column(
        [subj_row(s) for s in SUBJECTS],
        spacing=16,
    )

    # ── Strongest / Weakest callout ───────────────────────────────
    def callout(label, pair, bg, color, icon):
        if pair is None:
            return ft.Container()
        subj_name, acc = pair
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color=color, size=20),
                    ft.Column(
                        [
                            ft.Text(label, size=11, color=color,
                                    weight=ft.FontWeight.W_600),
                            ft.Text(subj_name, size=13, color=DARK,
                                    weight=ft.FontWeight.W_700),
                        ],
                        spacing=0, expand=True,
                    ),
                    ft.Text(f"{int(acc*100)}%", size=15,
                            weight=ft.FontWeight.W_800, color=color),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=bg,
            border_radius=ft.BorderRadius.all(12),
            padding=ft.Padding.all(14),
        )

    controls = [
        ft.Container(height=4),
        ft.Text("Analytics", size=22, weight=ft.FontWeight.W_800,
                color=DARK, font_family=FONT_DISPLAY),
        ft.Text("Your study performance overview.", size=13, color=GRAY),
        ft.Container(height=16),
        stats_row,
        ft.Container(height=16),
        chart_card,
        ft.Container(height=16),
        callout("Strongest Subject", strongest,
                GREEN_50, GREEN, ft.Icons.TRENDING_UP_ROUNDED),
        ft.Container(height=8),
        callout("Weakest Subject", weakest,
                RED_50, RED, ft.Icons.WARNING_AMBER_ROUNDED),
        ft.Container(height=20),
        ft.Text("Subject Mastery", size=14, weight=ft.FontWeight.W_700,
                color=DARK),
        ft.Container(height=12),
        comp.card(subj_cards),
        ft.Container(height=16),
    ]

    return comp.screen_scaffold(
        page, controls, active_route="/analytics",
        scroll=True, padding=20,
    )
