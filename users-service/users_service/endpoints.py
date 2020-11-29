from typing import Union, Tuple, Optional

import connexion

from config import SCHOOL_ID
from users_service import firebase
from users_service.sessions import Sessions

# singleton instance of Sessionss
sessions = Sessions()

# response types
Response = Union[Optional[dict], Tuple[Optional[dict], int]]
RESPONSE_401 = (None, 401)


def login() -> Response:

    # get parameters from body
    email = connexion.request.json["email"]
    password = connexion.request.json["password"]

    # authenticate with email and password
    try:
        user = firebase.sign_in_with_email_and_password(email, password)
    except:
        return RESPONSE_401

    # create a session and return user token
    session = sessions.add(user["localId"], user["idToken"])
    return {"user_token": session.user_token}


def logout(user_token: str) -> Response:
    sessions.remove(user_token)


def check_token(user_token: str) -> Response:

    # get session from user token
    session = sessions.get(user_token)
    if not session:
        return RESPONSE_401

    # return firebase token
    return {"firebase_token": session.firebase_token}


def get_current_user(user_token: str) -> Response:

    # get session from user token
    session = sessions.get(user_token)
    if not session:
        return RESPONSE_401

    # get user from database
    try:
        db = firebase.connect_db(session.firebase_token)
        user = db.collection("users").document(session.user_id).get()
    except:
        return RESPONSE_401

    # return current user
    return user


def get_team_members(team_id: str, user_token: str) -> Response:

    # get session from user token
    session = sessions.get(user_token)
    if not session:
        return RESPONSE_401

    # get team members from database
    try:
        db = firebase.connect_db(session.firebase_token)
        members = db.collection("schools") \
            .document(SCHOOL_ID) \
            .collection("teams") \
            .document(team_id) \
            .collection("members") \
            .get()
    except:
        return RESPONSE_401

    # return team members
    return members or []
