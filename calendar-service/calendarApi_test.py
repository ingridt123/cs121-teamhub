import pytest

from flask import request
import json
import time

import calendarApi
from testUtils import requests_validMock, db

""" Test file for calendarApi file. """

###############################################################################
# SETUP
###############################################################################

valid_eventId = "testEvent123"
valid_eventType = "practice"
valid_name1 = "Soccer Practice"
valid_name2 = "Weekly Soccer Practice"
valid_location = "Parents"
valid_userToken = "testToken123"
valid_userIds = ["user123", "user321"]
valid_time1 = "2020-12-10T13:45:00.000Z"
valid_time2 = "2020-12-10T14:00:00.000Z"
valid_date1 = "2020-12-10"
valid_date2 = "2021-01-10"
valid_daysOfWeek = ["M", "W"]
valid_weeklyFreq = "w"

time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
date_format = "%Y-%m-%d"

valid_json_get = {
	'userToken': valid_userToken
}

invalid_json_get = {
    'userToken': 321
}

valid_json_add = {
    'userToken': valid_userToken,
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
    'userToken': valid_userToken,
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
    'userToken': valid_userToken,
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
    'userToken': valid_userToken,
    'eventId': valid_eventId,
    'name': valid_name2
}

invalid_json_update = {
    'userToken': valid_userToken,
    'eventId': valid_eventId,
    'name': 1234
}

valid_json_delete = {
    'userToken': valid_userToken,
    'eventId': valid_eventId,
}

invalid_json_delete = {
    'userToken': valid_userToken,
    'eventId': [],
}

missing_json = {
    'userToken': valid_userToken,
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

@pytest.fixture
def client(requests_validMock, db):
    calendarApi.app.config['TESTING'] = True
    return calendarApi.app.test_client()


###############################################################################
# TEST FUNCTIONS
###############################################################################

### TESTS FOR GET ###

def test_getEvents(client):
    response = client.get('/events', data=json.dumps(valid_json_get), content_type='application/json')
    assert response.status_code == 200
    assert len(response.response) == 2
    assert event1 in response.response
    assert event2 in response.response

def test_getEventsJsonBadRequest(client):
    response = client.get('/events', content_type='application/json')
    assert response.status_code == 400

def test_getEventsJsonEmpty(client):
    response = client.get('/events', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

def test_getEventsJsonInvalidType(client):
    response = client.get('/events', data=json.dumps(invalid_json_get), content_type='application/json')
    assert response.status_code == 400

def test_getEventsFirebaseTokenError(client, requests_mock):
    requests_mock.get("localhost://checktoken", status_code=404)
    response = client.get('/events', data=json.dumps(valid_json_get), content_type='application/json')
    assert response.status_code == 401

### TESTS FOR ADD ###

def test_addEvent(client):
    response = client.post('/events', data=json.dumps(valid_json_add), content_type='application/json')
    assert response.status_code == 201

def test_addEventJsonBadRequest(client):
    response = client.post('/events', content_type='application/json')
    assert response.status_code == 400

def test_addEventJsonEmpty(client):
    response = client.post('/events', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

def test_addEventJsonMissingFields(client):
    response = client.post('/events', data=json.dumps(missing_json), content_type='application/json')
    assert response.status_code == 400

def test_addEventJsonInvalidType(client):
    response = client.post('/events', data=json.dumps(invalid_json_add1), content_type='application/json')
    assert response.status_code == 400

def test_addEventJsonInvalidValid(client):
    response = client.post('/events', data=json.dumps(invalid_json_add2), content_type='application/json')
    assert response.status_code == 400

def test_addEventFirebaseTokenError(client, requests_mock):
    requests_mock.get("localhost://checktoken", status_code=404)
    response = client.post('/events', data=json.dumps(valid_json_add), content_type='application/json')
    assert response.status_code == 401

### TESTS FOR UPDATE ###

def test_updateEvent(client):
    response = client.put('/events', data=json.dumps(valid_json_update), content_type='application/json')
    assert response.status_code == 201

def test_updateEventJsonBadRequest(client):
    response = client.put('/events', content_type='application/json')
    assert response.status_code == 400

def test_updateEventEmpty(client):
    response = client.put('/events', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

def test_updateEventJsonMissingFields(client):
    response = client.put('/events', data=json.dumps(missing_json), content_type='application/json')
    assert response.status_code == 400

def test_updateEventJsonInvalidType(client):
    response = client.put('/events', data=json.dumps(invalid_json_update), content_type='application/json')
    assert response.status_code == 400

def test_updateEventFirebaseTokenError(client, requests_mock):
    requests_mock.get("localhost://checktoken", status_code=404)
    response = client.put('/events', data=json.dumps(valid_json_update), content_type='application/json')
    assert response.status_code == 401

### TESTS FOR DELETE ###

def test_deleteEvent(client):
    response = client.delete('/events', data=json.dumps(valid_json_update), content_type='application/json')
    assert response.status_code == 201

def test_deleteEventJsonBadRequest(client):
    response = client.delete('/events', content_type='application/json')
    assert response.status_code == 400

def test_deleteEventEmpty(client):
    response = client.delete('/events', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

def test_deleteEventJsonMissingFields(client):
    response = client.delete('/events', data=json.dumps(missing_json), content_type='application/json')
    assert response.status_code == 400

def test_deleteEventJsonInvalidType(client):
    response = client.delete('/events', data=json.dumps(invalid_json_delete), content_type='application/json')
    assert response.status_code == 400

def test_deleteEventFirebaseTokenError(client, requests_mock):
    requests_mock.get("localhost://checktoken", status_code=404)
    response = client.delete('/events', data=json.dumps(valid_json_delete), content_type='application/json')
    assert response.status_code == 401