import pytest

import os
import google.api_core.datetime_helpers
from google.cloud import firestore
import google.auth.credentials
from unittest import mock
import time
import requests

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

    # Create database client
    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    db = firestore.Client(project="test", credentials=credentials)
    mocker.patch('calendarApiFirebase.getFirebaseClient', return_value=db)

    # Reset data in emulator
    requests.delete("http://localhost:8080/emulator/v1/projects/test/databases/(default)/documents")
    ref = db.collection(u'schools').document(u'school1').collection(u'teams').document('team123').collection(u'events')
    ref.document(u'0d3IKB9awt0FtzN7z1Qv').set({
        'userIds': ['user456', 'user234'], 
        'name': 'Basketball Practice', 
        'dates': {
            'from': google.api_core.datetime_helpers.from_rfc3339("2020-11-12T00:00:00.000000Z"),
            'to': google.api_core.datetime_helpers.from_rfc3339("2020-11-12T00:00:00.000000Z")
        }, 
        'eventType': 'practice', 
        'location': 'Rains'
    })
    ref.document(u'6w3mDhxwunaqVOVvUqDG').set({
        'userIds': [],
        'name': 'Track Meet',
        'dates': {
            'from': google.api_core.datetime_helpers.from_rfc3339("2020-11-08T00:00:00.000000Z"),
            'to': google.api_core.datetime_helpers.from_rfc3339("2020-11-08T00:00:00.000000Z")
        },
        'eventType': 'competition'
    })
    ref.document(u'gkjtuYvCOGkiVeEsmD7T').set({
        'userIds': ['user123', 'user321'], 
        'name': 'Soccer Practice',
        'location': 'Parents', 
        'eventType': 'practice', 
        'times': {
            'from': google.api_core.datetime_helpers.from_rfc3339("2020-12-10T07:45:00.000000Z"),
            'to': google.api_core.datetime_helpers.from_rfc3339("2020-12-10T08:00:00.000000Z")
        },
        'dates': {
            'to': google.api_core.datetime_helpers.from_rfc3339("2020-12-10T00:00:00.000000Z"),
            'from': google.api_core.datetime_helpers.from_rfc3339("2020-12-10T00:00:00.000000Z"),
        },
        'repeating': {
            'frequency': 'w', 
            'daysOfWeek': ['M', 'W'], 
            'startDate': google.api_core.datetime_helpers.from_rfc3339("2020-12-10T00:00:00.000000Z"),
            'endDate': google.api_core.datetime_helpers.from_rfc3339("2021-01-10T00:00:00.000000Z"),
        }, 
    })

    yield db