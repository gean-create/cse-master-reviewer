"""
CSE Master Reviewer 2026 — 100% FREE for all Filipino public servants.
No subscription. No payment. No limits. Forever free.

Exam dates are AUTO-CALCULATED based on official CSC pattern:
- 1st exam: 2nd Sunday of March every year
- 2nd exam: 2nd Sunday of August every year
(Official CSC pattern confirmed for 2026 onwards)
"""
import datetime as dt

APP_VERSION = "2026.1.0"
APP_NAME = "Civil Service Reviewer 2026"
IS_FREE = True


def _second_sunday(year: int, month: int) -> dt.date:
    """Calculate the 2nd Sunday of a given month and year."""
    # Find first day of month
    first = dt.date(year, month, 1)
    # Find first Sunday (weekday 6 = Sunday)
    days_until_sunday = (6 - first.weekday()) % 7
    first_sunday = first + dt.timedelta(days=days_until_sunday)
    # Second Sunday = first Sunday + 7 days
    return first_sunday + dt.timedelta(days=7)


def _application_period(exam_date: dt.date):
    """Estimate application period: ~10-12 weeks before exam."""
    app_end = exam_date - dt.timedelta(weeks=8)
    app_start = app_end - dt.timedelta(weeks=4)
    return app_start, app_end


def get_exam_schedule(years_ahead: int = 3) -> list:
    """
    Auto-generate CSE exam schedule for current and future years.
    Returns list of exam dicts sorted by date.
    """
    today = dt.date.today()
    current_year = today.year
    exams = []

    for year in range(current_year - 1, current_year + years_ahead + 1):
        # 1st exam: 2nd Sunday of March
        march_date = _second_sunday(year, 3)
        app_start, app_end = _application_period(march_date)
        exams.append({
            "date": march_date.isoformat(),
            "label": f"March {year} CSE-PPT",
            "description": "Professional & Sub-Professional Levels",
            "application_start": app_start.isoformat(),
            "application_end": app_end.isoformat(),
            "year": year,
            "batch": 1,
        })

        # 2nd exam: 2nd Sunday of August
        august_date = _second_sunday(year, 8)
        app_start2, app_end2 = _application_period(august_date)
        exams.append({
            "date": august_date.isoformat(),
            "label": f"August {year} CSE-PPT",
            "description": "Professional & Sub-Professional Levels",
            "application_start": app_start2.isoformat(),
            "application_end": app_end2.isoformat(),
            "year": year,
            "batch": 2,
        })

    # Sort by date
    exams.sort(key=lambda x: x["date"])
    return exams


def get_upcoming_exams(count: int = 3) -> list:
    """Get next N upcoming exam dates from today."""
    today = dt.date.today().isoformat()
    all_exams = get_exam_schedule(years_ahead=3)
    upcoming = [e for e in all_exams if e["date"] >= today]
    return upcoming[:count]


def get_next_exam() -> dict | None:
    """Get the single next upcoming exam."""
    upcoming = get_upcoming_exams(1)
    return upcoming[0] if upcoming else None


def days_until_exam(exam: dict) -> int:
    """Days remaining until a specific exam."""
    try:
        exam_date = dt.date.fromisoformat(exam["date"])
        return (exam_date - dt.date.today()).days
    except Exception:
        return 0


# Known confirmed dates (override auto-calculation for verified dates)
CONFIRMED_DATES = {
    "2026-03-08": "March 8, 2026 CSE-PPT (Confirmed by CSC)",
    "2026-08-09": "August 9, 2026 CSE-PPT (Confirmed by CSC)",
}

# Pre-compute for quick access
CSE_EXAM_DATES = get_exam_schedule()
