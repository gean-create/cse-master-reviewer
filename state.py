"""
Application state — CSE Master Reviewer.
Wraps Flet SharedPreferences for offline-first persistence.
Single source of truth; passed by reference to all screens.
"""
import json
import datetime as dt
import flet as ft

from data.questions import QUESTIONS, by_ids
from data.flashcards import FLASHCARDS
from theme import SUBJECTS

STORAGE_KEY = "cse_master_reviewer_state_v1"
MAX_WRONG_ANSWERS = 500   # cap to prevent unbounded growth


def _today_str():
    return dt.date.today().isoformat()


def _now_str():
    return dt.datetime.now().isoformat(timespec="seconds")


def _default_data():
    return {
        "profile": None,
        "subjects": {
            s: {"lesson_done": False, "flashcards_mastered": [], "flashcards_learning": []}
            for s in SUBJECTS
        },
        "quiz_history": [],
        "exam_history": [],
        "wrong_answers": [],
        "streak": {"count": 0, "last_date": None},
        "onboarded": False,
        "subscription": {},
    }


ACHIEVEMENT_DEFS = [
    {"id": "first_quiz",    "title": "First Steps",        "desc": "Complete your first practice quiz.",       "icon": "QUIZ_ROUNDED"},
    {"id": "streak_3",      "title": "3-Day Streak",       "desc": "Study 3 days in a row.",                  "icon": "LOCAL_FIRE_DEPARTMENT_ROUNDED"},
    {"id": "streak_7",      "title": "Week Warrior",       "desc": "Study 7 days in a row.",                  "icon": "WHATSHOT_ROUNDED"},
    {"id": "quiz_master",   "title": "Quiz Master",        "desc": "Complete 10 practice quizzes.",           "icon": "MILITARY_TECH_ROUNDED"},
    {"id": "perfect_score", "title": "Perfect Score",      "desc": "Score 100% on any quiz or exam.",         "icon": "STAR_ROUNDED"},
    {"id": "exam_passed",   "title": "Exam Ready",         "desc": "Pass a mock exam (80%+).",                "icon": "EMOJI_EVENTS_ROUNDED"},
    {"id": "all_rounder",   "title": "All-Rounder",        "desc": "Finish the lesson in all 4 subjects.",    "icon": "SCHOOL_ROUNDED"},
    {"id": "flash_16",      "title": "Flashcard Fanatic",  "desc": "Master 16 flashcards.",                   "icon": "BOLT_ROUNDED"},
]


class AppState:
    # BUG FIX #1: page is required — pass it from main() after page setup
    def __init__(self, page: ft.Page):
        self.page = page
        self.prefs = ft.SharedPreferences()
        self.data = _default_data()
        # ephemeral session state (not persisted)
        self.current_subject = SUBJECTS[0]
        self.active_question_ids = []
        self.active_mode = "practice"
        self.last_result = None
        self.exam_config = None   # set by exam config screen

    # ------------------------------------------------------------------ IO
    async def load(self):
        try:
            raw = await self.prefs.get(STORAGE_KEY)
        except Exception:
            raw = None
        if raw:
            try:
                loaded = json.loads(raw)
                defaults = _default_data()
                defaults.update(loaded)
                for s in SUBJECTS:
                    defaults["subjects"].setdefault(
                        s, {"lesson_done": False, "flashcards_mastered": [], "flashcards_learning": []}
                    )
                self.data = defaults
            except Exception:
                self.data = _default_data()

    async def save(self):
        try:
            await self.prefs.set(STORAGE_KEY, json.dumps(self.data))
        except Exception:
            pass

    def save_bg(self):
        self.page.run_task(self.save)

    # ------------------------------------------------------------ profile
    @property
    def onboarded(self):
        return self.data.get("onboarded", False)

    @onboarded.setter
    def onboarded(self, val: bool):
        self.data["onboarded"] = val

    @property
    def is_logged_in(self):
        return self.data.get("profile") is not None

    @property
    def name(self):
        p = self.data.get("profile")
        return p["name"] if p else "Reviewer"

    @property
    def track(self):
        p = self.data.get("profile")
        return p.get("track", "Professional") if p else "Professional"

    def create_profile(self, name: str, track: str, email: str = "", user_id: str = ""):
        import hashlib
        uid = user_id or hashlib.md5((email or name).encode()).hexdigest()[:12]
        self.data["profile"] = {
            "name": name.strip() or "Reviewer",
            "track": track,
            "email": email.strip().lower(),
            "user_id": uid,
        }
        self.save_bg()

    def log_out(self):
        self.data = _default_data()
        # save synchronously via run_task before navigating
        self.save_bg()

    # ---------------------------------------------------------- subjects
    def subject_state(self, subject):
        return self.data["subjects"][subject]

    def mark_lesson_done(self, subject):
        self.subject_state(subject)["lesson_done"] = True
        self._touch_streak()
        self.save_bg()

    def mark_flashcard(self, subject, card_id, mastered: bool):
        st = self.subject_state(subject)
        for bucket in ("flashcards_mastered", "flashcards_learning"):
            if card_id in st[bucket]:
                st[bucket].remove(card_id)
        target = "flashcards_mastered" if mastered else "flashcards_learning"
        st[target].append(card_id)
        self._touch_streak()
        self.save_bg()

    def subject_accuracy(self, subject):
        attempts = [q for q in self.data["quiz_history"] if q.get("subject") == subject]
        if not attempts:
            return None
        correct = sum(a["correct"] for a in attempts)
        total = sum(a["total"] for a in attempts)
        return correct / total if total else None

    def subject_mastery_pct(self, subject):
        """Returns float 0.0–1.0."""
        st = self.subject_state(subject)
        deck_size = max(len(FLASHCARDS.get(subject, [])), 1)
        lesson_component = 0.25 if st["lesson_done"] else 0.0
        flash_component = 0.25 * (len(st["flashcards_mastered"]) / deck_size)
        acc = self.subject_accuracy(subject)
        quiz_component = 0.50 * acc if acc is not None else 0.0
        return min(1.0, lesson_component + flash_component + quiz_component)

    def readiness_score(self):
        """Returns float 0.0–1.0."""
        scores = [self.subject_mastery_pct(s) for s in SUBJECTS]
        return sum(scores) / len(scores) if scores else 0.0

    def overall_accuracy(self):
        all_attempts = self.data["quiz_history"] + [
            {"correct": e["correct"], "total": e["total"]} for e in self.data["exam_history"]
        ]
        total = sum(a["total"] for a in all_attempts)
        correct = sum(a["correct"] for a in all_attempts)
        return correct / total if total else None

    def strongest_weakest(self):
        scored = [(s, self.subject_accuracy(s)) for s in SUBJECTS if self.subject_accuracy(s) is not None]
        if not scored:
            return None, None
        return max(scored, key=lambda x: x[1]), min(scored, key=lambda x: x[1])

    def total_questions_answered(self):
        return (sum(a["total"] for a in self.data["quiz_history"]) +
                sum(e["total"] for e in self.data["exam_history"]))

    # ---------------------------------------------------------- grading
    # BUG FIX #2: grade() is now PURE — it does NOT write wrong_answers.
    # Only _record_wrongs() writes wrong_answers, called once per attempt.
    def grade(self, question_ids, answers: dict):
        """Pure scoring — returns (correct, total, breakdown). No side effects."""
        qs = by_ids(question_ids)
        correct = 0
        breakdown = {}
        for q in qs:
            subj = q.get("subject", "General Information")
            breakdown.setdefault(subj, {"correct": 0, "total": 0})
            breakdown[subj]["total"] += 1
            if answers.get(q["id"]) == q["answer"]:
                correct += 1
                breakdown[subj]["correct"] += 1
        return correct, len(qs), breakdown

    def _record_wrongs(self, question_ids, answers: dict):
        """Write wrong answers to history — called exactly once per attempt."""
        qs = by_ids(question_ids)
        new_wrongs = []
        for q in qs:
            chosen = answers.get(q["id"])
            if chosen != q["answer"]:
                new_wrongs.append({
                    "qid": q["id"],
                    "subject": q.get("subject", "General Information"),
                    "category": q.get("category", ""),
                    "your_idx": chosen,
                    "correct_idx": q["answer"],
                    "date": _now_str(),
                })
        # prepend and cap list
        self.data["wrong_answers"] = (new_wrongs + self.data["wrong_answers"])[:MAX_WRONG_ANSWERS]

    def record_quiz_attempt(self, subject, question_ids, answers, mode="practice"):
        correct, total, breakdown = self.grade(question_ids, answers)
        self._record_wrongs(question_ids, answers)
        self.data["quiz_history"].insert(0, {
            "date": _now_str(), "subject": subject, "mode": mode,
            "total": total, "correct": correct,
            "question_ids": list(question_ids),
        })
        self._touch_streak()
        self.save_bg()
        return correct, total, breakdown

    def record_exam_attempt(self, question_ids, answers, duration_sec, track="Professional"):
        correct, total, breakdown = self.grade(question_ids, answers)
        self._record_wrongs(question_ids, answers)
        self.data["exam_history"].insert(0, {
            "date": _now_str(), "total": total, "correct": correct,
            "duration_sec": duration_sec, "breakdown": breakdown,
            "question_ids": list(question_ids), "track": track,
        })
        self._touch_streak()
        self.save_bg()
        return correct, total, breakdown

    # ------------------------------------------------------------ streak
    def _touch_streak(self):
        today = _today_str()
        streak = self.data["streak"]
        last = streak.get("last_date")
        if last == today:
            return
        yesterday = (dt.date.today() - dt.timedelta(days=1)).isoformat()
        streak["count"] = (streak["count"] + 1) if last == yesterday else 1
        streak["last_date"] = today

    @property
    def streak_count(self):
        return self.data["streak"]["count"]

    # ------------------------------------------------------- achievements
    def unlocked_achievements(self):
        unlocked = set()
        qh = self.data["quiz_history"]
        eh = self.data["exam_history"]
        if qh:
            unlocked.add("first_quiz")
        if self.streak_count >= 3:
            unlocked.add("streak_3")
        if self.streak_count >= 7:
            unlocked.add("streak_7")
        if len(qh) >= 10:
            unlocked.add("quiz_master")
        if any(a["total"] > 0 and a["correct"] == a["total"] for a in qh + eh):
            unlocked.add("perfect_score")
        if any(e["total"] > 0 and e["correct"] / e["total"] >= 0.8 for e in eh):
            unlocked.add("exam_passed")
        if all(self.subject_state(s)["lesson_done"] for s in SUBJECTS):
            unlocked.add("all_rounder")
        if sum(len(self.subject_state(s)["flashcards_mastered"]) for s in SUBJECTS) >= 16:
            unlocked.add("flash_16")
        return unlocked

    # --------------------------------------------------------- analytics
    def weekly_activity(self):
        counts = {}
        for a in self.data["quiz_history"] + self.data["exam_history"]:
            d = a["date"][:10]
            counts[d] = counts.get(d, 0) + 1
        out = []
        for i in range(6, -1, -1):
            day = dt.date.today() - dt.timedelta(days=i)
            out.append((day.strftime("%a")[0], counts.get(day.isoformat(), 0)))
        return out


    # -------------------------------------------------------- subscription
    def subscription_status(self):
        from subscription_service import get_trial_status
        return get_trial_status(self.data)

    def can_access_premium(self) -> bool:
        return self.subscription_status()["can_access_premium"]

    def start_trial_if_new(self):
        from subscription_service import start_trial
        start_trial(self.data)
        self.save_bg()

    def reset_progress(self):
        profile = self.data.get("profile")
        self.data = _default_data()
        self.data["profile"] = profile
        self.data["onboarded"] = True
        self.save_bg()
