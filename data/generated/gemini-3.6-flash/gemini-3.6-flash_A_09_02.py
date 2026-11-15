import secrets
import time
from typing import Optional


class SessionManager:

    def __init__(self, ttl_seconds: int = 3600):
        self.ttl_seconds = ttl_seconds
        self._sessions = {}

    def create_session(self, user_id: str) -> str:
        """Generates a secure session token for a given user."""
        token = secrets.token_urlsafe(32)
        expiration = time.time() + self.ttl_seconds
        self._sessions[token] = {"user_id": user_id, "expires_at": expiration}
        return token

    def check_session(self, token: str) -> Optional[str]:
        """Validates the session token. Returns user_id if valid, None if invalid or expired."""
        session = self._sessions.get(token)
        if not session:
            return None

        if time.time() > session["expires_at"]:
            self.revoke_session(token)
            return None

        return session["user_id"]

    def revoke_session(self, token: str) -> None:
        """Deletes a session token (e.g., on logout)."""
        self._sessions.pop(token, None)


# Example usage:
if __name__ == "__main__":
    manager = SessionManager(ttl_seconds=1800)  # 30-minute session expiration

    # 1. Login & Token Creation
    user_id = "user_12345"
    session_token = manager.create_session(user_id)
    print(f"Created Token: {session_token}")

    # 2. Authenticate subsequent request
    authenticated_user = manager.check_session(session_token)
    if authenticated_user:
        print(f"Access granted for: {authenticated_user}")
    else:
        print("Invalid or expired session.")

    # 3. Logout
    manager.revoke_session(session_token)
    print(f"Post-logout Check: {manager.check_session(session_token)}")
