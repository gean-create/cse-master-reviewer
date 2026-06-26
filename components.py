"""Reusable UI building blocks shared across screens."""
import flet as ft
import theme as th


def ring(pct: int, size=110, stroke=10, label_size=22, sub_label=None, track_color=None, fill_color=None):
    pct = max(0, min(100, pct))
    fill_color = fill_color or th.BLUE
    track_color = track_color or th.BLUE_50
    inner = [
        ft.ProgressRing(value=pct / 100, width=size, height=size, stroke_width=stroke,
                         color=fill_color, bgcolor=track_color, stroke_cap=ft.StrokeCap.ROUND),
        ft.Container(
            content=ft.Column(
                [
                    th.text(f"{pct}%", size=label_size, weight=ft.FontWeight.W_800, color=th.DARK, font=th.FONT_DISPLAY),
                    th.caption(sub_label) if sub_label else ft.Container(),
                ],
                spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.Alignment.CENTER,
        ),
    ]
    return ft.Stack(inner, width=size, height=size)


def card(content, bgcolor=th.WHITE, padding=16, radius=th.R_MD, shadow=True, on_click=None, border=None, width=None, expand=None):
    c = ft.Container(
        content=content,
        bgcolor=bgcolor,
        padding=padding,
        border_radius=radius,
        shadow=th.shadow_sm() if shadow else None,
        on_click=on_click,
        border=border,
        width=width,
        expand=expand,
        ink=on_click is not None,
        animate=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
    )
    return c


def gradient_card(content, colors=None, padding=20, radius=th.R_LG, shadow=None):
    colors = colors or [th.BLUE, th.BLUE_700]
    return ft.Container(
        content=content,
        padding=padding,
        border_radius=radius,
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=colors),
        shadow=shadow or th.shadow_blue(),
    )


def primary_button(label, on_click=None, icon=None, bgcolor=None, color=th.WHITE, expand=False, height=50, disabled=False):
    return ft.Button(
        content=ft.Row(
            [th.body_strong(label, color=color), ft.Icon(icon, color=color, size=18) if icon else ft.Container()],
            alignment=ft.MainAxisAlignment.CENTER, spacing=8, tight=True,
        ),
        on_click=on_click,
        bgcolor=bgcolor or th.BLUE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14), elevation={"": 0}),
        height=height,
        expand=expand,
        disabled=disabled,
    )


def cta_button(label, on_click=None, icon=None, expand=False, height=50):
    return primary_button(label, on_click=on_click, icon=icon, bgcolor=th.RED, expand=expand, height=height)


def outline_button(label, on_click=None, icon=None, expand=False, height=50, color=th.BLUE):
    return ft.OutlinedButton(
        content=ft.Row(
            [ft.Icon(icon, color=color, size=18) if icon else ft.Container(), th.body_strong(label, color=color)],
            alignment=ft.MainAxisAlignment.CENTER, spacing=8, tight=True,
        ),
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=14),
            side={"": ft.BorderSide(1.4, th.BORDER)},
        ),
        height=height,
        expand=expand,
    )


def ghost_button(label, on_click=None, color=th.GRAY):
    return ft.TextButton(
        content=th.body_strong(label, color=color),
        on_click=on_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14)),
    )


def progress_bar(value, color=th.BLUE, bgcolor=th.BLUE_50, height=8):
    return ft.ProgressBar(value=max(0.0, min(1.0, value)), color=color, bgcolor=bgcolor,
                           border_radius=height, height=height)


def chip(label, selected=False, on_click=None):
    return ft.Container(
        content=th.body_strong(label, color=th.WHITE if selected else th.DARK, size=13),
        bgcolor=th.BLUE if selected else th.SURFACE_TINT,
        padding=ft.Padding.symmetric(horizontal=16, vertical=9),
        border_radius=20,
        on_click=on_click,
        ink=on_click is not None,
    )


def badge_pill(label, bgcolor, color, icon=None, size=11):
    contents = []
    if icon:
        contents.append(ft.Icon(icon, size=13, color=color))
    contents.append(th.text(label, size=size, weight=ft.FontWeight.W_700, color=color))
    return ft.Container(
        content=ft.Row(contents, spacing=4, tight=True, alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=bgcolor, padding=ft.Padding.symmetric(horizontal=10, vertical=5), border_radius=20,
    )


def subject_icon(subject, size=44, bg=None, fg=None):
    bg = bg or th.BLUE_50
    fg = fg or th.BLUE
    return ft.Container(
        content=ft.Icon(th.SUBJECT_ICONS.get(subject, ft.Icons.MENU_BOOK_ROUNDED), color=fg, size=size * 0.45),
        width=size, height=size, bgcolor=bg, border_radius=size * 0.32, alignment=ft.Alignment.CENTER,
    )


def top_bar(page, title, on_back=None, actions=None, transparent=False):
    left = ft.IconButton(
        icon=ft.Icons.ARROW_BACK_ROUNDED, icon_color=th.DARK,
        on_click=on_back or (lambda e: page.go("/home")),
        style=ft.ButtonStyle(bgcolor={"": th.SURFACE_TINT}, shape=ft.CircleBorder()),
    )
    row = [left, ft.Container(content=th.h3(title), expand=True, alignment=ft.Alignment.CENTER_LEFT, padding=ft.Padding.only(left=4))]
    if actions:
        row.extend(actions)
    return ft.Container(
        content=ft.Row(row, alignment=ft.MainAxisAlignment.START),
        padding=ft.Padding.only(left=20, right=20, top=18, bottom=10),
        bgcolor=None if transparent else th.APP_BG,
    )


NAV_ITEMS = [
    ("/home", ft.Icons.HOME_ROUNDED, "Home"),
    ("/topics", ft.Icons.MENU_BOOK_ROUNDED, "Reviewer"),
    ("/practice", ft.Icons.EDIT_NOTE_ROUNDED, "Practice"),
    ("/analytics", ft.Icons.BAR_CHART_ROUNDED, "Analytics"),
    ("/profile", ft.Icons.PERSON_ROUNDED, "Profile"),
]


def bottom_nav(page, active_route):
    try:
        idx = [r for r, _, _ in NAV_ITEMS].index(active_route)
    except ValueError:
        idx = 0

    def on_change(e):
        target = NAV_ITEMS[e.control.selected_index][0]
        if target != page.route:
            page.go(target)

    return ft.NavigationBar(
        selected_index=idx,
        on_change=on_change,
        bgcolor=th.WHITE,
        indicator_color=th.BLUE_50,
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
        destinations=[
            ft.NavigationBarDestination(icon=icon, label=label) for _, icon, label in NAV_ITEMS
        ],
    )


def empty_state(icon, title, subtitle):
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(ft.Icon(icon, size=34, color=th.GRAY_SOFT), width=72, height=72,
                             bgcolor=th.SURFACE_TINT, border_radius=36, alignment=ft.Alignment.CENTER),
                th.h3(title),
                th.caption(subtitle, size=13),
            ],
            spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(vertical=40), alignment=ft.Alignment.CENTER,
    )


def screen_scaffold(page, body_controls, active_route=None, scroll=True, padding=20, bgcolor=th.APP_BG):
    """Wraps screen content in a scrollable column, optionally with bottom nav."""
    column = ft.Column(
        body_controls,
        spacing=16,
        scroll=ft.ScrollMode.AUTO if scroll else None,
        expand=True,
    )
    content = ft.Container(content=column, padding=ft.Padding.only(left=padding, right=padding, top=padding, bottom=4), expand=True, bgcolor=bgcolor)
    controls = [content]
    if active_route:
        controls.append(bottom_nav(page, active_route))
    return ft.View(
        route=page.route,
        controls=[ft.Column(controls, spacing=0, expand=True)],
        padding=0,
        bgcolor=bgcolor,
        scroll=None,
    )
