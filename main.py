"""CSE Master Reviewer — entry point."""
import flet as ft
from theme import BLUE, GOLD, RED, APP_BG, WHITE, FONT_BODY, FONT_URLS
from state import AppState


def build_router(page: ft.Page, state: AppState):
    from screens import (
        splash, onboarding, login, home, topics, lesson,
        reviewer_book, schedule, quiz, exam_config, mock_exam, results,
        analytics, review, achievements, profile
    )

    ROUTES = {
        "/splash":       splash.build,
        "/onboarding":   onboarding.build,
        "/login":        login.build,
        "/home":         home.build,
        "/topics":       topics.build,
        "/lesson":       lesson.build,
        "/reviewer_book":reviewer_book.build,
        "/schedule":     schedule.build,
        "/quiz":         quiz.build,
        "/exam_config":  exam_config.build,
        "/mock_exam":    mock_exam.build,
        "/results":      results.build,
        "/analytics":    analytics.build,
        "/review":       review.build,
        "/achievements": achievements.build,
        "/profile":      profile.build,
    }

    ROOT_ROUTES = {"/home", "/topics", "/analytics", "/profile",
                   "/splash", "/onboarding", "/login", "/schedule"}

    def on_route_change(e: ft.RouteChangeEvent):
        route = e.route.split("?")[0]

        # Auth guard — BUG FIX #7
        if route not in ("/splash", "/onboarding", "/login"):
            if not state.is_logged_in:
                page.go("/login")
                return

        builder = ROUTES.get(route, ROUTES["/home"])
        view = builder(page, state)

        if route in ROOT_ROUTES:
            page.views.clear()
        page.views.append(view)
        page.update()

    def on_view_pop(e: ft.ViewPopEvent):
        if len(page.views) > 1:
            page.views.pop()
            top = page.views[-1]
            page.go(top.route or "/home")

    page.on_route_change = on_route_change
    page.on_view_pop = on_view_pop


async def main(page: ft.Page):
    page.title = "CSE Master Reviewer"
    page.bgcolor = APP_BG
    page.padding = 0
    page.window.width = 390
    page.window.height = 844
    page.fonts = FONT_URLS

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=BLUE, secondary=GOLD, error=RED, surface=WHITE,
        ),
        font_family=FONT_BODY,
        use_material3=True,
    )

    # BUG FIX #1: pass page to AppState
    state = AppState(page)
    await state.load()

    build_router(page, state)
    page.go("/splash")


import os

if os.environ.get("PORT"):
    # Running on a cloud web host (e.g. Render) — serve as a web app
    port = int(os.environ["PORT"])
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
else:
    # Running natively (Android/iOS APK, desktop, or local dev) —
    # let Flet auto-detect the platform. Forcing WEB_BROWSER here is
    # what caused the black screen on real Android devices.
    ft.run(main)
