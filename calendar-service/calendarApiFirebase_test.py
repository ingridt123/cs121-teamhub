import pytest

import google.api_core.datetime_helpers
from google.cloud import firestore
import time

import calendarApiFirebase
import calendarEvent
import calendarErrors
from testUtils import db

""" Test file for calendarApiFirebase file. """
# TODO: add exception checking
###############################################################################
# SETUP
###############################################################################

valid_firebaseToken = "testToken321"
valid_schoolId = "school1"
valid_teamId = "team123"
valid_eventId1 = "gkjtuYvCOGkiVeEsmD7T"
valid_eventId2 = "0d3IKB9awt0FtzN7z1Qv"
valid_userId = "user123"
valid_path = "schools/school1/teams/team123/events"
valid_time1 = "2020-12-10T07:45:00.000000Z"
valid_time2 = "2020-12-10T08:00:00.000000Z"
valid_time4 = "2020-12-28T10:00:00.000000Z"
valid_time5 = "2020-12-28T18:00:00.000000Z"
valid_date1 = "2020-12-10T00:00:00.000000Z"
valid_date2 = "2021-01-10T00:00:00.000000Z"
valid_date3 = "2020-11-08T00:00:00.000000Z"
valid_date4 = "2020-12-28T00:00:00.000000Z"
valid_date5 = "2021-12-28T00:00:00.000000Z"
valid_date6 = "2020-11-12T00:00:00.000000Z"

valid_eventDict_addBefore = {
    "userIds": [],
    "eventType": "practice",
    "name": "Softball Practice",
    "location": "Pritzlaff",
    "times": {
        "from": google.api_core.datetime_helpers.from_rfc3339(valid_time4),
        "to": google.api_core.datetime_helpers.from_rfc3339(valid_time5)
    },
    "dates": {
        "from": google.api_core.datetime_helpers.from_rfc3339(valid_date4),
        "to": google.api_core.datetime_helpers.from_rfc3339(valid_date4)
    },
    "repeating": {
        "frequency": calendarEvent.CalendarEventFrequency.Weekly.value,
        'daysOfWeek': [calendarEvent.DaysOfWeek.Wednesday.value],
        "startDate": google.api_core.datetime_helpers.from_rfc3339(valid_date4),
        "endDate": google.api_core.datetime_helpers.from_rfc3339(valid_date5)
    }
}

valid_eventDict_addAfter = {
    "userIds": [],
    "eventType": "practice",
    "name": "Softball Practice",
    "location": "Pritzlaff",
    "times": {
        "from": valid_time4,
        "to": valid_time5
    },
    "dates": {
        "from": valid_date4,
        "to": valid_date4
    },
    "repeating": {
        "frequency": calendarEvent.CalendarEventFrequency.Weekly.value,
        'daysOfWeek': [calendarEvent.DaysOfWeek.Wednesday.value],
        "startDate": valid_date4,
        "endDate": valid_date5
    }
}

valid_eventDict_updateBefore = {
    "userIds": []
}

valid_eventDict_updateAfter = {
    "userIds": [],
    "name": "Basketball Practice",
    "location": "Rains",
    "eventType": "practice",
    "dates": {
        "from": valid_date6,
        "to": valid_date6
    }
}

event1 = {
    'location': 'Parents', 
    'eventType': 'practice', 
    'repeating': {
        'frequency': 'w', 
        'daysOfWeek': ['M', 'W'], 
        'startDate': valid_date1,
        'endDate': valid_date2
    }, 
    'times': {
        'from': valid_time1,
        'to': valid_time2
    },
    'dates': {
        'to': valid_date1,
        'from': valid_date1
    },
    'userIds': [valid_userId, 'user321'], 
    'name': 'Soccer Practice'
}

event2 = {
    'dates': {
        'to': valid_date3,
        'from': valid_date3
    }, 
    'name': 'Track Meet', 
    'eventType': 'competition', 
    'userIds': []
}


###############################################################################
# TEST FUNCTIONS
###############################################################################

# Test immediately passed
def test_getEventsReference(db):
    ref = calendarApiFirebase.getEventsReference(db, valid_schoolId, valid_teamId, valid_eventId1)
    assert ref is not None
    assert type(ref) == firestore.DocumentReference
    assert ref.path == valid_path + "/" + valid_eventId1

# Test immediately passed
# CollectionReference doesn't have path attribute, so updated test in response to that
def test_getEventsReferenceNoEventId(db):
    ref = calendarApiFirebase.getEventsReference(db, valid_schoolId, valid_teamId)
    assert ref is not None
    assert type(ref) == firestore.CollectionReference
    assert ref.document().path[:ref.document().path.rfind('/')] == valid_path

# Found that returning list of DocumentSnapshots instead of dicts, so added to_dict() when
# appending documents to list
# Found that database returns dates and times in DatetimeWithNanoseconds, so changed calendarEvent
# to use datetime instead and convert back to string when getting event in calendarApiFirebase
def test_getEvents(db):
    events = calendarApiFirebase.getEvents(valid_firebaseToken, valid_schoolId, valid_teamId, valid_userId)
    assert len(events) == 2
    assert event1 in events
    assert event2 in events

# Test immediately passed
def test_addEvent(db):
    calendarApiFirebase.addEvent(valid_firebaseToken, valid_schoolId, valid_teamId, valid_eventDict_addBefore)
    events = calendarApiFirebase.getEvents(valid_firebaseToken, valid_schoolId, valid_teamId, valid_userId)
    assert len(events) == 3
    assert event1 in events
    assert event2 in events
    assert valid_eventDict_addAfter in events

# Test immediately passed
# Test updated wrong event (valid_eventId1 instead of valid_eventId2) so this was changed
def test_updateEvent(db):
    calendarApiFirebase.updateEvent(valid_firebaseToken, valid_schoolId, valid_teamId, valid_eventId2, valid_eventDict_updateBefore)
    events = calendarApiFirebase.getEvents(valid_firebaseToken, valid_schoolId, valid_teamId, valid_userId)
    assert len(events) == 3
    assert event1 in events
    assert event2 in events
    assert valid_eventDict_updateAfter in events

# Test immediately passed
def test_deleteEvent(db):
    calendarApiFirebase.deleteEvent(valid_firebaseToken, valid_schoolId, valid_teamId, valid_eventId1)
    events = calendarApiFirebase.getEvents(valid_firebaseToken, valid_schoolId, valid_teamId, valid_userId)
    assert len(events) == 1
    assert event2 in events
