"""Mock Exam — real CSE simulation with accurate timer, question navigator, flag system."""
import flet as ft
import asyncio
import random
from theme import (BLUE, BLUE_50, WHITE, DARK, GRAY, GREEN, GREEN_50,
                   RED, RED_50, ORANGE, APP_BG, BORDER, FONT_DISPLAY,
                   SUBJECTS, NAVY)
import components as comp
from data.questions import by_subject, get as get_q

# Fallback config if exam_config screen is skipped
DEFAULT_CONFIG = {
    "track": "Professional",
    "total": 40,
    "duration_min": 40,
    "categories": [(s, 10) for s in SUBJECTS],
}


def build(page: ft.Page, state) -> ft.View:
    cfg = getattr(state, "exam_config", None) or DEFAULT_CONFIG
    track = cfg.get("track", "Professional")
    duration_sec = cfg.get("duration_min", 40) * 60

    # Build question pool from available questions (scales with your bank)
    all_ids = []
    for subj in SUBJECTS:
        qs = by_subject(subj)
        n = min(cfg.get("total", 40) // len(SUBJECTS), len(qs))
        all_ids += [q["id"] for q in random.sample(qs, n)]
    random.shuffle(all_ids)
    questions = [get_q(qid) for qid in all_ids if get_q(qid)]
    total = len(questions)

    answers = {}
    flagged = set()
    idx = [0]
    time_left = [duration_sec]
    exam_done = [False]
    is_paused = [False]
    # BUG FIX #3: store task reference so we can cancel it on navigate-away
    _tick_task = [None]

    # ── Timer ────────────────────────────────────────────────────
    h0, m0 = divmod(duration_sec // 60, 60)
    timer_text = ft.Text(
        f"{h0:02d}:{m0:02d}:00" if h0 else f"{m0:02d}:00",
        size=15, weight=ft.FontWeight.W_700, color=DARK,
    )

    async def _tick():
        while time_left[0] > 0 and not exam_done[0]:
            await asyncio.sleep(1)
            if exam_done[0]:
                break
            if is_paused[0]:
                continue  # frozen — don't decrement time while paused
            time_left[0] -= 1
            h, rem = divmod(time_left[0], 3600)
            m, s = divmod(rem, 60)
            timer_text.value = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
            timer_text.color = RED if time_left[0] < 300 else DARK
            try:
                page.update()
            except Exception:
                break
        if not exam_done[0]:
            _finish_exam()

    _tick_task[0] = page.run_task(_tick)

    # ── Grid navigator ───────────────────────────────────────────
    def _nav_grid():
        cells = []
        for i, q in enumerate(questions):
            qid = q["id"]
            is_current = i == idx[0]
            is_flagged = qid in flagged
            answered = qid in answers
            if is_current:
                bg, txt_c = BLUE, WHITE
            elif is_flagged:
                bg, txt_c = ORANGE + "44", DARK
            elif answered:
                bg, txt_c = GREEN_50, GREEN
            else:
                bg, txt_c = WHITE, GRAY

            cells.append(ft.GestureDetector(
                content=ft.Container(
                    content=ft.Text(str(i + 1), size=10,
                                    weight=ft.FontWeight.W_700, color=txt_c),
                    bgcolor=bg,
                    border=ft.Border.all(1.5 if is_current else 1,
                                         BLUE if is_current else BORDER),
                    border_radius=ft.BorderRadius.all(6),
                    width=34, height=34,
                    alignment=ft.Alignment(0, 0),
                ),
                on_tap=lambda _, i=i: _jump(i),
            ))
        return cells

    grid_view = ft.GridView(runs_count=10, max_extent=38, spacing=3, run_spacing=3)
    grid_view.controls = _nav_grid()

    # ── Question area ────────────────────────────────────────────
    question_text = ft.Text("", size=15, weight=ft.FontWeight.W_600, color=DARK)
    subject_badge = ft.Text("", size=11, color=BLUE, weight=ft.FontWeight.W_600)
    choices_col = ft.Column(spacing=8)
    progress_text = ft.Text(f"1 / {total}", size=12, color=GRAY)

    def _render():
        q = questions[idx[0]]
        question_text.value = q["question"]
        subject_badge.value = q.get("subject", "")
        progress_text.value = f"{idx[0]+1} / {total}"
        chosen = answers.get(q["id"])
        items = []
        for i, ch in enumerate(q["choices"]):
            sel = chosen == i
            items.append(ft.GestureDetector(
                content=ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text(["A","B","C","D"][i], size=11,
                                            weight=ft.FontWeight.W_700,
                                            color=WHITE if sel else DARK),
                            bgcolor=BLUE if sel else BORDER + "66",
                            border_radius=ft.BorderRadius.all(6),
                            width=26, height=26,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Text(ch, size=13, color=DARK, expand=True),
                    ], spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=BLUE_50 if sel else WHITE,
                    border=ft.Border.all(1.5, BLUE if sel else BORDER),
                    border_radius=ft.BorderRadius.all(12),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                ),
                on_tap=lambda _, ci=i: _select(ci),
            ))
        choices_col.controls = items
        grid_view.controls = _nav_grid()
        page.update()

    def _select(ci):
        q = questions[idx[0]]
        answers[q["id"]] = ci
        _render()

    def _jump(i):
        idx[0] = i
        _render()

    def _on_prev(_):
        if idx[0] > 0:
            idx[0] -= 1
            _render()

    def _on_next(_):
        if idx[0] < total - 1:
            idx[0] += 1
            _render()

    def _on_flag(_):
        q = questions[idx[0]]
        if q["id"] in flagged:
            flagged.discard(q["id"])
        else:
            flagged.add(q["id"])
        _render()

    def _finish_exam():
        if exam_done[0]:
            return
        exam_done[0] = True  # BUG FIX #3: stops the _tick coroutine cleanly
        duration_used = duration_sec - time_left[0]
        # BUG FIX #2: single call — record_exam_attempt grades internally
        correct, total_q, breakdown = state.record_exam_attempt(
            all_ids, answers, duration_used, track=track
        )
        state.last_result = {
            "correct": correct, "total": total_q, "breakdown": breakdown,
            "mode": "exam", "subject": None, "answers": answers,
            "question_ids": all_ids, "track": track,
            "duration_sec": duration_used,
        }
        page.go("/results")

    pause_overlay = ft.Container(visible=False)

    def _build_pause_overlay():
        h, rem = divmod(time_left[0], 3600)
        m, s = divmod(rem, 60)
        time_str = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.PAUSE_CIRCLE_ROUNDED, color=WHITE, size=56),
                ft.Container(height=12),
                ft.Text("Exam Paused", size=20,
                        weight=ft.FontWeight.W_800, color=WHITE),
                ft.Text(f"Time remaining: {time_str}",
                        size=13, color=WHITE + "CC"),
                ft.Container(height=20),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=BLUE, size=18),
                        ft.Text("Resume Exam", size=14,
                                weight=ft.FontWeight.W_700, color=BLUE),
                    ], spacing=6),
                    bgcolor=WHITE,
                    on_click=_on_resume,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=NAVY,
            opacity=0.95,
            alignment=ft.Alignment(0, 0),
            expand=True,
        )

    def _on_pause(_):
        is_paused[0] = True
        pause_overlay.content = _build_pause_overlay()
        pause_overlay.visible = True
        page.update()

    def _on_resume(_):
        is_paused[0] = False
        pause_overlay.visible = False
        page.update()

    def on_submit(_):
        answered = len(answers)
        unanswered = total - answered

        def _confirm(_):
            page.pop_dialog()
            _finish_exam()

        def _cancel(_):
            page.pop_dialog()

        page.show_dialog(ft.AlertDialog(
            title=ft.Text("Submit Exam?", weight=ft.FontWeight.W_700),
            content=ft.Text(
                f"Answered: {answered}/{total}"
                + (f"\nUnanswered: {unanswered}" if unanswered else "")
                + "\n\nYou cannot change answers after submitting.",
                size=14,
            ),
            actions=[
                comp.ghost_button("Cancel", on_click=_cancel),
                comp.cta_button("Submit", on_click=_confirm),
            ],
        ))

    _render()

    h_dur, m_dur = divmod(cfg.get("duration_min", 40), 60)
    dur_label = f"{h_dur}h {m_dur}m" if h_dur else f"{m_dur}m"

    header = ft.Row([
        ft.Column([
            ft.Text(f"CSE {track} Exam", size=15,
                    weight=ft.FontWeight.W_800, color=DARK, font_family=FONT_DISPLAY),
            ft.Row([subject_badge], spacing=4),
        ], spacing=0, expand=True),
        ft.Row([
            ft.Icon(ft.Icons.TIMER_ROUNDED, color=GRAY, size=15),
            timer_text,
        ], spacing=4),
    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

    nav_row = ft.Row([
        ft.IconButton(icon=ft.Icons.CHEVRON_LEFT_ROUNDED, icon_color=BLUE, on_click=_on_prev),
        progress_text,
        ft.IconButton(icon=ft.Icons.PAUSE_ROUNDED, icon_color=GRAY, on_click=_on_pause,
                      tooltip="Pause exam"),
        ft.IconButton(icon=ft.Icons.FLAG_ROUNDED, icon_color=ORANGE, on_click=_on_flag,
                      tooltip="Flag for review"),
        ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT_ROUNDED, icon_color=BLUE, on_click=_on_next),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Legend row
    legend = ft.Row([
        ft.Row([ft.Container(width=12, height=12, bgcolor=BLUE, border_radius=ft.BorderRadius.all(3)),
                ft.Text("Current", size=10, color=GRAY)], spacing=4),
        ft.Row([ft.Container(width=12, height=12, bgcolor=GREEN_50, border_radius=ft.BorderRadius.all(3)),
                ft.Text("Answered", size=10, color=GRAY)], spacing=4),
        ft.Row([ft.Container(width=12, height=12, bgcolor=ORANGE+"44", border_radius=ft.BorderRadius.all(3)),
                ft.Text("Flagged", size=10, color=GRAY)], spacing=4),
    ], spacing=12)

    view_body = ft.Container(
        content=ft.Column([
            header,
            ft.Divider(height=1, color=BORDER),
            ft.Container(height=4),
            ft.Text("Navigator", size=10, weight=ft.FontWeight.W_600, color=GRAY),
            grid_view,
            legend,
            ft.Container(height=4),
            nav_row,
            ft.Divider(height=1, color=BORDER),
            ft.Container(height=8),
            question_text,
            ft.Container(height=12),
            choices_col,
            ft.Container(height=20),
            comp.cta_button("Submit Exam", on_click=on_submit, expand=True),
            ft.Container(height=16),
        ], scroll=ft.ScrollMode.AUTO, expand=True),
        padding=ft.Padding.all(16),
        expand=True,
    )

    return ft.View(
        route="/mock_exam",
        controls=[ft.Stack([view_body, pause_overlay], expand=True)],
        padding=0, bgcolor=APP_BG)
