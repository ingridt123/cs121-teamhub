import pytest

import os
import google.api_core.datetime_helpers
from google.oauth2.credentials import Credentials
from google.cloud.firestore import Client
from unittest import mock
import time
import requests

from testConstants import *

""" Utility functions for testing. """

# Added fixture for requests_mock because needed prior to creating CalendarRequest object
@pytest.fixture
def requests_validMock(requests_mock):
    requests_mock.get(CHECK_TOKEN_URL, json={'firebaseToken': FIREBASE_TOKEN}, status_code=200)
    requests_mock.get(CURRENT_USERS_URL, json={'schoolId': SCHOOL_ID, 'teamId': TEAM_ID}, status_code=200)

@pytest.fixture
def db(mocker):
    # Set up environment variables
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8080/firestore"
    os.environ["FIRESTORE_HOST"] = "http://localhost:8080"
    os.environ["FIRESTORE_PROJECT_ID"] = "test"

    # Create database client
    credentials = mock.Mock(spec=google.oauth2.credentials.Credentials)
    db = Client(project="test", credentials=credentials)
    mocker.patch('calendarApiFirebase.getFirebaseClient', return_value=db)

    # Reset data in emulator
    requests.delete("http://localhost:8080/emulator/v1/projects/test/databases/(default)/documents")
    ref = db.collection(u'schools').document(SCHOOL_ID).collection(u'teams').document(TEAM_ID).collection(u'events')
    ref.document(EVENT1_ID).set({
        'userIds': EVENT1_USERIDS, 
        'name': EVENT1_NAME,
        'location': EVENT1_LOCATION, 
        'eventType': EVENT1_EVENTTYPE, 
        'times': {
            'from': google.api_core.datetime_helpers.from_rfc3339(EVENT1_TIME1),
            'to': google.api_core.datetime_helpers.from_rfc3339(EVENT1_TIME2)
        },
        'dates': {
            'to': google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE1),
            'from': google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE1),
        },
        'repeating': {
            'frequency': EVENT1_REPEATINGFREQ, 
            'daysOfWeek': EVENT1_REPEATINGDAYS, 
            'startDate': google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE1),
            'endDate': google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE2),
        }, 
    })
    ref.document(EVENT2_ID).set({
        'userIds': EVENT2_USERIDS, 
        'name': EVENT2_NAME,
        'dates': {
            'from': google.api_core.datetime_helpers.from_rfc3339(EVENT2_DATE1),
            'to': google.api_core.datetime_helpers.from_rfc3339(EVENT2_DATE1)
        }, 
        'eventType': EVENT2_EVENTTYPE, 
        'location': EVENT2_LOCATION
    })
    ref.document(EVENT3_ID).set({
        'userIds': EVENT3_USERIDS,
        'name': EVENT3_NAME,
        'dates': {
            'from': google.api_core.datetime_helpers.from_rfc3339(EVENT3_DATE1),
            'to': google.api_core.datetime_helpers.from_rfc3339(EVENT3_DATE1)
        },
        'eventType': EVENT3_EVENTTYPE
    })

    return db