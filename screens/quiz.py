"""Quiz screen — practice / daily / retake with instant feedback."""
import flet as ft
import random
from theme import (BLUE, BLUE_50, WHITE, DARK, GRAY, GREEN, GREEN_50,
                   RED, RED_50, APP_BG, FONT_DISPLAY, SUBJECTS, BORDER)
import components as comp
from data.questions import by_subject, get as get_q


def build(page: ft.Page, state) -> ft.View:
    mode = getattr(state, "active_mode", "practice")
    subj = state.current_subject

    # Build question list
    if getattr(state, "active_question_ids", None):
        question_ids = state.active_question_ids[:]
    elif subj:
        qs = by_subject(subj)
        question_ids = [q["id"] for q in random.sample(qs, min(8, len(qs)))]
    else:
        ids = []
        for s in SUBJECTS:
            qs = by_subject(s)
            ids += [q["id"] for q in random.sample(qs, min(3, len(qs)))]
        random.shuffle(ids)
        question_ids = ids[:10]

    questions = [get_q(qid) for qid in question_ids if get_q(qid)]
    total = len(questions)

    idx = [0]
    answers = {}
    revealed = [False]

    progress_text = ft.Text(f"1 / {total}", size=12, color=GRAY)
    progress_bar_ctrl = comp.progress_bar(1 / max(total, 1))
    question_text = ft.Text("", size=16, weight=ft.FontWeight.W_600, color=DARK)
    choices_col = ft.Column(spacing=10)
    feedback_col = ft.Column(visible=False)
    next_btn_container = ft.Container(visible=False)

    def _render():
        q = questions[idx[0]]
        progress_text.value = f"{idx[0]+1} / {total}"
        progress_bar_ctrl.value = (idx[0] + 1) / total
        question_text.value = q["question"]
        revealed[0] = False
        feedback_col.visible = False
        next_btn_container.visible = False
        _render_choices(q)
        page.update()

    def _render_choices(q):
        chosen = answers.get(q["id"])
        correct = q["answer"]
        items = []
        for i, ch in enumerate(q["choices"]):
            is_correct = i == correct
            is_chosen = i == chosen
            if revealed[0]:
                if is_correct:
                    bg, border_c, txt_c = GREEN_50, GREEN, GREEN
                elif is_chosen:
                    bg, border_c, txt_c = RED_50, RED, RED
                else:
                    bg, border_c, txt_c = WHITE, BORDER, GRAY
            else:
                bg = BLUE_50 if is_chosen else WHITE
                border_c = BLUE if is_chosen else BORDER
                txt_c = BLUE if is_chosen else DARK

            letter = ["A", "B", "C", "D"][i]
            badge_bg = (GREEN if (revealed[0] and is_correct) else
                        RED if (revealed[0] and is_chosen and not is_correct) else
                        BLUE if is_chosen else BORDER + "44")
            leading = ft.Container(
                content=ft.Text(letter, size=12, weight=ft.FontWeight.W_700,
                                color=WHITE if revealed[0] and (is_correct or is_chosen) else txt_c),
                bgcolor=badge_bg,
                width=28, height=28,
                border_radius=ft.BorderRadius.all(8),
                alignment=ft.Alignment(0, 0),
            )
            items.append(ft.GestureDetector(
                content=ft.Container(
                    content=ft.Row([leading, ft.Text(ch, size=13, color=txt_c, expand=True)],
                                   spacing=10,
                                   vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=bg,
                    border=ft.Border.all(1.5, border_c),
                    border_radius=ft.BorderRadius.all(12),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=12),
                ),
                on_tap=lambda _, ci=i: _on_choice(ci),
                disabled=revealed[0],
            ))
        choices_col.controls = items

    def _on_choice(choice_idx):
        if revealed[0]:
            return
        q = questions[idx[0]]
        answers[q["id"]] = choice_idx
        revealed[0] = True
        is_correct = choice_idx == q["answer"]
        feedback_col.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED if is_correct else ft.Icons.CANCEL_ROUNDED,
                                color=GREEN if is_correct else RED, size=20),
                        ft.Text("Correct!" if is_correct else "Incorrect",
                                size=14, weight=ft.FontWeight.W_700,
                                color=GREEN if is_correct else RED),
                    ], spacing=6),
                    ft.Text(q.get("explanation", ""), size=12, color=DARK),
                ], spacing=6),
                bgcolor=GREEN_50 if is_correct else RED_50,
                border_radius=ft.BorderRadius.all(12),
                padding=ft.Padding.all(14),
                border=ft.Border(left=ft.BorderSide(4, GREEN if is_correct else RED)),
            )
        ]
        feedback_col.visible = True
        next_btn_container.visible = True
        _render_choices(q)
        page.update()

    def _on_next(_):
        if idx[0] < total - 1:
            idx[0] += 1
            _render()
        else:
            _finish()

    def _finish():
        # BUG FIX #2: single call to record_quiz_attempt — no manual grade() call
        correct, total_q, breakdown = state.record_quiz_attempt(
            subj, question_ids, answers, mode=mode
        )
        state.last_result = {
            "correct": correct, "total": total_q, "breakdown": breakdown,
            "mode": mode, "subject": subj, "answers": answers,
            "question_ids": question_ids,
        }
        state.active_question_ids = []
        page.go("/results")

    next_btn_container.content = comp.primary_button(
        "Next Question", on_click=_on_next, expand=True,
        icon=ft.Icons.ARROW_FORWARD_ROUNDED,
    )

    def on_back(_):
        page.go("/topics" if subj else "/home")

    title = (f"{subj} Chapter Test" if mode == "chapter_test"
             else f"{subj} Quiz" if subj and mode == "practice"
             else "Daily Challenge" if mode == "daily"
             else "Retake Quiz")
    _render()

    controls = [
        comp.top_bar(page, title, on_back=on_back),
        ft.Container(height=12),
        ft.Row([progress_bar_ctrl, progress_text], spacing=10,
               vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Container(height=20),
        question_text,
        ft.Container(height=16),
        choices_col,
        ft.Container(height=16),
        feedback_col,
        ft.Container(height=12),
        next_btn_container,
        ft.Container(height=16),
    ]
    return comp.screen_scaffold(page, controls, active_route=None, scroll=True, padding=20)
