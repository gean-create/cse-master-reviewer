"""Home Dashboard — Professional CSE Reviewer 2026."""
import flet as ft
import random
from theme import (NAVY, BLUE, BLUE_50, BLUE_100, GOLD, GOLD_50,
                   WHITE, APP_BG, GRAY, GRAY_SOFT, GREEN, GREEN_50,
                   RED, RED_50, ORANGE, ORANGE_50, BORDER,
                   SUBJECTS, PASSING_SCORE)
import components as comp
from subscription_service import get_trial_status
from data.questions import by_subject


def build(page: ft.Page, state) -> ft.View:
    name = state.name.split()[0] if state.name else "Reviewer"
    track = state.track
    readiness = state.readiness_score()
    streak = state.streak_count
    total_q = state.total_questions_answered()
    sub = get_trial_status(state.data)

    # ── Header ──────────────────────────────────────────────────
    import datetime as dt
    hour = dt.datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"

    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(f"{greeting},", size=14, color=WHITE + "BB"),
                    ft.Text(name + "! 👋", size=22,
                            weight=ft.FontWeight.W_800, color=WHITE,
                            font_family="Georgia"),
                ], spacing=0, expand=True),
                ft.Container(
                    content=ft.Image(
                        src="assets/icon.png",
                        width=48, height=48,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    border_radius=ft.BorderRadius.all(24),
                    bgcolor=WHITE + "22",
                    padding=ft.Padding.all(4),
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=4),
            comp.badge_pill(
                f"📋 {track} Level",
                WHITE + "22", WHITE, size=12,
            ),
        ], spacing=6),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[BLUE, NAVY],
        ),
        padding=ft.Padding.only(left=20, right=20, top=50, bottom=24),
        border_radius=ft.BorderRadius.only(
            bottom_left=28, bottom_right=28),
    )

    # ── Subscription banner ──────────────────────────────────────
    if sub["trial_expired"] and not sub["is_premium"]:
        sub_banner = ft.GestureDetector(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.STAR_ROUNDED, color=WHITE, size=18),
                    ft.Text("Upgrade to Premium — ₱150/year",
                            size=13, weight=ft.FontWeight.W_700,
                            color=WHITE, expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED,
                            color=WHITE, size=18),
                ], spacing=10),
                bgcolor=RED,
                border_radius=ft.BorderRadius.all(12),
                padding=ft.Padding.symmetric(horizontal=14, vertical=12),
            ),
            on_tap=lambda _: page.go("/upgrade"),
        )
    elif sub["on_trial"]:
        days = sub["trial_days_left"]
        sub_banner = ft.GestureDetector(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.HOURGLASS_TOP_ROUNDED,
                            color=BLUE, size=16),
                    ft.Text(
                        f"Free trial: {days} day{'s' if days != 1 else ''} left",
                        size=12, color=BLUE, expand=True),
                    ft.Text("Upgrade ₱150/yr →", size=11,
                            color=BLUE, weight=ft.FontWeight.W_700),
                ], spacing=8),
                bgcolor=BLUE_50,
                border_radius=ft.BorderRadius.all(10),
                padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                border=ft.Border.all(1, BLUE_100),
            ),
            on_tap=lambda _: page.go("/upgrade"),
        )
    else:
        sub_banner = ft.Container()

    # ── Readiness Card ───────────────────────────────────────────
    pct = int(readiness * 100)
    passed = readiness >= PASSING_SCORE
    readiness_card = comp.gradient_card(
        ft.Row([
            ft.Column([
                ft.Text("Overall Readiness", size=12,
                        color=WHITE + "BB"),
                ft.Text(
                    "Exam Ready! 🎉" if passed else f"{pct}% Ready",
                    size=26, weight=ft.FontWeight.W_900,
                    color=WHITE, font_family="Georgia",
                ),
                ft.Text(
                    f"Target: {int(PASSING_SCORE*100)}% to pass the CSE",
                    size=11, color=WHITE + "BB",
                ),
                ft.Container(height=8),
                comp.progress_bar(
                    readiness,
                    color=GOLD,
                    bgcolor=WHITE + "22",
                    height=6,
                ),
            ], spacing=4, expand=True),
            ft.Container(width=16),
            comp.ring(
                readiness, size=80, stroke=7,
                fill_color=GOLD,
                track_color=WHITE + "22",
                label_size=16,
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

    # ── Stats Row ────────────────────────────────────────────────
    def stat_box(value, label, color=BLUE, bg=BLUE_50):
        return ft.Container(
            content=ft.Column([
                ft.Text(str(value), size=22,
                        weight=ft.FontWeight.W_800,
                        color=color, font_family="Georgia"),
                ft.Text(label, size=10, color=GRAY,
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2),
            bgcolor=bg, expand=True,
            border_radius=ft.BorderRadius.all(14),
            padding=ft.Padding.symmetric(horizontal=8, vertical=12),
            shadow=comp.shadow(blur=4, opacity=0.05),
        )

    overall_acc = state.overall_accuracy()
    acc_txt = f"{int(overall_acc*100)}%" if overall_acc else "—"

    stats_row = ft.Row([
        stat_box(acc_txt, "Accuracy", BLUE, BLUE_50),
        stat_box(str(total_q), "Questions", "#7C3AED", "#F3F0FF"),
        stat_box(f"{streak}🔥", "Day Streak", ORANGE, ORANGE_50),
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

    def start_exam(_):
        page.go("/exam_config")

    daily_btn = ft.GestureDetector(
        content=ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.BOLT_ROUNDED,
                                    color=WHITE, size=22),
                    bgcolor=GOLD,
                    border_radius=ft.BorderRadius.all(12),
                    padding=ft.Padding.all(10),
                ),
                ft.Column([
                    ft.Text("Daily Challenge", size=14,
                            weight=ft.FontWeight.W_700, color=NAVY),
                    ft.Text("10 mixed questions • ~8 min",
                            size=11, color=GRAY),
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
        on_tap=start_daily,
    )

    exam_btn = ft.GestureDetector(
        content=ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.ASSIGNMENT_ROUNDED,
                                    color=WHITE, size=22),
                    bgcolor=NAVY,
                    border_radius=ft.BorderRadius.all(12),
                    padding=ft.Padding.all(10),
                ),
                ft.Column([
                    ft.Text("Full Mock Exam", size=14,
                            weight=ft.FontWeight.W_700, color=NAVY),
                    ft.Text(
                        "170 items • 3h 10m (Professional)" if track == "Professional"
                        else "165 items • 2h 40m (Sub-Pro)",
                        size=11, color=GRAY,
                    ),
                ], spacing=2, expand=True),
                comp.badge_pill("Premium", GOLD_50, GOLD,
                                size=10) if not sub["can_access_premium"]
                else ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED,
                             color=GRAY_SOFT, size=20),
            ], spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=WHITE,
            border_radius=ft.BorderRadius.all(16),
            padding=ft.Padding.all(16),
            shadow=comp.shadow(),
        ),
        on_tap=start_exam,
    )

    # ── Subject Grid ─────────────────────────────────────────────
    def subj_card(subj):
        pct = state.subject_mastery_pct(subj)
        acc = state.subject_accuracy(subj)
        acc_txt = f"{int(acc*100)}%" if acc is not None else "New"
        color = comp.SUBJECT_COLORS.get(subj, BLUE)

        def go(_):
            state.current_subject = subj
            page.go("/topics")

        return ft.GestureDetector(
            content=ft.Container(
                content=ft.Column([
                    comp.subject_icon(subj, size=40),
                    ft.Container(height=8),
                    ft.Text(subj.split()[0], size=11,
                            weight=ft.FontWeight.W_700,
                            color=NAVY,
                            text_align=ft.TextAlign.CENTER),
                    ft.Text(acc_txt, size=13,
                            weight=ft.FontWeight.W_800,
                            color=color,
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=4),
                    comp.progress_bar(pct, color=color,
                                      bgcolor=color + "18",
                                      height=4),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2),
                bgcolor=WHITE,
                border_radius=ft.BorderRadius.all(16),
                padding=ft.Padding.all(14),
                shadow=comp.shadow(blur=6, opacity=0.06),
                expand=True,
            ),
            on_tap=go,
            expand=True,
        )

    subj_grid = ft.Column([
        ft.Row(
            [subj_card(SUBJECTS[0]), subj_card(SUBJECTS[1])],
            spacing=12,
        ),
        ft.Row(
            [subj_card(SUBJECTS[2]), subj_card(SUBJECTS[3])],
            spacing=12,
        ),
    ], spacing=12)

    def section(title):
        return ft.Text(title, size=15,
                       weight=ft.FontWeight.W_800, color=NAVY)

    controls = [
        header,
        ft.Container(
            content=ft.Column([
                ft.Container(height=4),
                sub_banner,
                ft.Container(height=12) if sub["on_trial"] or
                    (sub["trial_expired"] and not sub["is_premium"])
                    else ft.Container(height=0),
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
                section("Subjects"),
                ft.Container(height=10),
                subj_grid,
                ft.Container(height=20),
            ], spacing=0),
            padding=ft.Padding.all(20),
        ),
    ]

    return ft.View(
        route="/home",
        controls=[
            ft.Column([
                ft.Container(
                    content=ft.Column(controls, spacing=0,
                                      scroll=ft.ScrollMode.AUTO),
                    expand=True,
                ),
                comp.bottom_nav(page, "/home"),
            ], spacing=0, expand=True),
        ],
        padding=0,
        bgcolor=APP_BG,
    )
