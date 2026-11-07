import datetime
import secrets
from http.cookies import SimpleCookie
from typing import Dict, Optional, Tuple


class SessionManager:

    def __init__(self, expiry_seconds: int = 3600):
        self.expiry_seconds = expiry_seconds
        # Storage mapping token -> (user_id, expiration_timestamp)
        self._sessions: Dict[str, Tuple[str, datetime.datetime]] = {}

    def create_session(self, user_id: str) -> Tuple[str, str]:
        """Generates a secure session token and returns (token, Set-Cookie header)."""
        # Cryptographically secure random token (256 bits of entropy)
        token = secrets.token_urlsafe(32)

        now = datetime.datetime.now(datetime.timezone.utc)
        expires_at = now + datetime.timedelta(seconds=self.expiry_seconds)

        # Store session server-side
        self._sessions[token] = (user_id, expires_at)

        # Build secure HTTP cookie
        cookie = SimpleCookie()
        cookie["session_id"] = token
        cookie["session_id"]["httponly"] = True
        cookie["session_id"]["secure"] = True
        cookie["session_id"]["samesite"] = "Strict"
        cookie["session_id"]["path"] = "/"
        cookie["session_id"]["max-age"] = self.expiry_seconds

        return token, cookie.output(header="Set-Cookie:")

    def validate_session(self, token: str) -> Optional[str]:
        """Validates token.

        Returns user_id if valid and unexpired, otherwise None.
        """
        if not token or token not in self._sessions:
            return None

        user_id, expires_at = self._sessions[token]
        now = datetime.datetime.now(datetime.timezone.utc)

        # Check expiration
        if now > expires_at:
            self.revoke_session(token)
            return None

        return user_id

    def revoke_session(self, token: str) -> None:
        """Deletes session (used for logout or expired session cleanup)."""
        self._sessions.pop(token, None)
