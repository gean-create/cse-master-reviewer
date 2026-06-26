"""Review screen — wrong answers grouped by subject."""
import flet as ft
from theme import (BLUE, BLUE_50, WHITE, DARK, GRAY, GREEN, GREEN_50,
                   RED, RED_50, APP_BG, BORDER, SUBJECTS)
import components as comp


def build(page: ft.Page, state) -> ft.View:
    result = getattr(state, "last_result", {}) or {}
    question_ids = result.get("question_ids", [])
    answers = result.get("answers", {})

    from data.questions import get as get_q
    items = []
    for qid in question_ids:
        q = get_q(qid)
        if not q:
            continue
        chosen = answers.get(qid)
        correct = q["answer"]
        if chosen != correct:
            items.append((q, chosen))

    def on_back(_):
        page.go("/results")

    def on_retake(_):
        wrong_ids = [q["id"] for q, _ in items]
        state.active_question_ids = wrong_ids
        state.active_mode = "retake"
        page.go("/quiz")

    def review_card(q, chosen):
        choices = q["choices"]
        correct = q["answer"]

        def choice_row(i, text):
            is_correct = i == correct
            is_chosen = i == chosen
            if is_correct:
                bg, color = GREEN_50, GREEN
                icon = ft.Icons.CHECK_CIRCLE_ROUNDED
            elif is_chosen:
                bg, color = RED_50, RED
                icon = ft.Icons.CANCEL_ROUNDED
            else:
                bg, color = WHITE, GRAY
                icon = None

            return ft.Row(
                [
                    ft.Icon(icon, color=color, size=16) if icon
                    else ft.Container(width=16),
                    ft.Text(f"{['A','B','C','D'][i]}. {text}",
                            size=12, color=color if (is_correct or is_chosen) else GRAY,
                            weight=ft.FontWeight.W_600 if (is_correct or is_chosen)
                            else ft.FontWeight.W_400),
                ],
                spacing=8,
            )

        return comp.card(
            ft.Column(
                [
                    ft.Row(
                        [
                            comp.badge_pill(
                                q.get("subject", "").split()[0],
                                BLUE_50, BLUE,
                            ),
                        ],
                    ),
                    ft.Container(height=6),
                    ft.Text(q["question"], size=13,
                            weight=ft.FontWeight.W_600, color=DARK),
                    ft.Container(height=10),
                    *[choice_row(i, ch) for i, ch in enumerate(q["choices"])],
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Text(
                            q.get("explanation", ""),
                            size=12, color=DARK, italic=True,
                        ),
                        bgcolor=BLUE_50,
                        border_radius=ft.BorderRadius.all(8),
                        padding=ft.Padding.all(10),
                        border=ft.Border(left=ft.BorderSide(3, BLUE)),
                    ),
                ],
                spacing=2,
            ),
        )

    if not items:
        empty = comp.empty_state(
            ft.Icons.CHECK_CIRCLE_ROUNDED,
            "Perfect Score!",
            "You answered every question correctly.",
        )
        controls = [
            comp.top_bar(page, "Review Answers", on_back=on_back),
            ft.Container(height=40),
            empty,
        ]
    else:
        retake_btn = comp.cta_button(
            f"Retake {len(items)} Wrong Question{'s' if len(items)!=1 else ''}",
            on_click=on_retake, expand=True,
        )
        controls = [
            comp.top_bar(page, "Review Answers", on_back=on_back),
            ft.Container(height=8),
            ft.Text(f"{len(items)} incorrect answer{'s' if len(items)!=1 else ''}",
                    size=13, color=GRAY),
            ft.Container(height=12),
            *[ft.Column([review_card(q, ch), ft.Container(height=10)])
              for q, ch in items],
            ft.Container(height=8),
            retake_btn,
            ft.Container(height=16),
        ]

    return comp.screen_scaffold(
        page, controls, active_route=None,
        scroll=True, padding=20,
    )
