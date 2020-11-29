import json
import os

import requests

import config


def sign_in_with_email_and_password(email, password):
    """Signs a user in with email and password"""
    request_url = "{}:signInWithPassword?key={}".format(
        config.FIREBASE_AUTH_URL,
        config.API_KEY)
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    data = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    res = requests.post(request_url, headers=headers, data=data)
    res.raise_for_status()
    return res.json()


def create_user_with_email_and_password(email, password):
    """Creates a user with email and password"""
    request_url = "{}:signUp?key={}".format(
        config.FIREBASE_AUTH_URL,
        config.API_KEY)
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    data = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    req = requests.post(request_url, headers=headers, data=data)
    req.raise_for_status()
    return req.json()


def connect_db(firebase_token=None):
    """Creates a database connection given a Firebase token"""
    return Database(
        firebase_token,
        config.FIRESTORE_URL,
        config.API_KEY)


class Database():
    """
    AD HOC: Weak copy of Database class from Pyrebase library

    In order to get around annoying incompatabilty of Pyrebase with the
    official Google Cloud libraries, as well as with the Firebase emulator
    """

    def __init__(self, token=None, base_url=None, api_key=None):
        self.token = token
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.path = None

    def collection(self, path):
        return self._child(path)

    def document(self, path):
        return self._child(path)

    def _child(self, path):
        return DatabaseChild(self, [path])

    def get(self):
        url = self._make_url()
        headers = self._make_headers()
        res = self.session.get(url, headers=headers)
        res.raise_for_status()
        return _clean_response(res.json())

    def push(self, data):
        url = self._make_url(pop=True)
        headers = self._make_headers()
        data_str = self._make_data(data)
        res = self.session.post(url, headers=headers, data=data_str)
        res.raise_for_status()
        return _clean_response(res.json())

    def _make_url(self, pop=False):
        if pop:
            last = self.path.pop()
        path = "/".join(self.path)
        self.path = None
        if pop:
            return "{}/{}?documentId={}".format(self.base_url, path, last)
        return "{}/{}".format(self.base_url, path)

    def _make_headers(self, create=True):
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        if self.token:
            headers["Authorization"] = "Bearer {}".format(self.token)
        return headers

    def _make_data(self, data):
        fields = {key: _value_to_firebase(value)
                  for key, value in data.items()}
        return json.dumps({"fields": fields}).encode("utf-8")


class DatabaseChild():
    def __init__(self, database, path=None):
        self.database = database
        self.path = path or []

    def collection(self, path):
        return self._child(path)

    def document(self, path):
        return self._child(path)

    def _child(self, path):
        return DatabaseChild(self.database, self.path + [path])

    def get(self):
        self.database.path = self.path.copy()
        return self.database.get()

    def push(self, data):
        self.database.path = self.path.copy()
        return self.database.push(data)


def _clean_response(data):
    if "documents" in data:
        return [_clean_response(item) for item in data["documents"]]
    if "fields" in data:
        return {key: _value_from_firebase(value)
                for key, value in data["fields"].items()}


def _value_to_firebase(x):
    if x is None:
        return {"nullValue": x}
    if type(x) == str:
        return {"stringValue": x}
    if type(x) == int:
        return {"integerValue": x}
    if type(x) == bool:
        return {"booleanValue": x}
    if type(x) == dict:
        fields = {key: _value_to_firebase(value)
                  for key, value in x.items()}
        return {"mapValue": {"fields": fields}}


def _value_from_firebase(x):
    if "mapValue" in x:
        fields = x["mapValue"]["fields"]
        return {key: _value_from_firebase(value)
                for key, value in fields.items()}
    return list(x.values())[0]
