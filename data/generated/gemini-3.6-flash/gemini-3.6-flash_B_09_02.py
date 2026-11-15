import base64
import hashlib
import hmac
from http.cookies import SimpleCookie
import json
import secrets
import time
from typing import Optional


class SessionManager:

    def __init__(self, secret_key: Optional[str] = None):
        # Use provided key or generate a cryptographically strong secret key
        self.secret_key = (
            secret_key.encode() if secret_key else secrets.token_bytes(32)
        )

    def create_session_token(self, user_id: str, max_age: int = 3600) -> str:
        """Generates a secure, signed token containing payload and expiration."""
        expiration = int(time.time()) + max_age
        payload = json.dumps({"user_id": user_id, "exp": expiration}).encode(
            "utf-8"
        )
        b64_payload = (
            base64.urlsafe_b64encode(payload).decode("utf-8").rstrip("=")
        )

        signature = hmac.new(
            self.secret_key, b64_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return f"{b64_payload}.{signature}"

    def verify_session_token(self, token: str) -> Optional[str]:
        """Validates the token signature and expiration.

        Returns user_id if valid.
        """
        try:
            b64_payload, signature = token.split(".")

            # Verify signature (timing-attack resistant comparison)
            expected_signature = hmac.new(
                self.secret_key, b64_payload.encode("utf-8"), hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, expected_signature):
                return None

            # Decode payload with padding correction
            padding = "=" * (-len(b64_payload) % 4)
            payload_bytes = base64.urlsafe_b64decode(b64_payload + padding)
            data = json.loads(payload_bytes.decode("utf-8"))

            # Check expiration
            if time.time() > data.get("exp", 0):
                return None

            return data.get("user_id")
        except (ValueError, KeyError, json.JSONDecodeError):
            return None

    def get_secure_cookie_header(
        self,
        cookie_name: str,
        user_id: str,
        max_age: int = 3600,
        domain: Optional[str] = None,
    ) -> str:
        """Creates a Set-Cookie header string with security flags."""
        token = self.create_session_token(user_id, max_age)

        cookie = SimpleCookie()
        cookie[cookie_name] = token
        cookie[cookie_name]["httponly"] = True
        cookie[cookie_name]["secure"] = True
        cookie[cookie_name]["samesite"] = "Lax"
        cookie[cookie_name]["path"] = "/"
        cookie[cookie_name]["max-age"] = max_age
        if domain:
            cookie[cookie_name]["domain"] = domain

        return cookie.output(header="Set-Cookie:")
