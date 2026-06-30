"""
Civil Service Reviewer 2026 — Design System v2
Elegant Indigo/Navy + Gold palette, per brand reference.
"""
import flet as ft

# ── Brand Colors (new palette) ───────────────────────────────────────
NAVY       = "#0F172A"   # Navy Blue — primary dark
INDIGO     = "#1E3A8A"   # Indigo Blue — primary
BLUE       = "#1E3A8A"   # alias used across screens
BLUE_700   = "#0F172A"
BLUE_50    = "#EEF2FB"
BLUE_100   = "#D8E1F5"

GOLD       = "#D4AF37"   # Elegant Gold
GOLD_MUTED = "#C9A227"   # Muted Gold
GOLD_LIGHT = "#E6C766"
GOLD_50    = "#FBF6E6"

WHITE      = "#FFFFFF"
OFF_WHITE  = "#F8FAFC"
SURFACE    = "#FFFFFF"
APP_BG     = "#F8FAFC"   # Light Gray background

DARK       = "#0F172A"   # Dark Navy text
DARK_2     = "#1E293B"
GRAY       = "#334155"   # Slate
GRAY_SOFT  = "#64748B"   # Gray
BORDER     = "#E2E8F0"

GREEN      = "#15803D"
GREEN_50   = "#DCFCE7"
GREEN_100  = "#BBF7D0"
RED        = "#DC2626"
RED_50     = "#FEE2E2"
ORANGE     = "#C9A227"   # use muted gold for warning tone (avoids bright yellow)
ORANGE_50  = "#FBF6E6"

# ── Typography ──────────────────────────────────────────────────────
FONT_DISPLAY = "Georgia"
FONT_BODY    = "Arial"
FONT_URLS = {}

# ── Subjects ────────────────────────────────────────────────────────
SUBJECTS = ["Verbal Ability", "Numerical Ability",
            "Analytical Ability", "General Information"]

SUBJECT_ICONS = {
    "Verbal Ability":     ft.Icons.SPELLCHECK_ROUNDED,
    "Numerical Ability":  ft.Icons.CALCULATE_ROUNDED,
    "Analytical Ability": ft.Icons.PSYCHOLOGY_ROUNDED,
    "General Information":ft.Icons.PUBLIC_ROUNDED,
    "Clerical Ability":   ft.Icons.FOLDER_ROUNDED,
}

SUBJECT_COLORS = {
    "Verbal Ability":     INDIGO,
    "Numerical Ability":  "#7C3AED",
    "Analytical Ability": "#0E7490",
    "General Information":GREEN,
    "Clerical Ability":   GOLD_MUTED,
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
