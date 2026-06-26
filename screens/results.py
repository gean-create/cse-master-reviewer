"""Results screen."""
import flet as ft
from data.questions import get as get_q  # BUG FIX #5 — proper import, no __import__ hack
from theme import (BLUE, BLUE_50, WHITE, DARK, GRAY, GREEN, GREEN_50,
                   RED, RED_50, ORANGE, ORANGE_50, APP_BG,
                   FONT_DISPLAY, PASSING_SCORE, SUBJECTS)
import components as comp


def build(page: ft.Page, state) -> ft.View:
    result = getattr(state, "last_result", {}) or {}
    correct = result.get("correct", 0)
    total = result.get("total", 1)
    breakdown = result.get("breakdown", {})
    mode = result.get("mode", "practice")
    track = result.get("track", "")
    duration_sec = result.get("duration_sec", 0)

    score_pct = correct / max(total, 1)
    passed = score_pct >= PASSING_SCORE   # BUG FIX #4: both are 0.0–1.0 floats now
    is_exam = mode == "exam"

    # ── Score card ───────────────────────────────────────────────
    score_card = comp.gradient_card(
        ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Mock Exam" if is_exam else "Quiz Result",
                            size=12, color=WHITE + "BB"),
                    ft.Text(
                        "PASSED!" if (passed and is_exam) else
                        "FAILED" if (not passed and is_exam) else
                        f"{int(score_pct * 100)}%",
                        size=38, weight=ft.FontWeight.W_800,
                        color=WHITE, font_family=FONT_DISPLAY,
                    ),
                    ft.Text(f"{correct} / {total} correct",
                            size=13, color=WHITE + "CC"),
                ], spacing=2, expand=True),
                comp.ring(score_pct, size=90, stroke=8,
                          fill_color=WHITE, track_color=WHITE + "33", label_size=17),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=12),
            ft.Row([
                comp.badge_pill(
                    "✓ Passed!" if passed else f"Need {int(PASSING_SCORE*100)}% to pass",
                    WHITE + "22", WHITE,
                    icon=ft.Icons.CHECK_ROUNDED if passed else ft.Icons.WARNING_AMBER_ROUNDED,
                ),
                ft.Container(expand=True),
                # Show duration for exams
                ft.Text(
                    f"⏱ {duration_sec // 60}m {duration_sec % 60}s" if is_exam and duration_sec else "",
                    size=11, color=WHITE + "BB",
                ) if is_exam else ft.Container(),
            ]),
        ]),
        colors=[GREEN + "CC", "#16a34a"] if passed else None,
    )

    # ── Breakdown ────────────────────────────────────────────────
    def breakdown_row(label, data):
        c = data.get("correct", 0)
        t = data.get("total", 0)
        pct = c / max(t, 1)
        color = GREEN if pct >= PASSING_SCORE else (ORANGE if pct >= 0.5 else RED)
        return ft.Column([
            ft.Row([
                ft.Text(label, size=12, color=DARK,
                        weight=ft.FontWeight.W_600, expand=True),
                ft.Text(f"{c}/{t}", size=12, color=GRAY),
            ]),
            comp.progress_bar(pct, color=color),
        ], spacing=4)

    breakdown_items = []
    for s in SUBJECTS:
        if s in breakdown:
            breakdown_items += [breakdown_row(s, breakdown[s]), ft.Container(height=6)]
    # also show non-SUBJECTS categories (for Pro exam sub-categories)
    for cat, data in breakdown.items():
        if cat not in SUBJECTS and breakdown_items is not None:
            breakdown_items += [breakdown_row(cat, data), ft.Container(height=6)]

    breakdown_card = (comp.card(ft.Column([
        ft.Text("Subject Breakdown", size=14, weight=ft.FontWeight.W_700, color=DARK),
        ft.Container(height=12),
        *breakdown_items,
    ])) if breakdown_items else ft.Container())

    # ── Actions ──────────────────────────────────────────────────
    def on_review(_):
        if not state.can_access_premium():
            page.show_dialog(ft.AlertDialog(
                title=ft.Text("Premium Feature", weight=ft.FontWeight.W_700),
                content=ft.Text("Wrong answer review is a Premium feature.\nUpgrade for ₱150/year.", size=13),
                actions=[
                    comp.ghost_button("Cancel", on_click=lambda _: page.close_dialog()),
                    comp.primary_button("Upgrade", expand=False,
                                        on_click=lambda _: [page.close_dialog(), page.go("/upgrade")]),
                ],
            ))
            return
        page.go("/review")

    def on_retake(_):
        qids = result.get("question_ids", [])
        answers_map = result.get("answers", {})
        # BUG FIX #5: use proper get_q import
        wrong_ids = [qid for qid in qids
                     if answers_map.get(qid) != (get_q(qid) or {}).get("answer")]
        state.active_question_ids = wrong_ids if wrong_ids else qids
        state.active_mode = "retake"
        page.go("/quiz")

    def on_home(_):
        page.go("/home")

    controls = [
        ft.Container(height=8),
        score_card,
        ft.Container(height=16),
        breakdown_card,
        ft.Container(height=20),
        comp.primary_button("Review Wrong Answers", on_click=on_review,
                            expand=True, icon=ft.Icons.EDIT_NOTE_ROUNDED),
        ft.Container(height=10),
        comp.outline_button("Retake Quiz", on_click=on_retake, expand=True),
        ft.Container(height=10),
        comp.ghost_button("Back to Home", on_click=on_home),
        ft.Container(height=16),
    ]
    return comp.screen_scaffold(page, controls, active_route=None, scroll=True, padding=20)
