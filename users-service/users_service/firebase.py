import config
import firebase


def connect_auth():
    """Creates a authentication connection"""
    return firebase.Auth(
        config.FIREBASE_AUTH_URL,
        config.API_KEY)


def connect_db(firebase_token=None):
    """Creates a database connection given a Firebase token"""
    return firebase.Database(
        firebase_token,
        config.FIRESTORE_URL,
        config.API_KEY)
