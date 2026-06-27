"""
CSE Master Reviewer 2026 — Component Library
Professional, exam-focused UI components.
"""
import flet as ft
from theme import (
    NAVY, BLUE, BLUE_700, BLUE_50, BLUE_100, GOLD, GOLD_50,
    WHITE, APP_BG, OFF_WHITE, SURFACE,
    DARK, GRAY, GRAY_SOFT, BORDER,
    GREEN, GREEN_50, RED, RED_50, ORANGE, ORANGE_50,
    SUBJECTS, SUBJECT_ICONS, SUBJECT_COLORS,
    FONT_DISPLAY, FONT_BODY
)


def shadow(blur=12, opacity=0.08, offset_y=4):
    return ft.BoxShadow(
        blur_radius=blur,
        color=ft.Colors.with_opacity(opacity, "#0D1B4B"),
        offset=ft.Offset(0, offset_y),
    )


def card(content, bgcolor=WHITE, padding=16, radius=16,
         shadow_on=True, on_click=None, border=None, width=None):
    return ft.Container(
        content=content,
        bgcolor=bgcolor,
        border_radius=ft.BorderRadius.all(radius),
        padding=ft.Padding.all(padding),
        border=border,
        width=width,
        shadow=shadow() if shadow_on else None,
        on_click=on_click,
        ink=on_click is not None,
    )


def gradient_card(content, colors=None, padding=20, radius=20):
    colors = colors or [BLUE, NAVY]
    return ft.Container(
        content=content,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=colors,
        ),
        border_radius=ft.BorderRadius.all(radius),
        padding=ft.Padding.all(padding),
        shadow=shadow(blur=20, opacity=0.20, offset_y=6),
    )


def primary_button(label, on_click, icon=None, expand=False,
                   height=52, disabled=False, bgcolor=None):
    bgcolor = bgcolor or BLUE
    content = ft.Row(
        [
            ft.Icon(icon, color=WHITE, size=18) if icon else ft.Container(),
            ft.Text(label, size=15, weight=ft.FontWeight.W_700, color=WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
    ) if icon else ft.Text(label, size=15, weight=ft.FontWeight.W_700, color=WHITE)

    return ft.Container(
        content=content,
        bgcolor=bgcolor if not disabled else GRAY_SOFT,
        border_radius=ft.BorderRadius.all(14),
        height=height,
        alignment=ft.Alignment(0, 0),
        on_click=on_click if not disabled else None,
        ink=not disabled,
        expand=expand,
        shadow=shadow(blur=8, opacity=0.20, offset_y=3) if not disabled else None,
    )


def gold_button(label, on_click, icon=None, expand=False, height=52):
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icon, color=NAVY, size=18) if icon else ft.Container(),
                ft.Text(label, size=15, weight=ft.FontWeight.W_700, color=NAVY),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ) if icon else ft.Text(label, size=15, weight=ft.FontWeight.W_700, color=NAVY),
        bgcolor=GOLD,
        border_radius=ft.BorderRadius.all(14),
        height=height,
        alignment=ft.Alignment(0, 0),
        on_click=on_click,
        ink=True,
        expand=expand,
        shadow=shadow(blur=8, opacity=0.20, offset_y=3),
    )


def outline_button(label, on_click, expand=False, height=52, color=BLUE):
    return ft.Container(
        content=ft.Text(label, size=15, weight=ft.FontWeight.W_600, color=color),
        bgcolor=WHITE,
        border=ft.Border.all(2, color),
        border_radius=ft.BorderRadius.all(14),
        height=height,
        alignment=ft.Alignment(0, 0),
        on_click=on_click,
        ink=True,
        expand=expand,
    )


def ghost_button(label, on_click, color=GRAY):
    return ft.TextButton(
        content=ft.Text(label, size=14, color=color, weight=ft.FontWeight.W_500),
        on_click=on_click,
    )


def cta_button(label, on_click, expand=False, height=52):
    return primary_button(label, on_click, expand=expand,
                          height=height, bgcolor=RED)


def progress_bar(value, color=BLUE, bgcolor=BLUE_50, height=8):
    return ft.ProgressBar(
        value=max(0.0, min(1.0, float(value or 0))),
        color=color,
        bgcolor=bgcolor,
        border_radius=ft.BorderRadius.all(height // 2),
        height=height,
    )


def ring(pct, size=100, stroke=10, label_size=20,
         fill_color=BLUE, track_color=BLUE_50, sub_label=None):
    pct = max(0.0, min(1.0, float(pct or 0)))
    label = ft.Text(
        f"{int(pct * 100)}%",
        size=label_size,
        weight=ft.FontWeight.W_800,
        color=fill_color,
    )
    ring_ctrl = ft.ProgressRing(
        value=pct,
        width=size, height=size,
        stroke_width=stroke,
        color=fill_color,
        bgcolor=track_color,
    )
    children = [ring_ctrl, label]
    if sub_label:
        children.append(ft.Text(sub_label, size=10, color=GRAY))
    return ft.Stack(
        controls=[
            ring_ctrl,
            ft.Container(
                content=ft.Column(
                    children[1:],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                alignment=ft.Alignment(0, 0),
                width=size, height=size,
            )
        ],
        width=size, height=size,
    )


def badge_pill(label, bgcolor=BLUE_50, color=BLUE, icon=None, size=11):
    items = []
    if icon:
        items.append(ft.Icon(icon, color=color, size=size + 2))
    items.append(ft.Text(label, size=size, color=color, weight=ft.FontWeight.W_600))
    return ft.Container(
        content=ft.Row(items, spacing=4, tight=True),
        bgcolor=bgcolor,
        border_radius=ft.BorderRadius.all(20),
        padding=ft.Padding.symmetric(horizontal=10, vertical=5),
    )


def subject_icon(subject, size=44):
    icon = SUBJECT_ICONS.get(subject, ft.Icons.QUIZ_ROUNDED)
    color = SUBJECT_COLORS.get(subject, BLUE)
    bg = color + "18"
    return ft.Container(
        content=ft.Icon(icon, color=color, size=size * 0.5),
        bgcolor=bg,
        border_radius=ft.BorderRadius.all(size * 0.3),
        width=size, height=size,
        alignment=ft.Alignment(0, 0),
        border=ft.Border.all(1.5, color + "33"),
    )


def top_bar(page, title, on_back=None, actions=None, subtitle=None):
    left = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_ROUNDED,
                icon_color=NAVY, icon_size=22,
                on_click=on_back,
            ) if on_back else ft.Container(width=8),
            ft.Column(
                [
                    ft.Text(title, size=17, weight=ft.FontWeight.W_700, color=NAVY),
                    ft.Text(subtitle, size=11, color=GRAY) if subtitle else ft.Container(),
                ],
                spacing=0,
            ),
        ],
        spacing=4,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
    right = ft.Row(actions or [], spacing=4)
    return ft.Container(
        content=ft.Row(
            [left, right],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=WHITE,
        padding=ft.Padding.symmetric(horizontal=8, vertical=8),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER)),
    )


NAV_ITEMS = [
    ("/home",      ft.Icons.HOME_ROUNDED,      "Home"),
    ("/topics",    ft.Icons.MENU_BOOK_ROUNDED,  "Reviewer"),
    ("/practice",  ft.Icons.EDIT_NOTE_ROUNDED,  "Practice"),
    ("/analytics", ft.Icons.BAR_CHART_ROUNDED,  "Analytics"),
    ("/profile",   ft.Icons.PERSON_ROUNDED,     "Profile"),
]


def bottom_nav(page, active_route):
    def on_change(e):
        _, _, routes = zip(*NAV_ITEMS)
        _, _, r = NAV_ITEMS[e.control.selected_index]
        page.go(r)

    idx = 0
    for i, (route, _, _) in enumerate(NAV_ITEMS):
        if active_route and active_route.startswith(route):
            idx = i
            break

    return ft.NavigationBar(
        selected_index=idx,
        on_change=on_change,
        bgcolor=WHITE,
        indicator_color=BLUE_50,
        destinations=[
            ft.NavigationBarDestination(
                icon=icon,
                selected_icon=icon,
                label=label,
            )
            for _, icon, label in NAV_ITEMS
        ],
        shadow_color=ft.Colors.with_opacity(0.08, NAVY),
        elevation=8,
    )


def empty_state(icon, title, subtitle):
    return ft.Column(
        [
            ft.Container(
                content=ft.Icon(icon, color=GRAY_SOFT, size=52),
                padding=ft.Padding.all(20),
            ),
            ft.Text(title, size=16, weight=ft.FontWeight.W_700, color=GRAY),
            ft.Text(subtitle, size=13, color=GRAY_SOFT,
                    text_align=ft.TextAlign.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
    )


def screen_scaffold(page, controls, active_route=None,
                    scroll=True, padding=20, bgcolor=APP_BG):
    body = ft.Column(
        controls,
        scroll=ft.ScrollMode.AUTO if scroll else None,
        expand=True,
        spacing=0,
    )

    bottom = [bottom_nav(page, active_route)] if active_route else []

    return ft.View(
        route=active_route or "/",
        controls=[
            ft.Column(
                [
                    ft.Container(
                        content=body,
                        expand=True,
                        padding=ft.Padding.all(padding),
                    ),
                    *bottom,
                ],
                expand=True,
                spacing=0,
            )
        ],
        padding=0,
        bgcolor=bgcolor,
    )
