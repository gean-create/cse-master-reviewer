"""
CSE Master Reviewer - Design tokens
Ported 1:1 from the original HTML/CSS design system so the Flet app
matches the approved visual design (Philippine flag color discipline:
white-dominant surface, blue for navigation/education, red reserved
strictly for exam/alert/CTA moments).
"""
import flet as ft

# ---- Colors -----------------------------------------------------------
WHITE = "#FFFFFF"
OFF_WHITE = "#FAFAFA"
SURFACE_TINT = "#F4F6FC"
APP_BG = "#EEF0F4"

BLUE = "#0038A8"
BLUE_700 = "#002777"
BLUE_50 = "#EAF0FB"
BLUE_100 = "#D7E3F6"

RED = "#CE1126"
RED_50 = "#FCEAEC"
RED_100 = "#F8D3D8"

DARK = "#1A1A1A"
GRAY = "#666666"
GRAY_SOFT = "#9CA3AF"
BORDER = "#ECEDF1"

GREEN = "#22C55E"
GREEN_50 = "#E9FAF0"

ORANGE = "#F59E0B"
ORANGE_50 = "#FEF3E2"

GOLD = "#C9A04D"

# ---- Radii --------------------------------------------------------------
R_SM = 12
R_MD = 16
R_LG = 20
R_XL = 24

# ---- Fonts ---------------------------------------------------------------
FONT_DISPLAY = "Plus Jakarta Sans"
FONT_BODY = "Inter"

FONT_URLS = {
    "Plus Jakarta Sans": "https://fonts.gstatic.com/s/plusjakartasans/v8/LDIbaomQNQcsA88c7O9yZ4KMCoOg4Iez5FdSbnLfAcW1YBI.ttf",
    "Inter": "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMa1ZL7.ttf",
}

SUBJECTS = ["Verbal Ability", "Numerical Ability", "Analytical Ability", "General Information"]
SUBJECT_SHORT = {
    "Verbal Ability": "Verbal",
    "Numerical Ability": "Numerical",
    "Analytical Ability": "Analytical",
    "General Information": "Gen. Info",
}
SUBJECT_ICONS = {
    "Verbal Ability": ft.Icons.SPELLCHECK_ROUNDED,
    "Numerical Ability": ft.Icons.CALCULATE_ROUNDED,
    "Analytical Ability": ft.Icons.PSYCHOLOGY_ROUNDED,
    "General Information": ft.Icons.PUBLIC_ROUNDED,
}
PASSING_SCORE = 0.80  # CSE actual passing percentage


def shadow_sm():
    return ft.BoxShadow(blur_radius=10, spread_radius=0, color=ft.Colors.with_opacity(0.06, DARK), offset=ft.Offset(0, 2))


def shadow_md():
    return ft.BoxShadow(blur_radius=24, spread_radius=0, color=ft.Colors.with_opacity(0.08, DARK), offset=ft.Offset(0, 8))


def shadow_blue():
    return ft.BoxShadow(blur_radius=20, spread_radius=0, color=ft.Colors.with_opacity(0.22, BLUE), offset=ft.Offset(0, 8))


def shadow_red():
    return ft.BoxShadow(blur_radius=20, spread_radius=0, color=ft.Colors.with_opacity(0.24, RED), offset=ft.Offset(0, 8))


def text(value, size=14, weight=None, color=DARK, font=FONT_BODY, **kwargs):
    return ft.Text(value, size=size, weight=weight, color=color, font_family=font, **kwargs)


def h1(value, color=DARK):
    return text(value, size=26, weight=ft.FontWeight.W_800, color=color, font=FONT_DISPLAY)


def h2(value, color=DARK):
    return text(value, size=20, weight=ft.FontWeight.W_700, color=color, font=FONT_DISPLAY)


def h3(value, color=DARK):
    return text(value, size=16, weight=ft.FontWeight.W_700, color=color, font=FONT_DISPLAY)


def body(value, color=DARK, size=14):
    return text(value, size=size, weight=ft.FontWeight.W_400, color=color, font=FONT_BODY)


def body_strong(value, color=DARK, size=14):
    return text(value, size=size, weight=ft.FontWeight.W_600, color=color, font=FONT_BODY)


def caption(value, color=GRAY, size=12):
    return text(value, size=size, weight=ft.FontWeight.W_500, color=color, font=FONT_BODY)


def micro(value, color=GRAY_SOFT, size=11):
    return text(value, size=size, weight=ft.FontWeight.W_500, color=color, font=FONT_BODY)
