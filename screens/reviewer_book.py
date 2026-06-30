"""
Reviewer Book — Brainbox-style printed-reviewer experience.
Numbered items grouped by category, in-page explanations,
an Answer Key you reveal per item — like flipping through
an actual CSC reviewer book, not flashcards.
"""
import flet as ft
from theme import (NAVY, BLUE, BLUE_50, GOLD, GOLD_50, WHITE, APP_BG,
                   GRAY, GRAY_SOFT, BORDER, GREEN, GREEN_50, RED, RED_50)
import components as comp
from data.questions import by_subject


def build(page: ft.Page, state) -> ft.View:
    subj = state.current_subject
    items = by_subject(subj)

    # Group by category, preserving first-seen order (like book chapters)
    chapters = {}
    for q in items:
        cat = q.get("category", "General")
        chapters.setdefault(cat, []).append(q)

    revealed = {}   # qid -> bool, whether answer key is shown

    def on_back(_):
        page.go("/topics")

    def on_continue(_):
        state.mark_lesson_done(subj)
        ids = [q["id"] for q in items]
        state.active_question_ids = ids[: min(10, len(ids))]
        state.active_mode = "practice"
        page.go("/quiz")

    list_col = ft.Column(spacing=0)

    def toggle_reveal(qid):
        revealed[qid] = not revealed.get(qid, False)
        render()

    def render():
        blocks = []
        item_no = 1
        for chapter_title, qs in chapters.items():
            blocks.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            width=4, height=22, bgcolor=GOLD,
                            border_radius=ft.BorderRadius.all(2),
                        ),
                        ft.Text(chapter_title.upper(), size=13,
                                weight=ft.FontWeight.W_800,
                                color=NAVY),
                    ], spacing=10),
                    padding=ft.Padding.only(top=18, bottom=10),
                )
            )
            for q in qs:
                is_open = revealed.get(q["id"], False)
                choice_rows = []
                for i, ch in enumerate(q["choices"]):
                    is_correct = i == q["answer"]
                    letter = ["A", "B", "C", "D"][i]
                    if is_open and is_correct:
                        txt_color, bg = GREEN, GREEN_50
                    else:
                        txt_color, bg = GRAY, WHITE
                    choice_rows.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(f"{letter}.", size=12,
                                        weight=ft.FontWeight.W_700,
                                        color=txt_color),
                                ft.Text(ch, size=12, color=txt_color,
                                        expand=True),
                                ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED,
                                        color=GREEN, size=14)
                                if (is_open and is_correct) else ft.Container(),
                            ], spacing=8),
                            bgcolor=bg,
                            border_radius=ft.BorderRadius.all(6),
                            padding=ft.Padding.symmetric(
                                horizontal=8, vertical=5),
                        )
                    )

                explanation_box = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.MENU_BOOK_ROUNDED,
                                color=GOLD, size=14),
                        ft.Text(q.get("explanation", ""), size=11.5,
                                color=NAVY, italic=True, expand=True),
                    ], spacing=8),
                    bgcolor=GOLD_50,
                    border_radius=ft.BorderRadius.all(8),
                    padding=ft.Padding.all(10),
                    visible=is_open,
                )

                item_card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(str(item_no), size=12,
                                               weight=ft.FontWeight.W_800,
                                               color=WHITE),
                                bgcolor=NAVY,
                                width=24, height=24,
                                border_radius=ft.BorderRadius.all(6),
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Text(q["question"], size=13.5,
                                    weight=ft.FontWeight.W_600,
                                    color=NAVY, expand=True),
                        ], spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.START),
                        ft.Container(height=8),
                        ft.Column(choice_rows, spacing=4),
                        ft.Container(height=6) if is_open else ft.Container(height=0),
                        explanation_box,
                        ft.Container(height=4),
                        ft.GestureDetector(
                            content=ft.Row([
                                ft.Icon(
                                    ft.Icons.VISIBILITY_OFF_ROUNDED if not is_open
                                    else ft.Icons.VISIBILITY_ROUNDED,
                                    color=BLUE, size=13,
                                ),
                                ft.Text(
                                    "Hide Answer Key" if is_open
                                    else "Show Answer Key",
                                    size=11.5, color=BLUE,
                                    weight=ft.FontWeight.W_700,
                                ),
                            ], spacing=6),
                            on_tap=lambda _, qid=q["id"]: toggle_reveal(qid),
                        ),
                    ], spacing=0),
                    bgcolor=WHITE,
                    border=ft.Border.all(1, BORDER),
                    border_radius=ft.BorderRadius.all(12),
                    padding=ft.Padding.all(14),
                    margin=ft.Margin.only(bottom=10),
                )
                blocks.append(item_card)
                item_no += 1

        list_col.controls = blocks
        page.update()

    render()

    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK_ROUNDED,
                             icon_color=NAVY, on_click=on_back),
                ft.Column([
                    ft.Text(subj, size=16, weight=ft.FontWeight.W_800,
                            color=NAVY),
                    ft.Text(f"{len(items)} items • Reviewer Book",
                            size=11, color=GRAY),
                ], spacing=0, expand=True),
                ft.Container(
                    content=ft.Icon(ft.Icons.MENU_BOOK_ROUNDED,
                                    color=GOLD, size=20),
                    bgcolor=GOLD_50,
                    border_radius=ft.BorderRadius.all(10),
                    padding=ft.Padding.all(8),
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ]),
        bgcolor=WHITE,
        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER)),
    )

    body = ft.Column([
        header,
        ft.Container(
            content=ft.Column(
                [list_col,
                 ft.Container(height=8),
                 comp.primary_button(
                     "Continue to Practice Quiz →",
                     on_click=on_continue, expand=True,
                     icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                 ),
                 ft.Container(height=20)],
                scroll=ft.ScrollMode.AUTO, expand=True,
            ),
            padding=ft.Padding.all(16),
            expand=True,
        ),
    ], spacing=0, expand=True)

    return ft.View(
        route="/reviewer_book",
        controls=[body],
        padding=0,
        bgcolor=APP_BG,
    )
