"""Flashcards screen — flip-card study deck."""
import flet as ft
from theme import (BLUE, BLUE_50, BLUE_700, WHITE, DARK, GRAY,
                   GREEN, GREEN_50, ORANGE, ORANGE_50, APP_BG, FONT_DISPLAY)
import components as comp
from data.flashcards import FLASHCARDS


def build(page: ft.Page, state) -> ft.View:
    subj = state.current_subject
    cards = FLASHCARDS.get(subj, [])
    idx = [0]
    flipped = [False]

    def on_back(_):
        page.go("/topics")

    # ── Progress bar ────────────────────────────────────────────
    prog_bar = comp.progress_bar(
        (idx[0] + 1) / max(len(cards), 1)
    )
    prog_text = ft.Text(f"1 / {len(cards)}", size=12, color=GRAY)

    def progress_row():
        return ft.Row(
            [prog_bar, prog_text],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

    prog_container = ft.Container(content=progress_row())

    # ── Flip card ────────────────────────────────────────────────
    card_content_col = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    flip_card_container = ft.Container(
        content=card_content_col,
        bgcolor=WHITE,
        border_radius=ft.BorderRadius.all(20),
        padding=ft.Padding.all(28),
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.10, "#000000"),
            offset=ft.Offset(0, 6),
        ),
        height=240,
        alignment=ft.Alignment(0, 0),
    )

    def _current_card():
        return cards[idx[0]] if idx[0] < len(cards) else None

    def _render():
        c = _current_card()
        if c is None:
            return
        if flipped[0]:
            card_content_col.controls = [
                ft.Text("DEFINITION", size=10,
                        weight=ft.FontWeight.W_700,
                        color=BLUE),
                ft.Container(height=12),
                ft.Text(c["definition"], size=15, color=DARK,
                        text_align=ft.TextAlign.CENTER),
            ]
            flip_card_container.bgcolor = BLUE_50
            flip_card_container.border = ft.Border.all(2, BLUE)
        else:
            card_content_col.controls = [
                ft.Text("TERM", size=10, weight=ft.FontWeight.W_700,
                        color=GRAY),
                ft.Container(height=12),
                ft.Text(c["term"], size=20, weight=ft.FontWeight.W_700,
                        color=DARK, text_align=ft.TextAlign.CENTER,
                        font_family=FONT_DISPLAY),
                ft.Container(height=12),
                ft.Text("Tap to flip ↓", size=11, color=GRAY),
            ]
            flip_card_container.bgcolor = WHITE
            flip_card_container.border = None

        prog_bar.value = (idx[0] + 1) / len(cards)
        prog_text.value = f"{idx[0]+1} / {len(cards)}"
        prog_container.content = progress_row()
        page.update()

    def on_flip(_):
        flipped[0] = not flipped[0]
        _render()

    def _advance(mastered: bool):
        c = _current_card()
        if c:
            state.mark_flashcard(subj, c["id"], mastered)
        flipped[0] = False
        idx[0] += 1
        if idx[0] >= len(cards):
            state.save_bg()
            page.go("/quiz")
        else:
            _render()

    def on_know(_):
        _advance(True)

    def on_learning(_):
        _advance(False)

    # Initial render
    _render()

    know_btn = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.CHECK_ROUNDED, color=WHITE, size=18),
             ft.Text("Know It!", size=14, color=WHITE, weight=ft.FontWeight.W_600)],
            spacing=6,
        ),
        bgcolor=GREEN,
        border_radius=ft.BorderRadius.all(14),
        padding=ft.Padding.symmetric(horizontal=24, vertical=14),
        on_click=on_know,
        ink=True,
    )

    learning_btn = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.REFRESH_ROUNDED, color=ORANGE, size=18),
             ft.Text("Still Learning", size=14, color=ORANGE,
                     weight=ft.FontWeight.W_600)],
            spacing=6,
        ),
        bgcolor=ORANGE_50,
        border_radius=ft.BorderRadius.all(14),
        padding=ft.Padding.symmetric(horizontal=24, vertical=14),
        on_click=on_learning,
        ink=True,
    )

    controls = [
        comp.top_bar(page, f"{subj} Flashcards", on_back=on_back),
        ft.Container(height=12),
        prog_container,
        ft.Container(height=20),
        ft.GestureDetector(
            content=flip_card_container,
            on_tap=on_flip,
        ),
        ft.Container(height=8),
        ft.Text("Tap the card to reveal definition",
                size=11, color=GRAY, text_align=ft.TextAlign.CENTER),
        ft.Container(height=24),
        ft.Row(
            [learning_btn, know_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        ),
        ft.Container(height=16),
    ]

    return comp.screen_scaffold(
        page, controls, active_route=None,
        scroll=False, padding=20,
    )
