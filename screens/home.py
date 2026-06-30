"""Home Dashboard — Professional, free, with exam countdown."""
import flet as ft
import datetime as dt
import asyncio
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

    # ── Exam Countdown (live H:M:S) ───────────────────────────────
    upcoming_exams = get_upcoming_exams(3)
    next_exam = upcoming_exams[0] if upcoming_exams else None

    countdown_days_txt = ft.Text("0", size=28, weight=ft.FontWeight.W_900, color=WHITE)
    countdown_hrs_txt = ft.Text("00", size=20, weight=ft.FontWeight.W_800, color=WHITE)
    countdown_min_txt = ft.Text("00", size=20, weight=ft.FontWeight.W_800, color=WHITE)
    countdown_sec_txt = ft.Text("00", size=20, weight=ft.FontWeight.W_800, color=WHITE)

    if next_exam:
        exam_dt = dt.datetime.combine(
            dt.date.fromisoformat(next_exam["date"]),
            dt.time(8, 0)  # 8:00 AM test proper start
        )

        async def _tick_countdown():
            while True:
                remaining = exam_dt - dt.datetime.now()
                if remaining.total_seconds() <= 0:
                    countdown_days_txt.value = "0"
                    countdown_hrs_txt.value = "00"
                    countdown_min_txt.value = "00"
                    countdown_sec_txt.value = "00"
                    try:
                        page.update()
                    except Exception:
                        pass
                    break
                total_sec = int(remaining.total_seconds())
                days, rem = divmod(total_sec, 86400)
                hours, rem = divmod(rem, 3600)
                minutes, seconds = divmod(rem, 60)
                countdown_days_txt.value = str(days)
                countdown_hrs_txt.value = f"{hours:02d}"
                countdown_min_txt.value = f"{minutes:02d}"
                countdown_sec_txt.value = f"{seconds:02d}"
                try:
                    page.update()
                except Exception:
                    break
                await asyncio.sleep(1)

        page.run_task(_tick_countdown)

        exam_date = dt.date.fromisoformat(next_exam["date"])
        exam_date_str = exam_date.strftime("%B %d, %Y")
        days_left = days_until_exam(next_exam)

        countdown_color = (RED if days_left <= 7 else
                           ORANGE if days_left <= 30 else BLUE)

        def time_box(value_ctrl, label):
            return ft.Container(
                content=ft.Column([
                    value_ctrl,
                    ft.Text(label, size=9, color=WHITE + "AA"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0),
                bgcolor=WHITE + "18",
                border_radius=ft.BorderRadius.all(10),
                padding=ft.Padding.symmetric(horizontal=10, vertical=8),
                width=58,
            )

        def go_schedule(_):
            page.go("/schedule")

        countdown_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.EVENT_AVAILABLE_ROUNDED,
                            color=WHITE, size=16),
                    ft.Text("Upcoming Civil Service Examination",
                            size=12, color=WHITE + "CC",
                            weight=ft.FontWeight.W_600),
                ], spacing=6),
                ft.Container(height=4),
                ft.Text(exam_date_str, size=18,
                        weight=ft.FontWeight.W_800, color=WHITE),
                ft.Text(next_exam["label"] + " — " + next_exam["description"],
                        size=11, color=WHITE + "BB"),
                ft.Container(height=12),
                ft.Row([
                    time_box(countdown_days_txt, "DAYS"),
                    time_box(countdown_hrs_txt, "HOURS"),
                    time_box(countdown_min_txt, "MINS"),
                    time_box(countdown_sec_txt, "SECS"),
                ], spacing=8),
                ft.Container(height=12),
                ft.GestureDetector(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Text("View Complete Schedule", size=12,
                                    weight=ft.FontWeight.W_700, color=WHITE),
                            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED,
                                    color=WHITE, size=14),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                        bgcolor=WHITE + "20",
                        border_radius=ft.BorderRadius.all(10),
                        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    ),
                    on_tap=go_schedule,
                ),
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
