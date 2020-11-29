import pytest

import os 
from flask import request
import json
import time

import calendarApi
from testUtils import requests_validMock, db

""" Test file for calendarApi file. """

###############################################################################
# SETUP
###############################################################################

valid_eventId = "0d3IKB9awt0FtzN7z1Qv"
valid_eventType = "practice"
valid_name1 = "Soccer Practice"
valid_name2 = "Weekly Soccer Practice"
valid_location = "Parents"
valid_userId = "user123"
valid_userIds = [valid_userId, "user321"]
valid_time1 = "2020-12-10T07:45:00.000000Z"
valid_time2 = "2020-12-10T08:00:00.000000Z"
valid_date1 = "2020-12-10T00:00:00.000000Z"
valid_date2 = "2021-01-10T00:00:00.000000Z"
valid_date3 = "2020-11-08T00:00:00.000000Z"
valid_daysOfWeek = ["M", "W"]
valid_weeklyFreq = "w"

valid_json_get = {
	'userToken': valid_userId
}

invalid_json_get = {
    'userToken': 321
}

valid_json_add = {
    'userToken': valid_userId,
    'userIds': valid_userIds,
    'eventType': valid_eventType,
    'name': valid_name1,
    'location': valid_location,
    'times': {
        'from': valid_time1,
        'to': valid_time2
    },
    'dates': {
        'from': valid_date1,
        'to': valid_date1
    },
    'repeating': {
	    'frequency': valid_weeklyFreq,
        'daysOfWeek': valid_daysOfWeek,
        'startDate': valid_date1,
        'endDate': valid_date2
    }
}

invalid_json_add1 = {
    'userToken': valid_userId,
    'userIds': valid_userIds,
    'eventType': True,
    'name': valid_name1,
    'location': valid_location,
    'times': {
        'from': valid_time1,
        'to': valid_time2
    },
    'dates': {
        'from': valid_date1,
        'to': valid_date1
    },
    'repeating': {
	    'frequency': valid_weeklyFreq,
        'daysOfWeek': valid_daysOfWeek,
        'startDate': valid_date1,
        'endDate': valid_date2
    }
}

invalid_json_add2 = {
    'userToken': valid_userId,
    'userIds': valid_userIds,
    'eventType': 'gym',
    'name': valid_name1,
    'location': valid_location,
    'times': {
        'from': valid_time1,
        'to': valid_time2
    },
    'dates': {
        'from': valid_date1,
        'to': valid_date1
    },
    'repeating': {
	    'frequency': valid_weeklyFreq,
        'daysOfWeek': valid_daysOfWeek,
        'startDate': valid_date1,
        'endDate': valid_date2
    }
}

valid_json_update = {
    'userToken': valid_userId,
    'eventId': valid_eventId,
    'userIds': []
}

invalid_json_update = {
    'userToken': valid_userId,
    'eventId': valid_eventId,
    'name': 1234
}

valid_json_delete = {
    'userToken': valid_userId,
    'eventId': valid_eventId,
}

invalid_json_delete = {
    'userToken': valid_userId,
    'eventId': [],
}

missing_json = {
    'userToken': valid_userId,
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
        'to': valid_time1
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

### FIXTURES ###

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
    mocker.patch('calendarApiFirebase.getEvents', return_value=[event1, event2])
    response = client.get('/events', data=json.dumps(valid_json_get), content_type='application/json')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert event1 in response.json
    assert event2 in response.json

# Found that catching BadRequest exception should use BadRequest instead of request.BadRequest
def test_getEventsJsonBadRequest(client):
    response = client.get('/events', content_type='application/json')
    assert response.status_code == 400

# # Test immediately passed
def test_getEventsJsonEmpty(client):
    response = client.get('/events', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

# # Test immediately passed
def test_getEventsJsonInvalidType(client):
    response = client.get('/events', data=json.dumps(invalid_json_get), content_type='application/json')
    assert response.status_code == 400

# # Test immediately passed
def test_getEventsFirebaseTokenError(client, requests_mock):
    requests_mock.get("localhost://checktoken", status_code=404)
    response = client.get('/events', data=json.dumps(valid_json_get), content_type='application/json')
    assert response.status_code == 401

### TESTS FOR ADD ###

# Test immediately passed
def test_addEvent(client):
    response1 = client.post('/events', data=json.dumps(valid_json_add), content_type='application/json')
    response2 = client.get('/events', data=json.dumps(valid_json_get), content_type='application/json')
    assert response1.status_code == 201
    assert len(response2.json) == 3

# Test immediately passed
def test_addEventJsonBadRequest(client):
    response = client.post('/events', content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_addEventJsonEmpty(client):
    response = client.post('/events', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_addEventJsonMissingFields(client):
    response = client.post('/events', data=json.dumps(missing_json), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_addEventJsonInvalidType(client):
    response = client.post('/events', data=json.dumps(invalid_json_add1), content_type='application/json')
    assert response.status_code == 400

# Found that not catching ValueError in calendarEvent, so added try-catch block to raise Error400
def test_addEventJsonInvalidValid(client):
    response = client.post('/events', data=json.dumps(invalid_json_add2), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_addEventFirebaseTokenError(client, requests_mock):
    requests_mock.get("localhost://checktoken", status_code=404)
    response = client.post('/events', data=json.dumps(valid_json_add), content_type='application/json')
    assert response.status_code == 401

# ### TESTS FOR UPDATE ###

def test_updateEvent(client):
    response1 = client.put('/events', data=json.dumps(valid_json_update), content_type='application/json')
    response2 = client.get('/events', data=json.dumps(valid_json_get), content_type='application/json')
    assert response1.status_code == 201
    assert len(response2.json) == 3

# Test immediately passed
def test_updateEventJsonBadRequest(client):
    response = client.put('/events', content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_updateEventEmpty(client):
    response = client.put('/events', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_updateEventJsonMissingFields(client):
    response = client.put('/events', data=json.dumps(missing_json), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_updateEventJsonInvalidType(client):
    response = client.put('/events', data=json.dumps(invalid_json_update), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_updateEventFirebaseTokenError(client, requests_mock):
    requests_mock.get("localhost://checktoken", status_code=404)
    response = client.put('/events', data=json.dumps(valid_json_update), content_type='application/json')
    assert response.status_code == 401

# ### TESTS FOR DELETE ###

# Test immediately passed
def test_deleteEvent(client):
    response1 = client.delete('/events', data=json.dumps(valid_json_delete), content_type='application/json')
    response2 = client.get('/events', data=json.dumps(valid_json_get), content_type='application/json')
    assert response1.status_code == 201
    assert len(response2.json) == 2

# Test immediately passed
def test_deleteEventJsonBadRequest(client):
    response = client.delete('/events', content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_deleteEventEmpty(client):
    response = client.delete('/events', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_deleteEventJsonMissingFields(client):
    response = client.delete('/events', data=json.dumps(missing_json), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_deleteEventJsonInvalidType(client):
    response = client.delete('/events', data=json.dumps(invalid_json_delete), content_type='application/json')
    assert response.status_code == 400

# Test immediately passed
def test_deleteEventFirebaseTokenError(client, requests_mock):
    requests_mock.get("localhost://checktoken", status_code=404)
    response = client.delete('/events', data=json.dumps(valid_json_delete), content_type='application/json')
    assert response.status_code == 401