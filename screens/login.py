"""
Login / Sign Up — Clean white design.
Always shown. Clear Sign Up / Sign In tabs.
Track selection is prominent and required.
"""
import flet as ft
from theme import (NAVY, BLUE, BLUE_50, BLUE_100, GOLD, GOLD_50,
                   WHITE, APP_BG, DARK, GRAY, GRAY_SOFT, BORDER, RED, GREEN)
import components as comp


TRACKS = [
    {
        "id": "Professional",
        "label": "Professional",
        "subtitle": "170 items • 3h 10m",
        "desc": "2nd level positions\n(requires Bachelor's degree)",
        "icon": ft.Icons.MILITARY_TECH_ROUNDED,
        "color": BLUE,
    },
    {
        "id": "Sub-Professional",
        "label": "Sub-Professional",
        "subtitle": "165 items • 2h 40m",
        "desc": "1st level positions\n(clerical & custodial roles)",
        "icon": ft.Icons.SCHOOL_ROUNDED,
        "color": "#7C3AED",
    },
]


def build(page: ft.Page, state) -> ft.View:
    # Tab: 0 = Sign Up, 1 = Sign In
    active_tab = [0]
    selected_track = ["Professional"]
    error_ref = [None]

    name_field = ft.TextField(
        label="Full Name",
        hint_text="e.g. Juan Dela Cruz",
        prefix_icon=ft.Icons.PERSON_ROUNDED,
        border_color=BORDER,
        focused_border_color=BLUE,
        border_radius=ft.BorderRadius.all(12),
        bgcolor=WHITE,
        color=NAVY,
        label_style=ft.TextStyle(color=GRAY),
        cursor_color=BLUE,
    )

    email_field = ft.TextField(
        label="Email Address",
        hint_text="yourname@email.com",
        prefix_icon=ft.Icons.EMAIL_ROUNDED,
        border_color=BORDER,
        focused_border_color=BLUE,
        border_radius=ft.BorderRadius.all(12),
        bgcolor=WHITE,
        color=NAVY,
        label_style=ft.TextStyle(color=GRAY),
        cursor_color=BLUE,
        keyboard_type=ft.KeyboardType.EMAIL,
    )

    password_field = ft.TextField(
        label="Password",
        hint_text="Minimum 6 characters",
        prefix_icon=ft.Icons.LOCK_ROUNDED,
        password=True,
        can_reveal_password=True,
        border_color=BORDER,
        focused_border_color=BLUE,
        border_radius=ft.BorderRadius.all(12),
        bgcolor=WHITE,
        color=NAVY,
        label_style=ft.TextStyle(color=GRAY),
        cursor_color=BLUE,
    )

    error_text = ft.Text("", color=RED, size=12, visible=False)
    error_ref[0] = error_text

    def show_error(msg):
        error_text.value = msg
        error_text.visible = True
        page.update()

    def clear_error():
        error_text.visible = False

    # ── Track selection ──────────────────────────────────────────
    track_col = ft.Column(spacing=10)

    def build_track_cards():
        cards = []
        for t in TRACKS:
            sel = t["id"] == selected_track[0]
            cards.append(ft.GestureDetector(
                content=ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(t["icon"],
                                           color=WHITE if sel else t["color"],
                                           size=24),
                            bgcolor=t["color"] if sel else t["color"] + "18",
                            border_radius=ft.BorderRadius.all(12),
                            padding=ft.Padding.all(10),
                            width=48, height=48,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column([
                            ft.Row([
                                ft.Text(t["label"], size=15,
                                        weight=ft.FontWeight.W_700,
                                        color=NAVY),
                                ft.Container(
                                    content=ft.Text(t["subtitle"], size=10,
                                                   color=t["color"],
                                                   weight=ft.FontWeight.W_600),
                                    bgcolor=t["color"] + "18",
                                    border_radius=ft.BorderRadius.all(6),
                                    padding=ft.Padding.symmetric(
                                        horizontal=8, vertical=3),
                                ),
                            ], spacing=8),
                            ft.Text(t["desc"], size=11, color=GRAY),
                        ], spacing=2, expand=True),
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE_ROUNDED if sel
                            else ft.Icons.RADIO_BUTTON_UNCHECKED_ROUNDED,
                            color=t["color"] if sel else GRAY_SOFT,
                            size=22,
                        ),
                    ], spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=t["color"] + "08" if sel else WHITE,
                    border=ft.Border.all(
                        2 if sel else 1,
                        t["color"] if sel else BORDER,
                    ),
                    border_radius=ft.BorderRadius.all(14),
                    padding=ft.Padding.all(14),
                ),
                on_tap=lambda _, tid=t["id"]: _select_track(tid),
            ))
        track_col.controls = cards

    def _select_track(tid):
        selected_track[0] = tid
        build_track_cards()
        page.update()

    build_track_cards()

    # ── Tab buttons ──────────────────────────────────────────────
    tab_signup = ft.Container()
    tab_signin = ft.Container()

    def build_tabs():
        def tab_btn(label, idx):
            sel = active_tab[0] == idx
            return ft.GestureDetector(
                content=ft.Container(
                    content=ft.Text(
                        label, size=14,
                        weight=ft.FontWeight.W_700 if sel
                        else ft.FontWeight.W_500,
                        color=BLUE if sel else GRAY,
                    ),
                    border=ft.Border(
                        bottom=ft.BorderSide(
                            3 if sel else 1,
                            BLUE if sel else BORDER,
                        )
                    ),
                    padding=ft.Padding.only(bottom=10),
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                ),
                on_tap=lambda _, i=idx: _switch_tab(i),
                expand=True,
            )
        return ft.Row([tab_btn("Create Account", 0),
                      tab_btn("Sign In", 1)],
                     spacing=0)

    tabs_container = ft.Container(content=build_tabs())

    # ── Form sections ─────────────────────────────────────────────
    signup_only = ft.Column([
        name_field,
        ft.Container(height=4),
        ft.Text("Choose Your Exam Track",
                size=13, weight=ft.FontWeight.W_700, color=NAVY),
        ft.Text("You can change this later in Profile settings.",
                size=11, color=GRAY),
        ft.Container(height=6),
        track_col,
        ft.Container(height=4),
    ], spacing=10, visible=True)

    def _switch_tab(idx):
        active_tab[0] = idx
        signup_only.visible = (idx == 0)
        tabs_container.content = build_tabs()
        clear_error()
        page.update()

    def on_submit(_):
        clear_error()
        email = (email_field.value or "").strip()
        pwd = (password_field.value or "").strip()

        if not email:
            show_error("Please enter your email address.")
            return
        if "@" not in email or "." not in email:
            show_error("Please enter a valid email address.")
            return
        if not pwd:
            show_error("Please enter a password.")
            return

        if active_tab[0] == 0:
            # Sign Up
            name = (name_field.value or "").strip()
            if not name:
                show_error("Please enter your full name.")
                return
            if len(pwd) < 6:
                show_error("Password must be at least 6 characters.")
                return
            # Check if email already used
            existing = state.data.get("profile", {})
            if existing and existing.get("email", "").lower() == email.lower():
                show_error("This email is already registered. Please Sign In.")
                return

            import hashlib
            uid = hashlib.md5(email.encode()).hexdigest()[:12]
            state.create_profile(name, selected_track[0], email, uid)
            state.start_trial_if_new()
            page.go("/home")

        else:
            # Sign In
            stored = state.data.get("profile") or {}
            if not stored:
                show_error("No account found. Please create an account first.")
                return
            if stored.get("email", "").lower() != email.lower():
                show_error("Email not found. Please check and try again.")
                return
            # Password check (simple — stored hash in production would be better)
            if len(pwd) < 1:
                show_error("Please enter your password.")
                return
            page.go("/home")

    submit_btn = ft.Container(
        content=ft.Row(
            [ft.Text("Create Account", size=15,
                     weight=ft.FontWeight.W_700, color=WHITE)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=BLUE,
        border_radius=ft.BorderRadius.all(14),
        height=54,
        alignment=ft.Alignment(0, 0),
        on_click=on_submit,
        ink=True,
    )

    submit_label = ft.Text("Create Account", size=15,
                           weight=ft.FontWeight.W_700, color=WHITE)

    def update_btn_label():
        submit_label.value = "Create Account" if active_tab[0] == 0 else "Sign In"

    submit_container = ft.Container(
        content=ft.Row(
            [submit_label],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=BLUE,
        border_radius=ft.BorderRadius.all(14),
        height=54,
        alignment=ft.Alignment(0, 0),
        on_click=on_submit,
        ink=True,
        shadow=ft.BoxShadow(
            blur_radius=12,
            color=ft.Colors.with_opacity(0.25, BLUE),
            offset=ft.Offset(0, 4),
        ),
    )

    def _switch_tab_with_btn(idx):
        active_tab[0] = idx
        signup_only.visible = (idx == 0)
        tabs_container.content = build_tabs()
        submit_label.value = "Create Account" if idx == 0 else "Sign In"
        clear_error()
        page.update()

    # Patch switch tab
    def _switch_tab(idx):
        _switch_tab_with_btn(idx)

    body = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=60),
                # Logo — white background, logo centered
                ft.Container(
                    content=ft.Image(
                        src="assets/icon.png",
                        width=130,
                        height=130,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(height=8),
                ft.Text(
                    "Civil Service Reviewer 2026",
                    size=18, weight=ft.FontWeight.W_800,
                    color=NAVY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "100% Free • For all Filipino public servants",
                    size=12, color=GRAY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=28),
                tabs_container,
                ft.Container(height=20),
                signup_only,
                email_field,
                ft.Container(height=10),
                password_field,
                ft.Container(height=8),
                error_text,
                ft.Container(height=16),
                submit_container,
                ft.Container(height=20),
                ft.Text(
                    "By continuing, you agree to use this app\nresponsibly for exam preparation.",
                    size=10, color=GRAY_SOFT,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=40),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=ft.Padding.symmetric(horizontal=24, vertical=0),
        expand=True,
        bgcolor=WHITE,
    )

    return ft.View(
        route="/login",
        controls=[body],
        padding=0,
        bgcolor=WHITE,
    )
