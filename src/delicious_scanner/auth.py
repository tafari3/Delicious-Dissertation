from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import time
from urllib.parse import quote

from delicious_scanner.config import settings

PBKDF2_ITERATIONS = 600_000
COOKIE_NAME = "delicious_session"


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    actual_salt = salt or secrets.token_bytes(18)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), actual_salt, PBKDF2_ITERATIONS)
    salt_text = base64.urlsafe_b64encode(actual_salt).decode("ascii").rstrip("=")
    digest_text = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt_text}${digest_text}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations_text, salt_text, digest_text = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iterations_text)
        salt = base64.urlsafe_b64decode(salt_text + "=" * (-len(salt_text) % 4))
        expected = base64.urlsafe_b64decode(digest_text + "=" * (-len(digest_text) % 4))
    except (ValueError, TypeError):
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(actual, expected)


def _sign(payload: str) -> str:
    return hmac.new(
        settings.session_secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def make_session_cookie(username: str) -> str:
    expires = int(time.time()) + settings.session_ttl_seconds
    payload = f"{quote(username, safe='')}|{expires}"
    return f"{payload}|{_sign(payload)}"


def verify_session_cookie(cookie: str | None) -> str | None:
    if not cookie or not settings.session_secret:
        return None
    try:
        username, expires_text, signature = cookie.rsplit("|", 2)
        payload = f"{username}|{expires_text}"
        if not hmac.compare_digest(_sign(payload), signature):
            return None
        if int(expires_text) < int(time.time()):
            return None
        return username
    except (ValueError, TypeError):
        return None


def credentials_valid(username: str, password: str) -> bool:
    return (
        bool(settings.auth_username)
        and hmac.compare_digest(username, settings.auth_username)
        and bool(settings.auth_password_hash)
        and verify_password(password, settings.auth_password_hash)
    )
