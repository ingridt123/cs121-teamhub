import json

import requests


class Auth():
    """
    AD HOC: Weak copy of Auth class from Pyrebase library

    In order to get around annoying incompatabilty of Pyrebase with the
    official Google Cloud libraries, as well as with the Firebase emulator
    """

    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()

    def sign_in_with_email_and_password(self, email, password):
        """Signs a user in with email and password"""
        request_url = "{}:signInWithPassword?key={}".format(
            self.base_url,
            self.api_key)
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        data = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": True
        })
        res = self.session.post(request_url, headers=headers, data=data)
        res.raise_for_status()
        return res.json()

    def create_user_with_email_and_password(self, email, password):
        """Creates a user with email and password"""
        request_url = "{}:signUp?key={}".format(
            self.base_url,
            self.api_key)
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        data = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": True
        })
        res = self.session.post(request_url, headers=headers, data=data)
        res.raise_for_status()
        return res.json()
