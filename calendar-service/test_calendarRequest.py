import pytest

import json
import requests

import calendarRequest
import calendarErrors
from testConstants import *
from testUtils import requests_validMock

""" Test file for CalendarRequest class. """

###############################################################################
# FIXTURES
###############################################################################

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
    assert request_validJson.getUserToken() == USER_ID

# Found that code didn't check for empty user token, so added check
def test_userTokenEmpty(requests_validMock):
    invalid_json = { 
        'userToken': '', 
        'eventType': EVENT1_EVENTTYPE, 
        'name': EVENT1_NAME, 
        'times': { 
            'from': EVENT1_TIME1, 
            'to': EVENT1_TIME2 
        }, 
        'dates': { 
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(invalid_json)

# Found that code didn't mistakenly raised exception if string instead of not string,
# so update type check from == to != str
def test_userTokenInvalid(requests_validMock):
    invalid_json = {
        'userToken': 12345,
        'eventType': EVENT1_EVENTTYPE, 
        'name': EVENT1_NAME, 
        'times': { 
            'from': EVENT1_TIME1, 
            'to': EVENT1_TIME2 
        }, 
        'dates': { 
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(invalid_json)

### TESTS FOR FIREBASE TOKEN ###

# Found that needed to get json from requests.get(), because this function returns all the
# information from the request
def test_firebaseToken(requests_validMock, request_validJson):
    assert request_validJson.getFirebaseToken() == FIREBASE_TOKEN

def test_firebaseTokenEmpty(requests_validMock, requests_mock):
    requests_mock.get(CHECK_TOKEN_URL, json={'firebaseToken': ''}, status_code=200)
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(valid_json)

# Found that instead of checking for Exception, needed to check status code of request instead
def test_firebaseTokenInvalid(requests_validMock, requests_mock):
    requests_mock.get(CHECK_TOKEN_URL, status_code=404)
    with pytest.raises(calendarErrors.Error401):
        calendarRequest.CalendarRequest(valid_json)

### TESTS FOR SCHOOL AND TEAM ID ###

# After fixing same issues found in tests above for school and team id, test passed immediately
def test_schoolAndTeamId(request_validJson):
    assert request_validJson.getSchoolId() == SCHOOL_ID
    assert request_validJson.getTeamId() == TEAM_ID

# After fixing same issues found in tests above for school and team id, test passed immediately
def test_schoolAndTeamIdEmptySchool(requests_validMock, requests_mock):
    requests_mock.get(CURRENT_USERS_URL, json={'school': '', 'team': TEAM_ID}, status_code=200)
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(valid_json)

# After fixing same issues found in tests above for school and team id, test passed immediately
def test_schoolAndTeamIdEmptyTeam(requests_validMock, requests_mock):
    requests_mock.get(CURRENT_USERS_URL, json={'school': SCHOOL_ID, 'team': ''}, status_code=200)
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(valid_json)

# After fixing same issues found in tests above for school and team id, test passed immediately
def test_schoolAndTeamIdInvalid(requests_validMock, requests_mock):
    requests_mock.get(CURRENT_USERS_URL, status_code=404)
    with pytest.raises(calendarErrors.Error400):
        calendarRequest.CalendarRequest(valid_json)