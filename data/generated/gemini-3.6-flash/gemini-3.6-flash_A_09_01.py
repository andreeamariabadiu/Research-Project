import secrets
import time


class SessionManager:
    def __init__(self, default_ttl: int = 3600):
        self.sessions = {}
        self.default_ttl = default_ttl

    def create_session(self, user_id: str, ttl: int = None) -> str:

        token = secrets.token_urlsafe(32)
        duration = ttl if ttl is not None else self.default_ttl
        expires_at = time.time() + duration

        self.sessions[token] = {"user_id": user_id, "expires_at": expires_at}
        return token

    def check_session(self, token: str):

        session = self.sessions.get(token)
        if not session:
            return None

        if time.time() > session["expires_at"]:
            del self.sessions[token]
            return None

        return session["user_id"]

    def revoke_session(self, token: str) -> bool:

        if token in self.sessions:
            del self.sessions[token]
            return True
        return False
