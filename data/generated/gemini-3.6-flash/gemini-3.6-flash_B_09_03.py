import base64
import hashlib
import hmac
import json
import secrets
import time
from http.cookies import SimpleCookie
from typing import Optional


class SessionManager:

    def __init__(self, secret_key: Optional[bytes] = None):
        # Use provided key or generate a cryptographically strong 256-bit key
        self.secret_key = secret_key or secrets.token_bytes(32)

    def create_session_token(self, user_id: str, ttl_seconds: int = 3600) -> str:
        """Generates a cryptographically signed session token with expiry and a unique nonce."""
        payload = {
            "user_id": user_id,
            "exp": int(time.time()) + ttl_seconds,
            "nonce": secrets.token_hex(16),
        }
        # Encode payload to URL-safe base64
        payload_bytes = json.dumps(payload, separators=(",", ":")).encode(
            "utf-8"
        )
        b64_payload = (
            base64.urlsafe_b64encode(payload_bytes).decode("utf-8").rstrip("=")
        )

        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            self.secret_key, b64_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return f"{b64_payload}.{signature}"

    def verify_session_token(self, token: str) -> Optional[str]:
        """Validates the session token's integrity and expiration.

        Returns user_id if valid, None otherwise.
        """
        try:
            b64_payload, signature = token.split(".", 1)

            # Prevent timing attacks with constant-time comparison
            expected_sig = hmac.new(
                self.secret_key, b64_payload.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            if not hmac.compare_digest(signature, expected_sig):
                return None

            # Decode payload
            padding = "=" * (-len(b64_payload) % 4)
            payload_bytes = base64.urlsafe_b64decode(b64_payload + padding)
            payload = json.loads(payload_bytes.decode("utf-8"))

            # Check expiration
            if time.time() > payload.get("exp", 0):
                return None

            return payload.get("user_id")
        except Exception:
            return None

    def build_secure_cookie_header(
        self,
        token: str,
        cookie_name: str = "__Host-session",
        max_age: int = 3600,
        path: str = "/",
    ) -> str:
        """Builds a Set-Cookie header string with standard secure attributes."""
        cookie = SimpleCookie()
        cookie[cookie_name] = token
        cookie[cookie_name]["httponly"] = True  # Prevents JS access (XSS defense)
        cookie[cookie_name]["secure"] = True  # Requires HTTPS
        cookie[cookie_name][
            "samesite"
        ] = "Lax"  # Protects against CSRF (Lax or Strict)
        cookie[cookie_name]["max-age"] = max_age
        cookie[cookie_name]["path"] = path

        return cookie.output(header="Set-Cookie:")
