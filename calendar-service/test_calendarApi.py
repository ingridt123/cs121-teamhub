import pytest

import os 
from flask import request
import json
import time

import calendarApi
from testConstants import *
from testUtils import requests_validMock, db

""" Test file for calendarApi file. """

###############################################################################
# FIXTURES
###############################################################################

@pytest.fixture
def client(db, requests_validMock):
    calendarApi.app.config['TESTING'] = True
    return calendarApi.app.test_client()


###############################################################################
# TEST FUNCTIONS
###############################################################################

### TESTS FOR GET ###

# Found that response must be response object, so use make_response and jsonify to create object
def test_getEvents(client, mocker):
    response = client.get(FLASK_ENDPOINT, data=json.dumps(valid_json_get), content_type='application/json')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert event1 in response.json
    assert event3 in response.json

# Found that catching BadRequest exception should use BadRequest instead of request.BadRequest
def test_getEventsJsonBadRequest(client):
    response = client.get(FLASK_ENDPOINT, content_type='application/json')
    assert response.status_code == 400

# # Test immediately passed
def test_getEventsJsonEmpty(client):
    response = client.get(FLASK_ENDPOINT, data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

# # Test immediately passed
def test_getEventsJsonInvalidType(client):
    invalid_json = {
        'userToken': 321
    }
    response = client.get(FLASK_ENDPOINT, data=json.dumps(invalid_json), content_type='application/json')
    assert response.status_code == 400

# # Test immediately passed
def test_getEventsFirebaseTokenError(client, requests_mock):
    requests_mock.get(CHECK_TOKEN_URL, status_code=404)
    response = client.get(FLASK_ENDPOINT, data=json.dumps(valid_json_get), content_type='application/json')
    assert response.status_code == 401

### TESTS FOR ADD ###

# Test immediately passed
def test_addEvent(client):
    response1 = client.post(FLASK_ENDPOINT, data=json.dumps(valid_json_add2), content_type='application/json')
    response2 = client.get(FLASK_ENDPOINT, data=json.dumps(valid_json_get), content_type='application/json')
    assert response1.status_code == 201
    assert len(response2.json) == 3
    assert event1 in response2.json
    assert event3 in response2.json
    assert event4 in response2.json

# Test immediately passed
def test_addEventJsonBadRequest(client):
    response = client.post(FLASK_ENDPOINT, content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_addEventJsonEmpty(client):
    response = client.post(FLASK_ENDPOINT, data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_addEventJsonMissingFields(client):
    invalid_json = {
        'userToken': USER_ID
    }
    response = client.post(FLASK_ENDPOINT, data=json.dumps(invalid_json), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_addEventJsonInvalidType(client):
    invalid_json = {
        'userToken': USER_ID,
        'userIds': EVENT1_USERIDS,
        'eventType': True,
        'name': EVENT1_NAME,
        'location': EVENT1_LOCATION,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE1
        },
        'repeating': {
            'frequency': EVENT1_REPEATINGFREQ,
            'daysOfWeek': EVENT1_REPEATINGDAYS,
            'startDate': EVENT1_DATE1,
            'endDate': EVENT1_DATE2
        }
    }
    response = client.post(FLASK_ENDPOINT, data=json.dumps(invalid_json), content_type='application/json')
    assert response.status_code == 400

# Found that not catching ValueError in calendarEvent, so added try-catch block to raise Error400
def test_addEventJsonInvalidValid(client):
    invalid_json = {
        'userToken': USER_ID,
        'userIds': EVENT1_USERIDS,
        'eventType': 'gym',
        'name': EVENT1_NAME,
        'location': EVENT1_LOCATION,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE1
        },
        'repeating': {
            'frequency': EVENT1_REPEATINGFREQ,
            'daysOfWeek': EVENT1_REPEATINGDAYS,
            'startDate': EVENT1_DATE1,
            'endDate': EVENT1_DATE2
        }
    }
    response = client.post(FLASK_ENDPOINT, data=json.dumps(invalid_json), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_addEventFirebaseTokenError(client, requests_mock):
    requests_mock.get(CHECK_TOKEN_URL, status_code=404)
    response = client.post(FLASK_ENDPOINT, data=json.dumps(valid_json_add2), content_type='application/json')
    assert response.status_code == 401

# ### TESTS FOR UPDATE ###

# Found that userIds = [] not being processed correctly by calendarEvent, so calendarEvent sets attributes to 
# None if they aren't in the json
def test_updateEvent(client):
    response1 = client.put(FLASK_ENDPOINT, data=json.dumps(valid_json_update), content_type='application/json')
    response2 = client.get(FLASK_ENDPOINT, data=json.dumps(valid_json_get), content_type='application/json')
    assert response1.status_code == 201
    assert len(response2.json) == 3
    assert event1 in response2.json
    assert event3 in response2.json
    assert event2_afterUpdate in response2.json

# Test immediately passed
def test_updateEventJsonBadRequest(client):
    response = client.put(FLASK_ENDPOINT, content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_updateEventEmpty(client):
    response = client.put(FLASK_ENDPOINT, data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_updateEventJsonMissingFields(client):
    invalid_json = {
        'userToken': USER_ID
    }
    response = client.put(FLASK_ENDPOINT, data=json.dumps(invalid_json), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_updateEventJsonInvalidType(client):
    invalid_json = {
        'userToken': USER_ID,
        'eventId': EVENT2_ID,
        'name': 123
    }
    response = client.put(FLASK_ENDPOINT, data=json.dumps(invalid_json), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_updateEventFirebaseTokenError(client, requests_mock):
    requests_mock.get(CHECK_TOKEN_URL, status_code=404)
    response = client.put(FLASK_ENDPOINT, data=json.dumps(valid_json_update), content_type='application/json')
    assert response.status_code == 401

# ### TESTS FOR DELETE ###

# Test immediately passed
def test_deleteEvent(client):
    response1 = client.delete(FLASK_ENDPOINT, data=json.dumps(valid_json_delete), content_type='application/json')
    response2 = client.get(FLASK_ENDPOINT, data=json.dumps(valid_json_get), content_type='application/json')
    assert response1.status_code == 201
    assert len(response2.json) == 1
    assert event3 in response2.json

# Test immediately passed
def test_deleteEventJsonBadRequest(client):
    response = client.delete(FLASK_ENDPOINT, content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_deleteEventEmpty(client):
    response = client.delete(FLASK_ENDPOINT, data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_deleteEventJsonMissingFields(client):
    invalid_json = {
        'userToken': USER_ID,
    }
    response = client.delete(FLASK_ENDPOINT, data=json.dumps(invalid_json), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_deleteEventJsonInvalidType(client):
    invalid_json = {
        'userToken': USER_ID,
        'eventId': [],
    }
    response = client.delete(FLASK_ENDPOINT, data=json.dumps(invalid_json), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_deleteEventFirebaseTokenError(client, requests_mock):
    requests_mock.get(CHECK_TOKEN_URL, status_code=404)
    response = client.delete(FLASK_ENDPOINT, data=json.dumps(valid_json_delete), content_type='application/json')
    assert response.status_code == 401