from typing import Optional
from uuid import uuid4


def generate_user_token() -> str:
    """Generate a unique user token"""
    return uuid4().hex


class Session():
    """Stores the values of a session"""

    def __init__(self, user_id: str, user_token: str, firebase_token: str):
        """Initialize a Session from values"""
        self.user_id = user_id
        self.user_token = user_token
        self.firebase_token = firebase_token


class Sessions():
    """Stores the table of user tokens to Sessions"""

    def __init__(self):
        """Initialize the underlying dictionary"""
        self.sessions = {}

    def add(self, user_id: str, firebase_token: str) -> Session:
        """
        Creates and stores a new session, and then returns the session
        Calls `generate_user_token` to create a user token
        """
        user_token = generate_user_token()
        session = Session(user_id, user_token, firebase_token)
        self.sessions[user_token] = session
        return session

    def get(self, user_token: str) -> Optional[Session]:
        """
        Returns the Session corresponding to the given user token
        Returns None if no such session exists
        """
        return self.sessions.get(user_token)

    def remove(self, user_token: str) -> None:
        """
        Removes a Session corresponding to the given user token
        Whether such session exists or not, return nothing
        """
        self.sessions.pop(user_token, None)

    def reset(self) -> None:
        """Reset the sessions instance (used for testing)"""
        self.sessions = {}
