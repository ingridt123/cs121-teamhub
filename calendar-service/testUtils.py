import pytest

import os
from google.cloud import firestore
import google.auth.credentials
from unittest import mock

""" Utility functions for testing. """

# Added fixture for requests_mock because needed prior to creating CalendarRequest object
@pytest.fixture
def requests_validMock(requests_mock):
    requests_mock.get("localhost://checktoken", json={'firebaseToken': 'testToken321'}, status_code=200)
    requests_mock.get("localhost://users/current", json={'schoolId': 'school1', 'teamId': 'team1'}, status_code=200)

@pytest.fixture
def db(mocker):
    # Set up environment variables
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8080/firestore"
    os.environ["FIRESTORE_HOST"] = "http://localhost:8080"
    os.environ["FIRESTORE_PROJECT_ID"] = "test"

    # Start and import data into emulator
    # Note: must run in cs121-teamhub directory
    # os.system("firebase emulators:start --import=./saved-data")
    # time.sleep(5)

    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    db = firestore.Client(project="test", credentials=credentials)
    mocker.patch('calendarApiFirebase.getFirebaseClient', return_value=db)
    yield db

    # TODO teardown code
    # os.system("kill $!")
    # os.system('\x03')
    # os.system('\x03')