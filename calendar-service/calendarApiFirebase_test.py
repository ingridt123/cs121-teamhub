import pytest

from google.cloud import firestore
import time

import calendarApiFirebase
import calendarEvent
import calendarErrors
from testUtils import db

""" Test file for calendarApiFirebase file. """

###############################################################################
# SETUP
###############################################################################

valid_firebaseToken = "testToken321"
valid_schoolId = "school1"
valid_teamId = "team123"
valid_eventId = "gkjtuYvCOGkiVeEsmD7T"
valid_userId = "user321"
valid_path = "schools/school1/teams/team123/events"
valid_time1 = "2020-12-10T13:45:00.000Z"
valid_time2 = "2020-12-10T14:00:00.000Z"
valid_time4 = "2020-12-28T10:00:00.000Z"
valid_time5 = "2020-12-28T18:00:00.000Z"
valid_date1 = "2020-12-10"
valid_date2 = "2021-01-10"
valid_date3 = "2020-11-28"
valid_date4 = "2020-12-28"
valid_date5 = "2021-12-28"
valid_date6 = "2021-11-12"

time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
date_format = "%Y-%m-%d"

valid_eventDict_add = {
    "userIds": [],
    "eventType": "practice",
    "name": "Softball Practice",
    "location": "Pritzlaff",
    "times": {
        "from": time.strptime(valid_time4, time_format),
        "to": time.strptime(valid_time5, time_format)
    },
    "dates": {
        "from": time.strptime(valid_date4, date_format),
        "to": time.strptime(valid_date4, date_format)
    },
    "repeating": {
        "frequency": calendarEvent.CalendarEventFrequency.Weekly.value,
        'daysOfWeek': [calendarEvent.DaysOfWeek.Wednesday.value],
        "startDate": time.strptime(valid_date4, date_format),
        "endDate": time.strptime(valid_date5, date_format)
    }
}

valid_eventDict_updateBefore = {
    "userIds": [],
    "eventId": "0d3IKB9awt0FtzN7z1Qv",
    "name": "Basketball Practice",
    "location": "Rains",
    "dates": {
        "from": time.strptime(valid_date6, date_format),
        "from": time.strptime(valid_date6, date_format),
    }
}

valid_eventDict_updateAfter = {
    "userIds": [],
    "eventId": "0d3IKB9awt0FtzN7z1Qv"
}

event1 = {
    'location': 'Parents', 
    'eventType': 'practice', 
    'repeating': {
        'frequency': 'w', 
        'daysOfWeek': ['M', 'W'], 
        'endDate': time.strptime(valid_date2, date_format),
        'startDate': time.strptime(valid_date1, date_format)
    }, 
    'times': {
        'from': time.strptime(valid_time1, time_format),
        'to': time.strptime(valid_time1, time_format)
    },
    'dates': {
        'to': time.strptime(valid_date1, date_format),
        'from': time.strptime(valid_date1, date_format)
    },
    'userIds': [valid_userId, 'user321'], 
    'name': 'Soccer Practice'
}

event2 = {
    'dates': {
        'to': time.strptime(valid_date3, date_format),
        'from': time.strptime(valid_date3, date_format)
    }, 
    'name': 'Track Meet', 
    'eventType': 'competition', 
    'userIds': []
}

### FIXTURES ###


###############################################################################
# TEST FUNCTIONS
###############################################################################

def test_getEventsReference(db):
    ref = calendarApiFirebase.getEventsReference(db, valid_schoolId, valid_teamId, valid_eventId)
    assert ref is not None
    assert type(ref) == firestore.DocumentReference
    assert ref.path == valid_path + "/" + valid_eventId

def test_getEventsReferenceNoEventId(db):
    ref = calendarApiFirebase.getEventsReference(db, valid_schoolId, valid_teamId)
    assert ref is not None
    assert type(ref) == firestore.CollectionReference
    assert ref.path == valid_path

def test_getEvents(db, mocker):
    mocker.patch('calendarApiFirebase.getFirebaseClient', return_value=db)
    events = calendarApiFirebase.getEvents(valid_firebaseToken, valid_schoolId, valid_teamId, valid_userId)
    assert len(events) == 2
    assert event1 in events
    assert event2 in events

# # TODO: for others as well?
# def test_getEventsError(db, mocker):
#     mocker.patch('calendarApiFirebase.getFirebaseClient', return_value=db)
#     mocker.patch('firestore.DocumentReference.stream', side_effect=Exception)
#     with pytest.raises(calendarErrors.Error404):
#         calendarApiFirebase.getEvents(valid_firebaseToken, valid_schoolId, valid_teamId, valid_userId)

def test_addEvent(db, mocker):
    mocker.patch('calendarApiFirebase.getFirebaseClient', return_value=db)
    calendarApiFirebase.addEvent(valid_firebaseToken, valid_schoolId, valid_teamId, valid_eventDict_add)
    events = calendarApiFirebase.getEvents(valid_firebaseToken, valid_schoolId, valid_teamId, valid_userId)
    assert len(events) == 3
    assert valid_eventDict_add in events

def test_updateEvent(db, mocker):
    mocker.patch('calendarApiFirebase.getFirebaseClient', return_value=db)
    calendarApiFirebase.updateEvent(valid_firebaseToken, valid_schoolId, valid_teamId, valid_eventId, valid_eventDict_updateBefore)
    events = calendarApiFirebase.getEvents(valid_firebaseToken, valid_schoolId, valid_teamId, valid_userId)
    assert len(events) == 3
    assert valid_eventDict_updateAfter in events

def test_deleteEvent(db, mocker):
    mocker.patch('calendarApiFirebase.getFirebaseClient', return_value=db)
    calendarApiFirebase.deleteEvent(valid_firebaseToken, valid_schoolId, valid_teamId, valid_eventId)
    events = calendarApiFirebase.getEvents(valid_firebaseToken, valid_schoolId, valid_teamId, valid_userId)
    assert len(events) == 2
