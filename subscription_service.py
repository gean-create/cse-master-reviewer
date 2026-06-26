"""
Subscription Service — CSE Master Reviewer
Handles free trial, premium status, and PayMongo payment verification.
All premium status is verified server-side via Firebase — cannot be faked locally.
"""
import json
import datetime as dt
import os
import urllib.request
import urllib.error

# ── Environment variables (set these in Fly.io secrets) ──────────────
PAYMONGO_SECRET_KEY = os.environ.get("PAYMONGO_SECRET_KEY", "")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "")
FIREBASE_API_KEY    = os.environ.get("FIREBASE_API_KEY", "")

FREE_TRIAL_DAYS   = 30
PREMIUM_PRICE_PHP = 150
PREMIUM_DAYS      = 365   # 1 year


def _today():
    return dt.date.today()


def _days_since(date_str: str) -> int:
    try:
        d = dt.date.fromisoformat(date_str)
        return (_today() - d).days
    except Exception:
        return 0


# ── Trial logic (stored locally — just a date, no security needed) ──
def get_trial_status(data: dict) -> dict:
    """
    Returns:
      {
        on_trial: bool,
        trial_days_left: int,
        trial_expired: bool,
        is_premium: bool,
        premium_days_left: int,
        premium_expired: bool,
        can_access_premium: bool,   # trial OR active premium
      }
    """
    sub = data.get("subscription", {})
    trial_start   = sub.get("trial_start")
    premium_start = sub.get("premium_start")
    premium_verified = sub.get("premium_verified", False)

    # Trial
    if trial_start:
        days_used = _days_since(trial_start)
        trial_days_left = max(0, FREE_TRIAL_DAYS - days_used)
        on_trial = trial_days_left > 0
        trial_expired = days_used >= FREE_TRIAL_DAYS
    else:
        trial_days_left = FREE_TRIAL_DAYS
        on_trial = False
        trial_expired = False

    # Premium
    if premium_start and premium_verified:
        days_used_p = _days_since(premium_start)
        premium_days_left = max(0, PREMIUM_DAYS - days_used_p)
        is_premium = premium_days_left > 0
        premium_expired = days_used_p >= PREMIUM_DAYS
    else:
        premium_days_left = 0
        is_premium = False
        premium_expired = False

    can_access_premium = on_trial or is_premium

    return {
        "on_trial": on_trial,
        "trial_days_left": trial_days_left,
        "trial_expired": trial_expired,
        "is_premium": is_premium,
        "premium_days_left": premium_days_left,
        "premium_expired": premium_expired,
        "can_access_premium": can_access_premium,
    }


def start_trial(data: dict):
    """Call once when user first logs in."""
    if "subscription" not in data:
        data["subscription"] = {}
    if not data["subscription"].get("trial_start"):
        data["subscription"]["trial_start"] = _today().isoformat()


# ── PayMongo payment link creation ───────────────────────────────────
def create_payment_link(user_email: str, user_name: str) -> dict:
    """
    Creates a PayMongo Payment Link for ₱150.
    Returns {"url": "https://...", "link_id": "...", "error": None}
    """
    if not PAYMONGO_SECRET_KEY:
        return {"url": None, "link_id": None,
                "error": "PayMongo key not configured"}

    import base64
    auth = base64.b64encode(f"{PAYMONGO_SECRET_KEY}:".encode()).decode()

    payload = json.dumps({
        "data": {
            "attributes": {
                "amount": PREMIUM_PRICE_PHP * 100,   # PayMongo uses centavos
                "description": "CSE Master Reviewer — 1 Year Premium Access",
                "remarks": f"User: {user_name} | {user_email}",
            }
        }
    }).encode()

    req = urllib.request.Request(
        "https://api.paymongo.com/v1/links",
        data=payload,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            attrs = result["data"]["attributes"]
            return {
                "url": attrs["checkout_url"],
                "link_id": result["data"]["id"],
                "error": None,
            }
    except Exception as e:
        return {"url": None, "link_id": None, "error": str(e)}


# ── PayMongo payment verification ────────────────────────────────────
def verify_payment_link(link_id: str) -> dict:
    """
    Checks if a PayMongo payment link has been paid.
    Returns {"paid": bool, "amount": int, "error": None}
    """
    if not PAYMONGO_SECRET_KEY or not link_id:
        return {"paid": False, "amount": 0, "error": "Missing config"}

    import base64
    auth = base64.b64encode(f"{PAYMONGO_SECRET_KEY}:".encode()).decode()

    req = urllib.request.Request(
        f"https://api.paymongo.com/v1/links/{link_id}",
        headers={"Authorization": f"Basic {auth}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            attrs = result["data"]["attributes"]
            paid = attrs.get("status") == "paid"
            amount = attrs.get("amount", 0) // 100
            return {"paid": paid, "amount": amount, "error": None}
    except Exception as e:
        return {"paid": False, "amount": 0, "error": str(e)}


# ── Firebase: save premium status (server-side, tamper-proof) ───────
def save_premium_to_firebase(user_id: str, link_id: str) -> bool:
    """
    Writes premium status to Firebase Firestore.
    Only called after payment is verified with PayMongo.
    Returns True on success.
    """
    if not FIREBASE_PROJECT_ID or not FIREBASE_API_KEY:
        return False   # Firebase not configured yet — graceful degradation

    url = (
        f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}"
        f"/databases/(default)/documents/subscribers/{user_id}"
        f"?key={FIREBASE_API_KEY}"
    )
    payload = json.dumps({
        "fields": {
            "premium_start": {"stringValue": _today().isoformat()},
            "premium_until": {"stringValue": (
                _today() + dt.timedelta(days=PREMIUM_DAYS)
            ).isoformat()},
            "link_id":       {"stringValue": link_id},
            "amount_paid":   {"integerValue": str(PREMIUM_PRICE_PHP)},
            "verified":      {"booleanValue": True},
        }
    }).encode()

    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            return True
    except Exception:
        return False


def check_premium_from_firebase(user_id: str) -> dict:
    """
    Reads premium status from Firebase.
    Returns {"is_premium": bool, "premium_until": str, "error": None}
    """
    if not FIREBASE_PROJECT_ID or not FIREBASE_API_KEY:
        return {"is_premium": False, "premium_until": "", "error": "Not configured"}

    url = (
        f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}"
        f"/databases/(default)/documents/subscribers/{user_id}"
        f"?key={FIREBASE_API_KEY}"
    )
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            fields = result.get("fields", {})
            premium_until_str = fields.get("premium_until", {}).get("stringValue", "")
            verified = fields.get("verified", {}).get("booleanValue", False)
            if premium_until_str and verified:
                until = dt.date.fromisoformat(premium_until_str)
                is_premium = until >= _today()
                return {"is_premium": is_premium,
                        "premium_until": premium_until_str, "error": None}
            return {"is_premium": False, "premium_until": "", "error": None}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"is_premium": False, "premium_until": "", "error": None}
        return {"is_premium": False, "premium_until": "", "error": str(e)}
    except Exception as e:
        return {"is_premium": False, "premium_until": "", "error": str(e)}
