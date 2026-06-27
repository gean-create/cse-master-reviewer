"""
CSE Master Reviewer 2026 — Design System
Professional, clean, exam-focused UI.
"""
import flet as ft

# ── Brand Colors ────────────────────────────────────────────────────
NAVY       = "#0D1B4B"   # Primary dark navy
BLUE       = "#0038A8"   # Philippine flag blue
BLUE_700   = "#002777"   # Darker blue
BLUE_50    = "#EAF0FB"   # Light blue tint
BLUE_100   = "#C8D9F5"   # Slightly deeper blue tint
GOLD       = "#C9A04D"   # Philippine gold
GOLD_LIGHT = "#F0D080"   # Light gold
GOLD_50    = "#FEF9EC"   # Gold tint background

WHITE      = "#FFFFFF"
OFF_WHITE  = "#F8F9FD"
SURFACE    = "#FFFFFF"
APP_BG     = "#F0F4FF"

DARK       = "#0D1B4B"   # Main text = navy
DARK_2     = "#1E2D5A"   # Secondary dark
GRAY       = "#5A6B8A"   # Body text
GRAY_SOFT  = "#8FA0BD"   # Placeholder / hint
BORDER     = "#DCE3F0"   # Borders

GREEN      = "#16A34A"
GREEN_50   = "#DCFCE7"
GREEN_100  = "#BBF7D0"
RED        = "#DC2626"
RED_50     = "#FEE2E2"
ORANGE     = "#D97706"
ORANGE_50  = "#FEF3C7"

# ── Typography ──────────────────────────────────────────────────────
FONT_DISPLAY = "Georgia"
FONT_BODY    = "Arial"

FONT_URLS = {}   # Using system fonts — no CDN needed

# ── Subjects ────────────────────────────────────────────────────────
SUBJECTS = ["Verbal Ability", "Numerical Ability",
            "Analytical Ability", "General Information"]

SUBJECT_ICONS = {
    "Verbal Ability":     ft.Icons.SPELLCHECK_ROUNDED,
    "Numerical Ability":  ft.Icons.CALCULATE_ROUNDED,
    "Analytical Ability": ft.Icons.PSYCHOLOGY_ROUNDED,
    "General Information":ft.Icons.PUBLIC_ROUNDED,
}

SUBJECT_COLORS = {
    "Verbal Ability":     BLUE,
    "Numerical Ability":  "#7C3AED",
    "Analytical Ability": "#0891B2",
    "General Information":GREEN,
}

# ── CSE Exam Config ─────────────────────────────────────────────────
PASSING_SCORE = 0.80

EXAM_PARTS = {
    "Professional": {
        "total": 170,
        "duration_min": 190,
        "parts": [
            {"name": "Part I — Verbal & Reading",       "weight": 0.30,
             "categories": ["Vocabulary","Grammar","Reading Comprehension",
                            "Word Analogy","Paragraph Organization"]},
            {"name": "Part II — Clerical & Logic",      "weight": 0.35,
             "categories": ["Number Series","Analogies",
                            "Logical Reasoning","Data Interpretation"]},
            {"name": "Part III — Numerical Ability",    "weight": 0.30,
             "categories": ["Numerical Reasoning","Word Problems",
                            "Data Sufficiency"]},
            {"name": "Part IV — General Information",   "weight": 0.05,
             "categories": ["Philippine Constitution","RA 6713",
                            "Human Rights","Environmental Management"]},
        ]
    },
    "Sub-Professional": {
        "total": 165,
        "duration_min": 160,
        "parts": [
            {"name": "Part I — Verbal",            "weight": 0.30,
             "categories": ["Vocabulary","Grammar","Reading Comprehension"]},
            {"name": "Part II — Clerical Ability", "weight": 0.35,
             "categories": ["Filing","Coding","Records Management",
                            "Office Procedures"]},
            {"name": "Part III — Numerical",       "weight": 0.30,
             "categories": ["Numerical Reasoning","Word Problems"]},
            {"name": "Part IV — General Info",     "weight": 0.05,
             "categories": ["Philippine Constitution","RA 6713",
                            "General Knowledge"]},
        ]
    }
}
