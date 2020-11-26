import pytest

import json
import requests
import requests_mock

import calendarRequest
import calendarErrors

""" Test file for CalendarRequest class. """

###############################################################################
# SETUP
###############################################################################

valid_json = {
    'userToken': 'testToken123', 
    'eventType': 'practice', 
    'name': 'Soccer Practice', 
    'times': { 
        'from': '2020-12-10T13:45:00.000Z', 
        'to': '2020-12-10T14:00:00.000Z' 
    }, 
    'dates': { 
        'from': '2020-12-10T13:45:00.000Z', 
        'to': '2020-12-10T14:00:00.000Z' 
    } 
}

### FIXTURES ###

@pytest.fixture
def request_validJson():
    return calendarRequest.CalendarRequest(valid_json)


###############################################################################
# TEST FUNCTIONS
###############################################################################

### TESTS FOR JSON ###

def test_json(request_validJson, requests_mock):
    requests_mock.get("/check_token", json={'token': 'testToken321'}, status_code=200)
    assert request_validJson.getJson() == valid_json

### TESTS FOR USER TOKEN

def test_userToken(request_validJson, requests_mock):
    requests_mock.get("/check_token", json={'token': 'testToken321'}, status_code=200)
    assert request_validJson.getUserToken() == "testToken123"

def test_userTokenEmpty():
    json = { 
        'userToken': '', 
        'eventType': 'practice', 
        'name': 'Soccer Practice', 
        'times': { 
            'from': '2020-12-10T13:45:00.000Z', 
            'to': '2020-12-10T14:00:00.000Z' 
        }, 
        'dates': { 
            'from': '2020-12-10T13:45:00.000Z', 
            'to': '2020-12-10T14:00:00.000Z' 
        } 
    }
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(json)


def test_userTokenInvalid():
    json = {
        'userToken': 12345,
        'eventType': 'practice',
        'name': 'Soccer Practice',
        'times': {
            'from': '2020-12-10T13:45:00.000Z',
            'to': '2020-12-10T14:00:00.000Z'
        },
        'dates': {
            'from': '2020-12-10T13:45:00.000Z',
            'to': '2020-12-10T14:00:00.000Z'
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(json)

### TESTS FOR FIREBASE TOKEN ###

def test_firebaseToken(request_validJson, requests_mock):
    requests_mock.get("/check_token", json={'token': 'testToken321'}, status_code=200)
    assert request_validJson.getFirebaseToken() == "testToken321"

def test_firebaseTokenEmpty(requests_mock):
    requests_mock.get("/check_token", json={'token': ''}, status_code=200)
    with pytest.raises(calendarErrors.Error401):
        calendarRequest.CalendarRequest(valid_json)

def test_firebaseTokenInvalid(requests_mock):
    requests_mock.get("/check_token", status_code=404)
    with pytest.raises(calendarErrors.Error401):
        calendarRequest.CalendarRequest(valid_json)

### TESTS FOR SCHOOL AND TEAM ID ###

def test_schoolAndTeamId(request_validJson, requests_mock):
    requests_mock.get("/users/current", json={'school': 'school1', 'team': 'team1'}, status_code=200)
    assert request_validJson.getSchoolId() == "school1"
    assert request_validJson.getTeamId() == "team1"

def test_schoolAndTeamIdEmptySchool(requests_mock):
    requests_mock.get("/users/current", json={'school': '', 'team': 'team1'}, status_code=200)
    with pytest.raises(calendarErrors.Error401):
        calendarRequest.CalendarRequest(valid_json)

def test_schoolAndTeamIdEmptyTeam(requests_mock):
    requests_mock.get("/users/current", json={'school': 'school1', 'team': ''}, status_code=200)
    with pytest.raises(calendarErrors.Error401):
        calendarRequest.CalendarRequest(valid_json)

def test_schoolAndTeamIdInvalid(requests_mock):
    requests_mock.get("/users/current", json={'school': 'school1', 'team': ''}, status_code=200)
    with pytest.raises(calendarErrors.Error404):
        calendarRequest.CalendarRequest(valid_json)