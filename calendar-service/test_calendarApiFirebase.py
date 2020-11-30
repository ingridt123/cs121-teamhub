import pytest

import google.api_core.datetime_helpers
import google.api_core.exceptions
from google.cloud import firestore
import time

import calendarApiFirebase
import calendarEvent
import calendarErrors
from testConstants import *
from testUtils import db

""" Test file for calendarApiFirebase file. """

###############################################################################
# TEST FUNCTIONS
###############################################################################

# Test immediately passed
def test_getEventsReference(db):
    ref = calendarApiFirebase.getEventsReference(db, SCHOOL_ID, TEAM_ID, EVENT1_ID)
    assert ref is not None
    assert type(ref) == firestore.DocumentReference
    assert ref.path == FIREBASE_PATH + "/" + EVENT1_ID

# Test immediately passed
# CollectionReference doesn't have path attribute, so updated test in response to that
def test_getEventsReferenceNoEventId(db):
    ref = calendarApiFirebase.getEventsReference(db, SCHOOL_ID, TEAM_ID)
    assert ref is not None
    assert type(ref) == firestore.CollectionReference
    assert ref.document().path[:ref.document().path.rfind('/')] == FIREBASE_PATH

# Found that returning list of DocumentSnapshots instead of dicts, so added to_dict() when
# appending documents to list
# Found that database returns dates and times in DatetimeWithNanoseconds, so changed calendarEvent
# to use datetime instead and convert back to string when getting event in calendarApiFirebase
def test_getEvents(db):
    events = calendarApiFirebase.getEvents(FIREBASE_TOKEN, SCHOOL_ID, TEAM_ID, USER_ID)
    assert len(events) == 2
    assert event1 in events
    assert event3 in events

# Test immediately passed
def test_addEvent(db):
    event4_beforeAdd = {
        "userIds": EVENT4_USERIDS,
        "eventType": EVENT4_EVENTTYPE,
        "name": EVENT4_NAME,
        "location": EVENT4_LOCATION,
        "times": {
            "from": google.api_core.datetime_helpers.from_rfc3339(EVENT4_TIME1),
            "to": google.api_core.datetime_helpers.from_rfc3339(EVENT4_TIME2)
        },
        "dates": {
            "from": google.api_core.datetime_helpers.from_rfc3339(EVENT4_DATE1),
            "to": google.api_core.datetime_helpers.from_rfc3339(EVENT4_DATE1)
        },
        "repeating": {
            "frequency": EVENT4_REPEATINGFREQ,
            'daysOfWeek': EVENT4_REPEATINGDAYS,
            "startDate": google.api_core.datetime_helpers.from_rfc3339(EVENT4_DATE1),
            "endDate": google.api_core.datetime_helpers.from_rfc3339(EVENT4_DATE2)
        }
    }
    calendarApiFirebase.addEvent(FIREBASE_TOKEN, SCHOOL_ID, TEAM_ID, event4_beforeAdd)
    events = calendarApiFirebase.getEvents(FIREBASE_TOKEN, SCHOOL_ID, TEAM_ID, USER_ID)
    assert len(events) == 3
    assert event1 in events
    assert event3 in events
    assert event4 in events

# Test immediately passed
# Test updated wrong event (EVENT1_ID instead of EVENT2_ID) so this was changed
def test_updateEvent(db):
    eventDict = {
        "userIds": []
    }
    calendarApiFirebase.updateEvent(FIREBASE_TOKEN, SCHOOL_ID, TEAM_ID, EVENT2_ID, eventDict)
    events = calendarApiFirebase.getEvents(FIREBASE_TOKEN, SCHOOL_ID, TEAM_ID, USER_ID)
    assert len(events) == 3
    assert event1 in events
    assert event3 in events
    assert event2_afterUpdate in events

# Test immediately passed
def test_deleteEvent(db):
    calendarApiFirebase.deleteEvent(FIREBASE_TOKEN, SCHOOL_ID, TEAM_ID, EVENT1_ID)
    events = calendarApiFirebase.getEvents(FIREBASE_TOKEN, SCHOOL_ID, TEAM_ID, USER_ID)
    assert len(events) == 1
    assert event3 in events
