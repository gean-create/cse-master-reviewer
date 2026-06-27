"""Login / Sign Up screen — professional design."""
import flet as ft
from theme import (NAVY, BLUE, BLUE_50, GOLD, GOLD_50, WHITE, OFF_WHITE,
                   APP_BG, DARK, GRAY, GRAY_SOFT, BORDER, RED)
import components as comp


def build(page: ft.Page, state) -> ft.View:
    is_signup = [True]
    error_text = ft.Text("", color=RED, size=12, visible=False)

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

    TRACKS = ["Professional", "Sub-Professional"]
    selected_track = [TRACKS[0]]

    def track_chip(t):
        sel = t == selected_track[0]
        return ft.GestureDetector(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE_ROUNDED if sel
                        else ft.Icons.RADIO_BUTTON_UNCHECKED_ROUNDED,
                        color=WHITE if sel else GRAY_SOFT, size=16,
                    ),
                    ft.Text(t, size=13,
                            color=WHITE if sel else GRAY,
                            weight=ft.FontWeight.W_600 if sel
                            else ft.FontWeight.W_400),
                ], spacing=8),
                bgcolor=BLUE if sel else WHITE,
                border=ft.Border.all(1.5, BLUE if sel else BORDER),
                border_radius=ft.BorderRadius.all(10),
                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            ),
            on_tap=lambda _, tr=t: _select(tr),
        )

    track_row = ft.Row(spacing=10)

    def _select(t):
        selected_track[0] = t
        track_row.controls = [track_chip(tr) for tr in TRACKS]
        page.update()

    track_row.controls = [track_chip(tr) for tr in TRACKS]

    name_container = ft.Container(content=name_field, visible=True)
    track_container = ft.Container(
        content=ft.Column([
            ft.Text("Exam Track", size=13,
                    weight=ft.FontWeight.W_600, color=NAVY),
            track_row,
        ], spacing=8),
        visible=True,
    )

    title_text = ft.Text(
        "Create Account",
        size=26, weight=ft.FontWeight.W_900,
        color=NAVY, font_family="Georgia",
    )
    subtitle_text = ft.Text(
        "Start your CSE journey today",
        size=13, color=GRAY,
    )
    toggle_text = ft.Text(
        "Already have an account? ", size=13, color=GRAY,
    )
    toggle_link = ft.Text(
        "Sign In", size=13, color=BLUE,
        weight=ft.FontWeight.W_700,
    )
    btn_text = ["Create Account"]

    submit_btn = comp.primary_button(
        "Create Account",
        on_click=None,
        expand=True,
        height=54,
    )

    def on_submit(_):
        email = (email_field.value or "").strip()
        password = (password_field.value or "").strip()

        if not email or not password:
            error_text.value = "Please enter your email and password."
            error_text.visible = True
            page.update()
            return

        if is_signup[0]:
            name = (name_field.value or "").strip()
            if not name:
                error_text.value = "Please enter your full name."
                error_text.visible = True
                page.update()
                return
            if len(password) < 6:
                error_text.value = "Password must be at least 6 characters."
                error_text.visible = True
                page.update()
                return
            # Create profile
            import hashlib
            user_id = hashlib.md5(email.encode()).hexdigest()[:12]
            state.create_profile(name, selected_track[0], email, user_id)
            state.start_trial_if_new()
        else:
            # Sign in — check stored email
            stored = state.data.get("profile", {})
            if stored.get("email", "").lower() != email.lower():
                error_text.value = "Email not found. Please sign up first."
                error_text.visible = True
                page.update()
                return
            if len(password) < 1:
                error_text.value = "Please enter your password."
                error_text.visible = True
                page.update()
                return

        error_text.visible = False
        page.go("/home")

    submit_btn = ft.GestureDetector(
        content=ft.Container(
            content=ft.Row([
                ft.Text("Create Account", size=15,
                        weight=ft.FontWeight.W_700, color=WHITE),
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=BLUE,
            border_radius=ft.BorderRadius.all(14),
            height=54,
            alignment=ft.Alignment(0, 0),
        ),
        on_tap=on_submit,
    )
    submit_label = ft.Text("Create Account", size=15,
                           weight=ft.FontWeight.W_700, color=WHITE)
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
    )

    def toggle_mode(_):
        is_signup[0] = not is_signup[0]
        if is_signup[0]:
            title_text.value = "Create Account"
            subtitle_text.value = "Start your CSE journey today"
            name_container.visible = True
            track_container.visible = True
            toggle_text.value = "Already have an account? "
            toggle_link.value = "Sign In"
            submit_label.value = "Create Account"
        else:
            title_text.value = "Welcome Back"
            subtitle_text.value = "Sign in to continue reviewing"
            name_container.visible = False
            track_container.visible = False
            toggle_text.value = "Don't have an account? "
            toggle_link.value = "Sign Up"
            submit_label.value = "Sign In"
        error_text.visible = False
        page.update()

    body = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=40),
                # Logo
                ft.Container(
                    content=ft.Image(
                        src="assets/icon.png",
                        width=90, height=90,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(height=16),
                title_text,
                subtitle_text,
                ft.Container(height=28),
                name_container,
                ft.Container(height=12),
                email_field,
                ft.Container(height=12),
                password_field,
                ft.Container(height=12),
                track_container,
                ft.Container(height=8),
                error_text,
                ft.Container(height=16),
                submit_container,
                ft.Container(height=16),
                ft.Row(
                    [toggle_text,
                     ft.GestureDetector(
                         content=toggle_link,
                         on_tap=toggle_mode,
                     )],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=40),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=ft.Padding.all(28),
        expand=True,
        bgcolor=APP_BG,
    )

    return ft.View(
        route="/login",
        controls=[body],
        padding=0,
        bgcolor=APP_BG,
    )
