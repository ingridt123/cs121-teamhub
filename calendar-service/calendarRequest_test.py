import pytest

import json
import requests

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

# Added fixture for requests_mock because needed prior to creating CalendarRequest object
@pytest.fixture
def requests_validMock(requests_mock):
    requests_mock.get("localhost://checktoken", json={'firebaseToken': 'testToken321'}, status_code=200)
    requests_mock.get("localhost://users/current", json={'schoolId': 'school1', 'teamId': 'team1'}, status_code=200)

@pytest.fixture
def request_validJson(requests_validMock):
    return calendarRequest.CalendarRequest(valid_json)


###############################################################################
# TEST FUNCTIONS
###############################################################################

### TESTS FOR JSON ###

# Test immediately passed
def test_json(request_validJson):
    assert request_validJson.getJson() == valid_json

### TESTS FOR USER TOKEN

# Found that code didn't mistakenly raised exception if string instead of not string,
# so update type check from == to != str
def test_userToken(request_validJson):
    assert request_validJson.getUserToken() == "testToken123"

# Found that code didn't check for empty user token, so added check
def test_userTokenEmpty(requests_validMock):
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

# Found that code didn't mistakenly raised exception if string instead of not string,
# so update type check from == to != str
def test_userTokenInvalid(requests_validMock):
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

# Found that needed to get json from requests.get(), because this function returns all the
# information from the request
def test_firebaseToken(requests_validMock, request_validJson):
    assert request_validJson.getFirebaseToken() == "testToken321"

def test_firebaseTokenEmpty(requests_validMock, requests_mock):
    requests_mock.get("localhost://checktoken", json={'firebaseToken': ''}, status_code=200)
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(valid_json)

# Found that instead of checking for Exception, needed to check status code of request instead
def test_firebaseTokenInvalid(requests_validMock, requests_mock):
    requests_mock.get("localhost://checktoken", status_code=404)
    with pytest.raises(calendarErrors.Error401):
        calendarRequest.CalendarRequest(valid_json)

### TESTS FOR SCHOOL AND TEAM ID ###

# After fixing same issues found in tests above for school and team id, test passed immediately
def test_schoolAndTeamId(request_validJson):
    assert request_validJson.getSchoolId() == "school1"
    assert request_validJson.getTeamId() == "team1"

# After fixing same issues found in tests above for school and team id, test passed immediately
def test_schoolAndTeamIdEmptySchool(requests_validMock, requests_mock):
    requests_mock.get("localhost://users/current", json={'school': '', 'team': 'team1'}, status_code=200)
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(valid_json)

# After fixing same issues found in tests above for school and team id, test passed immediately
def test_schoolAndTeamIdEmptyTeam(requests_validMock, requests_mock):
    requests_mock.get("localhost://users/current", json={'school': 'school1', 'team': ''}, status_code=200)
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(valid_json)

# After fixing same issues found in tests above for school and team id, test passed immediately
def test_schoolAndTeamIdInvalid(requests_validMock, requests_mock):
    requests_mock.get("localhost://users/current", status_code=404)
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(valid_json)