import secrets
import time
from typing import Optional


class SessionManager:

    def __init__(self, default_ttl: int = 3600):
        self._sessions = {}
        self.default_ttl = default_ttl

    def create_session(self, user_id: str, ttl: Optional[int] = None) -> str:
        """Creates and stores a secure session token for a logged-in user."""
        token = secrets.token_urlsafe(32)
        duration = ttl if ttl is not None else self.default_ttl
        expires_at = time.time() + duration

        self._sessions[token] = {"user_id": user_id, "expires_at": expires_at}
        return token

    def validate_session(self, token: str) -> Optional[str]:
        """Validates a session token.

        Returns the user_id if valid, or None if invalid/expired.
        """
        session_data = self._sessions.get(token)
        if not session_data:
            return None

        if time.time() > session_data["expires_at"]:
            del self._sessions[token]  # Clean up expired token
            return None

        return session_data["user_id"]

    def revoke_session(self, token: str) -> bool:
        """Revokes a session token (logout)."""
        return self._sessions.pop(token, None) is not None
