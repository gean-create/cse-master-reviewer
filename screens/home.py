"""Home Dashboard — Professional, free, with exam countdown."""
import flet as ft
import datetime as dt
import random
from theme import (NAVY, BLUE, BLUE_50, BLUE_100, GOLD, GOLD_50,
                   WHITE, APP_BG, GRAY, GRAY_SOFT, GREEN, GREEN_50,
                   RED, RED_50, ORANGE, ORANGE_50, BORDER,
                   SUBJECTS, PASSING_SCORE)
import components as comp
from free_config import get_upcoming_exams, get_next_exam, days_until_exam
from data.questions import by_subject


def build(page: ft.Page, state) -> ft.View:
    name = state.name.split()[0] if state.name else "Reviewer"
    track = state.track
    readiness = state.readiness_score()
    streak = state.streak_count
    total_q = state.total_questions_answered()

    hour = dt.datetime.now().hour
    greeting = ("Magandang umaga" if hour < 12
                else "Magandang hapon" if hour < 17
                else "Magandang gabi")

    # ── Header ──────────────────────────────────────────────────
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(f"{greeting},", size=13, color=WHITE + "BB"),
                    ft.Text(f"{name}! 👋", size=22,
                            weight=ft.FontWeight.W_800, color=WHITE),
                ], spacing=0, expand=True),
                ft.Container(
                    content=ft.Image(
                        src="assets/icon.png", width=44, height=44,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    border_radius=ft.BorderRadius.all(22),
                    bgcolor=WHITE + "22",
                    padding=ft.Padding.all(3),
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=6),
            ft.Row([
                comp.badge_pill(f"📋 {track}", WHITE + "22", WHITE, size=11),
                ft.Container(width=8),
                comp.badge_pill("🆓 100% Free", WHITE + "22", WHITE, size=11),
            ]),
        ], spacing=4),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1),
            colors=[BLUE, NAVY],
        ),
        padding=ft.Padding.only(left=20, right=20, top=52, bottom=24),
        border_radius=ft.BorderRadius.only(
            bottom_left=28, bottom_right=28),
    )

    # ── Exam Countdown ───────────────────────────────────────────
    upcoming_exams = get_upcoming_exams(3)
    next_exam = upcoming_exams[0] if upcoming_exams else None

    if next_exam:
        days_left = days_until_exam(next_exam)
        exam_date = dt.date.fromisoformat(next_exam["date"])
        exam_date_str = exam_date.strftime("%B %d, %Y")

        if days_left == 0:
            countdown_color = RED
        elif days_left <= 7:
            countdown_color = RED
        elif days_left <= 30:
            countdown_color = ORANGE
        else:
            countdown_color = BLUE

        # Mini pills for next 2 exams
        def exam_pill(exam):
            d = days_until_exam(exam)
            ex_date = dt.date.fromisoformat(exam["date"])
            return ft.Container(
                content=ft.Column([
                    ft.Text(ex_date.strftime("%b %d, %Y"),
                            size=11, weight=ft.FontWeight.W_700,
                            color=WHITE),
                    ft.Text(f"{d} days", size=10,
                            color=WHITE + "BB"),
                ], spacing=1,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=WHITE + "18",
                border_radius=ft.BorderRadius.all(8),
                padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            )

        future_pills = ft.Row(
            [exam_pill(e) for e in upcoming_exams[1:3]],
            spacing=8,
        ) if len(upcoming_exams) > 1 else ft.Container()

        countdown_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("📅 Next CSE Exam", size=11,
                                color=WHITE + "BB"),
                        ft.Text(exam_date_str, size=17,
                                weight=ft.FontWeight.W_800,
                                color=WHITE),
                        ft.Text(next_exam["label"], size=11,
                                color=WHITE + "BB"),
                    ], spacing=2, expand=True),
                    ft.Column([
                        ft.Text(str(days_left), size=36,
                                weight=ft.FontWeight.W_900,
                                color=WHITE),
                        ft.Text("days left", size=10,
                                color=WHITE + "BB"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.Row([
                    ft.Text("Upcoming:", size=10, color=WHITE + "88"),
                    future_pills,
                ], spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ]),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1),
                colors=[countdown_color, countdown_color + "CC"],
            ),
            border_radius=ft.BorderRadius.all(16),
            padding=ft.Padding.all(16),
            shadow=comp.shadow(blur=12, opacity=0.15),
        )
    else:
        countdown_card = ft.Container()

    # ── Readiness Card ───────────────────────────────────────────
    pct = int(readiness * 100)
    passed = readiness >= PASSING_SCORE

    readiness_card = comp.gradient_card(
        ft.Row([
            ft.Column([
                ft.Text("Readiness Score", size=12, color=WHITE + "BB"),
                ft.Text(
                    "Exam Ready! 🎉" if passed else f"{pct}% Ready",
                    size=22, weight=ft.FontWeight.W_900,
                    color=WHITE,
                ),
                ft.Container(height=4),
                ft.Text(
                    "Keep it up! You can pass the CSE." if passed
                    else f"Target: {int(PASSING_SCORE*100)}% to pass",
                    size=11, color=WHITE + "BB",
                ),
                ft.Container(height=8),
                comp.progress_bar(readiness, color=GOLD,
                                  bgcolor=WHITE + "22", height=6),
            ], spacing=2, expand=True),
            ft.Container(width=12),
            comp.ring(readiness, size=75, stroke=7,
                      fill_color=GOLD, track_color=WHITE + "22",
                      label_size=15),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

    # ── Stats ────────────────────────────────────────────────────
    overall_acc = state.overall_accuracy()
    acc_txt = f"{int(overall_acc*100)}%" if overall_acc else "—"

    stats_row = ft.Row([
        _stat(acc_txt, "Accuracy", BLUE, BLUE_50),
        _stat(str(total_q), "Questions", "#7C3AED", "#F3F0FF"),
        _stat(f"{streak}🔥", "Streak", ORANGE, ORANGE_50),
    ], spacing=10)

    # ── Quick Actions ────────────────────────────────────────────
    def start_daily(_):
        ids = []
        for s in SUBJECTS:
            qs = by_subject(s)
            ids += [q["id"] for q in random.sample(qs, min(3, len(qs)))]
        random.shuffle(ids)
        state.active_question_ids = ids[:10]
        state.active_mode = "daily"
        state.current_subject = None
        page.go("/quiz")

    daily_btn = _action_card(
        ft.Icons.BOLT_ROUNDED, GOLD, NAVY,
        "Daily Challenge",
        "10 mixed questions • ~8 min",
        start_daily,
    )

    exam_btn = _action_card(
        ft.Icons.ASSIGNMENT_ROUNDED, NAVY, WHITE,
        "Full Mock Exam",
        ("170 items • 3h 10m" if track == "Professional"
         else "165 items • 2h 40m"),
        lambda _: page.go("/exam_config"),
    )

    # ── Subject Grid ─────────────────────────────────────────────
    subj_grid = ft.Column([
        ft.Row([_subj_card(SUBJECTS[0], state, page),
                _subj_card(SUBJECTS[1], state, page)], spacing=12),
        ft.Row([_subj_card(SUBJECTS[2], state, page),
                _subj_card(SUBJECTS[3], state, page)], spacing=12),
    ], spacing=12)

    def section(t):
        return ft.Text(t, size=15, weight=ft.FontWeight.W_800, color=NAVY)

    content = ft.Column([
        ft.Container(height=8),
        countdown_card,
        ft.Container(height=12) if next_exam else ft.Container(height=0),
        readiness_card,
        ft.Container(height=16),
        stats_row,
        ft.Container(height=20),
        section("Quick Actions"),
        ft.Container(height=10),
        daily_btn,
        ft.Container(height=10),
        exam_btn,
        ft.Container(height=20),
        section("Study by Subject"),
        ft.Container(height=10),
        subj_grid,
        ft.Container(height=24),
        ft.Text(
            "Civil Service Reviewer 2026 — 100% Free for all Filipinos 🇵🇭",
            size=11, color=GRAY_SOFT,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Container(height=20),
    ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

    return ft.View(
        route="/home",
        controls=[ft.Column([
            header,
            ft.Container(
                content=content,
                padding=ft.Padding.all(20),
                expand=True,
            ),
            comp.bottom_nav(page, "/home"),
        ], spacing=0, expand=True)],
        padding=0,
        bgcolor=APP_BG,
    )


def _stat(value, label, color, bg):
    return ft.Container(
        content=ft.Column([
            ft.Text(str(value), size=20, weight=ft.FontWeight.W_800,
                    color=color),
            ft.Text(label, size=10, color=GRAY,
                    text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        bgcolor=bg, expand=True,
        border_radius=ft.BorderRadius.all(14),
        padding=ft.Padding.symmetric(horizontal=8, vertical=12),
        shadow=comp.shadow(blur=4, opacity=0.05),
    )


def _action_card(icon, icon_bg, icon_color, title, subtitle, on_tap):
    return ft.GestureDetector(
        content=ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=icon_color, size=22),
                    bgcolor=icon_bg,
                    border_radius=ft.BorderRadius.all(12),
                    padding=ft.Padding.all(10),
                ),
                ft.Column([
                    ft.Text(title, size=14, weight=ft.FontWeight.W_700,
                            color=NAVY),
                    ft.Text(subtitle, size=11, color=GRAY),
                ], spacing=2, expand=True),
                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED,
                        color=GRAY_SOFT, size=20),
            ], spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=WHITE,
            border_radius=ft.BorderRadius.all(16),
            padding=ft.Padding.all(16),
            shadow=comp.shadow(),
        ),
        on_tap=on_tap,
    )


def _subj_card(subj, state, page):
    from theme import SUBJECT_COLORS
    pct = state.subject_mastery_pct(subj)
    acc = state.subject_accuracy(subj)
    acc_txt = f"{int(acc*100)}%" if acc is not None else "New"
    color = SUBJECT_COLORS.get(subj, BLUE)

    def go(_):
        state.current_subject = subj
        page.go("/topics")

    return ft.GestureDetector(
        content=ft.Container(
            content=ft.Column([
                comp.subject_icon(subj, size=38),
                ft.Container(height=6),
                ft.Text(subj.split()[0], size=11,
                        weight=ft.FontWeight.W_700, color=NAVY,
                        text_align=ft.TextAlign.CENTER),
                ft.Text(acc_txt, size=13, weight=ft.FontWeight.W_800,
                        color=color,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=4),
                comp.progress_bar(pct, color=color,
                                  bgcolor=color + "18", height=4),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2),
            bgcolor=WHITE,
            border_radius=ft.BorderRadius.all(16),
            padding=ft.Padding.all(12),
            shadow=comp.shadow(blur=6, opacity=0.06),
            expand=True,
        ),
        on_tap=go,
        expand=True,
    )
