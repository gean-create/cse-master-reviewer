# CSE Master Reviewer

A full-featured Philippine Civil Service Exam reviewer app built with Python + Flet.

**Features**
- 60 original CSE-style practice questions across 4 subjects
- Structured lessons, flashcard decks, and practice quizzes per subject
- Timed 40-question mock exam with question navigator
- Readiness score ring, streak tracking, and analytics
- Wrong-answer review with one-tap retake
- 8 achievements, local profile, progress persistence
- Runs on the web and builds to an Android APK

---

## Run Locally

```bash
pip install flet
python main.py
```

Then open http://localhost:8080 in your browser.
On mobile: open the same URL on your phone while on the same Wi-Fi.

---

## Deploy to the Web (Public URL)

### Option A — Render (free tier, easiest)

1. Push this folder to a GitHub repo.
2. Go to https://render.com → New → Web Service → connect your repo.
3. Set:
   - **Build command:** `pip install flet`
   - **Start command:** `python main.py`
   - **Port:** `8080`
4. Click Deploy. You'll get a public URL like `https://cse-reviewer.onrender.com`.

### Option B — Railway

1. Push to GitHub. Go to https://railway.app → New → GitHub repo.
2. Add env var `PORT=8080`.
3. Deploy — Railway auto-detects Python and runs `python main.py`.

### Option C — Replit (instant, no signup needed)

1. Create a new Replit → Import from GitHub.
2. In the shell: `pip install flet && python main.py`
3. Replit exposes the port automatically.

---

## Build Android APK

You need Flutter + Android SDK installed on your own machine.

```bash
# Install Flet CLI
pip install flet

# Inside this project folder:
flet build apk

# The APK is output to:
# build/apk/app-release.apk
```

Install it on your Android device:
```bash
adb install build/apk/app-release.apk
```

Or transfer the APK file to your phone and tap to install
(enable "Install from unknown sources" in Android settings first).

### Requirements for APK build
- Python 3.9+
- Flutter 3.x (https://flutter.dev/docs/get-started/install)
- Android Studio + SDK (https://developer.android.com/studio)
- Java 17+

---

## Project Structure

```
cse_app/
  main.py           # Entry point and router
  theme.py          # Design tokens (colors, fonts, radii)
  state.py          # App state + SharedPreferences persistence
  components.py     # Reusable UI components
  requirements.txt
  data/
    questions.py    # 60 CSE-style questions
    lessons.py      # Lesson content per subject
    flashcards.py   # Flashcard decks per subject
  screens/
    splash.py       # Auto-routing splash
    onboarding.py   # 3-slide intro
    login.py        # Local profile creation
    home.py         # Dashboard
    topics.py       # Subject selection
    lesson.py       # Lesson reader
    flashcards.py   # Flip-card study
    quiz.py         # Practice quiz with instant feedback
    mock_exam.py    # Timed full exam
    results.py      # Score + breakdown
    analytics.py    # Stats + weekly chart
    review.py       # Wrong-answer review
    achievements.py # Badge grid
    profile.py      # Settings + logout
```

---

## Notes

- **Login is local only** — the profile is stored on the device, not a remote server.
  This is intentional: no backend is needed for an offline reviewer app.
- **Flet version:** tested on 0.85.3. Requires ≥ 0.85.0.
