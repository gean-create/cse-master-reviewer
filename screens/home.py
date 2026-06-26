"""Home screen — dashboard with readiness ring, streak, quick actions."""
import flet as ft
from theme import (BLUE, BLUE_50, BLUE_700, RED, RED_50, WHITE, DARK,
                   GRAY, GOLD, ORANGE, ORANGE_50, GREEN, GREEN_50,
                   APP_BG, BORDER, FONT_DISPLAY, PASSING_SCORE, SUBJECTS)
import components as comp
from data.questions import by_subject
import random


def build(page: ft.Page, state) -> ft.View:
    name = state.name or "Reviewer"
    readiness = state.readiness_score()
    streak = state.streak_count

    # ── Greeting header ─────────────────────────────────────────
    greeting = ft.Column(
        [
            ft.Text(f"Hello, {name.split()[0]}! 👋",
                    size=22, weight=ft.FontWeight.W_800,
                    color=DARK, font_family=FONT_DISPLAY),
            ft.Text("Let's keep studying today.", size=13, color=GRAY),
        ],
        spacing=2,
    )

    # ── Readiness card ──────────────────────────────────────────
    pct_label = f"{int(readiness * 100)}%"
    readiness_card = comp.gradient_card(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Readiness Score", size=13,
                                color=WHITE + "CC"),
                        ft.Text(pct_label, size=42,
                                weight=ft.FontWeight.W_800,
                                color=WHITE, font_family=FONT_DISPLAY),
                        ft.Text(
                            "You're exam-ready!" if readiness >= PASSING_SCORE
                            else f"Target: {int(PASSING_SCORE*100)}% to pass",
                            size=12, color=WHITE + "BB",
                        ),
                    ],
                    spacing=2, expand=True,
                ),
                comp.ring(readiness, size=90, stroke=8,
                          fill_color=WHITE,
                          track_color=WHITE + "33",
                          label_size=18),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # ── Streak pill ─────────────────────────────────────────────
    streak_card = comp.card(
        ft.Row(
            [
                ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED,
                        color=ORANGE, size=28),
                ft.Column(
                    [
                        ft.Text(f"{streak}-Day Streak",
                                size=15, weight=ft.FontWeight.W_700,
                                color=DARK),
                        ft.Text("Keep it going!", size=11, color=GRAY),
                    ],
                    spacing=0,
                ),
            ],
            spacing=12,
        ),
        bgcolor=ORANGE_50,
    )

    # ── Quick action: Daily Challenge ───────────────────────────
    def start_daily(_):
        # Random 10-question mix across all subjects
        ids = []
        for subj in SUBJECTS:
            qs = by_subject(subj)
            ids += [q["id"] for q in random.sample(qs, min(3, len(qs)))]
        random.shuffle(ids)
        state.active_question_ids = ids[:10]
        state.active_mode = "daily"
        state.current_subject = None
        page.go("/quiz")

    daily_card = comp.card(
        ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.BOLT_ROUNDED,
                                    color=WHITE, size=24),
                    bgcolor=RED,
                    border_radius=ft.BorderRadius.all(12),
                    padding=ft.Padding.all(10),
                ),
                ft.Column(
                    [
                        ft.Text("Daily Challenge", size=15,
                                weight=ft.FontWeight.W_700, color=DARK),
                        ft.Text("10 mixed questions • ~8 min",
                                size=11, color=GRAY),
                    ],
                    spacing=2, expand=True,
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=GRAY),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        on_click=start_daily,
    )

    # ── Quick action: Mock Exam ──────────────────────────────────
    def start_exam(_):
        page.go("/exam_config")

    exam_card = comp.card(
        ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.ASSIGNMENT_ROUNDED,
                                    color=WHITE, size=24),
                    bgcolor=BLUE,
                    border_radius=ft.BorderRadius.all(12),
                    padding=ft.Padding.all(10),
                ),
                ft.Column(
                    [
                        ft.Text("Mock Exam", size=15,
                                weight=ft.FontWeight.W_700, color=DARK),
                        ft.Text("40 questions • 40 min timed",
                                size=11, color=GRAY),
                    ],
                    spacing=2, expand=True,
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=GRAY),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        on_click=start_exam,
    )

    # ── Subject mini-cards ───────────────────────────────────────
    def mini_subject(subj):
        acc = state.subject_accuracy(subj)
        pct = state.subject_mastery_pct(subj)
        acc_txt = f"{int(acc*100)}%" if acc is not None else "—"

        def go(_):
            state.current_subject = subj
            page.go("/topics")

        return ft.GestureDetector(
            content=ft.Container(
                content=ft.Column(
                    [
                        comp.subject_icon(subj, size=36),
                        ft.Container(height=8),
                        ft.Text(subj.split()[0], size=11,
                                weight=ft.FontWeight.W_600, color=DARK),
                        ft.Text(acc_txt, size=13,
                                weight=ft.FontWeight.W_700, color=BLUE),
                        comp.progress_bar(pct, height=4),
                    ],
                    spacing=3,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=WHITE,
                border_radius=ft.BorderRadius.all(14),
                padding=ft.Padding.all(12),
                shadow=ft.BoxShadow(blur_radius=8,
                                    color=ft.Colors.with_opacity(0.06, "#000000"),
                                    offset=ft.Offset(0, 2)),
            ),
            on_tap=go,
            expand=True,
        )

    subjects_row = ft.Row(
        [mini_subject(s) for s in SUBJECTS],
        spacing=10,
    )

    section = lambda title: ft.Text(
        title, size=14, weight=ft.FontWeight.W_700, color=DARK
    )

    controls = [
        ft.Container(height=8),
        greeting,
        ft.Container(height=16),
        readiness_card,
        ft.Container(height=12),
        streak_card,
        ft.Container(height=20),
        section("Quick Actions"),
        ft.Container(height=8),
        daily_card,
        ft.Container(height=8),
        exam_card,
        ft.Container(height=20),
        section("Subjects"),
        ft.Container(height=8),
        subjects_row,
        ft.Container(height=16),
    ]

    return comp.screen_scaffold(
        page, controls, active_route="/home",
        scroll=True, padding=20,
    )
