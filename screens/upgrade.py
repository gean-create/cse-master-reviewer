"""
Upgrade Screen — Free trial info + PayMongo ₱150 payment flow.
"""
import flet as ft
import threading
from theme import (BLUE, BLUE_50, BLUE_700, WHITE, DARK, GRAY,
                   GREEN, GREEN_50, RED, RED_50, GOLD,
                   APP_BG, FONT_DISPLAY, BORDER)
import components as comp
from subscription_service import (
    create_payment_link, verify_payment_link,
    save_premium_to_firebase, get_trial_status,
    FREE_TRIAL_DAYS, PREMIUM_PRICE_PHP, PREMIUM_DAYS,
)


def build(page: ft.Page, state) -> ft.View:
    sub_status = get_trial_status(state.data)
    user_name  = state.name
    user_id    = state.data.get("profile", {}).get("user_id", user_name)

    pending_link_id = [state.data.get("subscription", {}).get("pending_link_id")]

    def on_back(_):
        page.go("/home")

    # ── Status banner ─────────────────────────────────────────────
    if sub_status["is_premium"]:
        days_left = sub_status["premium_days_left"]
        banner = comp.gradient_card(ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.STAR_ROUNDED, color=GOLD, size=28),
                ft.Column([
                    ft.Text("Premium Active ✓", size=16,
                            weight=ft.FontWeight.W_700, color=WHITE),
                    ft.Text(f"{days_left} days remaining",
                            size=12, color=WHITE + "CC"),
                ], spacing=2),
            ], spacing=12),
        ]), colors=[GREEN + "DD", "#15803d"])

    elif sub_status["on_trial"]:
        days_left = sub_status["trial_days_left"]
        banner = comp.gradient_card(ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.HOURGLASS_TOP_ROUNDED, color=GOLD, size=28),
                ft.Column([
                    ft.Text("Free Trial Active", size=16,
                            weight=ft.FontWeight.W_700, color=WHITE),
                    ft.Text(f"{days_left} days left in your free trial",
                            size=12, color=WHITE + "CC"),
                ], spacing=2),
            ], spacing=12),
        ]))

    else:
        banner = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.LOCK_ROUNDED, color=RED, size=24),
                ft.Column([
                    ft.Text("Free Trial Ended", size=15,
                            weight=ft.FontWeight.W_700, color=DARK),
                    ft.Text("Upgrade to continue full access.",
                            size=12, color=GRAY),
                ], spacing=2),
            ], spacing=12),
            bgcolor=RED_50,
            border_radius=ft.BorderRadius.all(14),
            padding=ft.Padding.all(16),
        )

    # ── What's included ───────────────────────────────────────────
    def feature_row(icon, text, premium=True):
        return ft.Row([
            ft.Icon(icon,
                    color=BLUE if premium else GRAY, size=18),
            ft.Text(text, size=13,
                    color=DARK if premium else GRAY),
        ], spacing=10)

    free_features = ft.Column([
        ft.Text("FREE (1 month trial)", size=13,
                weight=ft.FontWeight.W_700, color=GRAY),
        ft.Container(height=8),
        feature_row(ft.Icons.CHECK_ROUNDED, "Basic practice quizzes"),
        feature_row(ft.Icons.CHECK_ROUNDED, "Lessons & flashcards"),
        feature_row(ft.Icons.CHECK_ROUNDED, "Analytics"),
        feature_row(ft.Icons.CLOSE_ROUNDED, "Full mock exam", premium=False),
        feature_row(ft.Icons.CLOSE_ROUNDED, "All 500+ questions", premium=False),
        feature_row(ft.Icons.CLOSE_ROUNDED, "Wrong answer review", premium=False),
    ], spacing=8)

    premium_features = ft.Column([
        ft.Text("PREMIUM — ₱150 / year", size=13,
                weight=ft.FontWeight.W_700, color=BLUE),
        ft.Container(height=8),
        feature_row(ft.Icons.CHECK_ROUNDED, "Everything in Free"),
        feature_row(ft.Icons.CHECK_ROUNDED, "Full 170-item CSE mock exam"),
        feature_row(ft.Icons.CHECK_ROUNDED, "All 500+ questions"),
        feature_row(ft.Icons.CHECK_ROUNDED, "Professional & Sub-Pro tracks"),
        feature_row(ft.Icons.CHECK_ROUNDED, "Wrong answer review"),
        feature_row(ft.Icons.CHECK_ROUNDED, "Detailed analytics"),
        feature_row(ft.Icons.CHECK_ROUNDED, "Priority support"),
    ], spacing=8)

    comparison_card = comp.card(ft.Column([
        free_features,
        ft.Divider(height=20, color=BORDER),
        premium_features,
    ]))

    # ── Price highlight ────────────────────────────────────────────
    price_card = ft.Container(
        content=ft.Column([
            ft.Text("One-Time Payment", size=12,
                    color=GRAY, text_align=ft.TextAlign.CENTER),
            ft.Row([
                ft.Text("₱", size=20, weight=ft.FontWeight.W_700, color=BLUE),
                ft.Text("150", size=48, weight=ft.FontWeight.W_800,
                        color=BLUE, font_family=FONT_DISPLAY),
            ], alignment=ft.MainAxisAlignment.CENTER,
               vertical_alignment=ft.CrossAxisAlignment.END,
               spacing=2),
            ft.Text("Full access for 1 year", size=13, color=GRAY,
                    text_align=ft.TextAlign.CENTER),
            ft.Text("That's only ₱12.50 per month!",
                    size=11, color=GREEN,
                    weight=ft.FontWeight.W_600,
                    text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
        bgcolor=BLUE_50,
        border_radius=ft.BorderRadius.all(16),
        padding=ft.Padding.symmetric(horizontal=20, vertical=20),
        border=ft.Border.all(2, BLUE),
    )

    # ── Payment status UI ──────────────────────────────────────────
    status_text = ft.Text("", size=12, color=GRAY,
                          text_align=ft.TextAlign.CENTER, visible=False)
    verify_btn  = ft.Container(visible=False)
    pay_btn_container = ft.Container()

    def _show_status(msg, color=GRAY):
        status_text.value = msg
        status_text.color = color
        status_text.visible = True
        page.update()

    def _on_pay(_):
        if sub_status["is_premium"]:
            return
        _show_status("Creating secure payment link…", BLUE)
        pay_btn_container.content = comp.primary_button(
            "Processing…", on_click=None, expand=True, disabled=True)
        page.update()

        def _do_payment():
            result = create_payment_link(
                user_email=f"{user_id}@csereviewer.app",
                user_name=user_name,
            )
            if result["error"]:
                _show_status(
                    "Payment system not yet configured.\n"
                    "Please contact the admin.", RED)
                pay_btn_container.content = comp.primary_button(
                    "Pay ₱150 via GCash / Maya",
                    on_click=_on_pay, expand=True)
                page.update()
                return

            link_id = result["link_id"]
            pending_link_id[0] = link_id
            if "subscription" not in state.data:
                state.data["subscription"] = {}
            state.data["subscription"]["pending_link_id"] = link_id
            state.save_bg()

            # Open PayMongo checkout in browser
            page.launch_url(result["url"])

            # Show verify button
            verify_btn.visible = True
            pay_btn_container.content = comp.outline_button(
                "Open Payment Page Again", on_click=_on_pay, expand=True)
            _show_status(
                "Complete your payment in the browser,\n"
                "then tap 'I Already Paid' below.", BLUE)
            page.update()

        threading.Thread(target=_do_payment, daemon=True).start()

    def _on_verify(_):
        lid = pending_link_id[0]
        if not lid:
            _show_status("No pending payment found.", RED)
            return
        _show_status("Verifying your payment…", BLUE)
        page.update()

        def _do_verify():
            result = verify_payment_link(lid)
            if result["error"]:
                _show_status(
                    "Could not verify. Check your internet\n"
                    "connection and try again.", RED)
                page.update()
                return
            if result["paid"]:
                # Save to Firebase (server-side)
                save_premium_to_firebase(user_id, lid)
                # Save locally too
                if "subscription" not in state.data:
                    state.data["subscription"] = {}
                import datetime as dt
                state.data["subscription"].update({
                    "premium_start": dt.date.today().isoformat(),
                    "premium_verified": True,
                    "pending_link_id": None,
                })
                state.save_bg()
                _show_status("✓ Payment confirmed! Premium activated.", GREEN)
                verify_btn.visible = False
                page.update()
                import asyncio; asyncio.get_event_loop().call_later(
                    1.5, lambda: page.go("/home"))
            else:
                _show_status(
                    "Payment not yet received.\n"
                    "Complete GCash/Maya payment first, then verify.", ORANGE := "#F59E0B")
                page.update()

        threading.Thread(target=_do_verify, daemon=True).start()

    pay_btn_container.content = (
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.STAR_ROUNDED, color=GOLD, size=18),
                ft.Text("Premium Already Active",
                        size=14, color=GOLD, weight=ft.FontWeight.W_600),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            bgcolor=GREEN_50,
            border_radius=ft.BorderRadius.all(14),
            padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        ) if sub_status["is_premium"] else
        comp.primary_button(
            "Pay ₱150 via GCash / Maya",
            on_click=_on_pay, expand=True,
            icon=ft.Icons.PAYMENT_ROUNDED,
        )
    )

    verify_btn.content = comp.outline_button(
        "I Already Paid — Verify Now",
        on_click=_on_verify, expand=True,
    )

    # Check if there's a pending link from a previous session
    if state.data.get("subscription", {}).get("pending_link_id") and not sub_status["is_premium"]:
        verify_btn.visible = True
        _show_status("Tap 'I Already Paid' if you completed payment.", BLUE)

    secure_note = ft.Row([
        ft.Icon(ft.Icons.LOCK_ROUNDED, color=GREEN, size=14),
        ft.Text("Secured by PayMongo · GCash · Maya",
                size=11, color=GRAY),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)

    controls = [
        comp.top_bar(page, "Upgrade to Premium", on_back=on_back),
        ft.Container(height=8),
        banner,
        ft.Container(height=16),
        price_card,
        ft.Container(height=16),
        comparison_card,
        ft.Container(height=20),
        pay_btn_container,
        ft.Container(height=10),
        verify_btn,
        ft.Container(height=8),
        status_text,
        ft.Container(height=12),
        secure_note,
        ft.Container(height=20),
        ft.Text(
            "Questions? Message us on Facebook:\nfacebook.com/csemasterreviewer",
            size=11, color=GRAY, text_align=ft.TextAlign.CENTER,
        ),
        ft.Container(height=16),
    ]

    return comp.screen_scaffold(
        page, controls, active_route=None, scroll=True, padding=20)
