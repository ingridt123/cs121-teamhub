import json
import pytest
import requests
import requests_mock
import calendarRequest

""" Test file for CalendarRequest class. """

###############################################################################
# SETUP
###############################################################################

valid_json = "{ \
    'userToken': 'testToken123', \
    'eventType': 'practice', \
    'name': 'Soccer Practice', \
    'times': { \
        'from': '2020-12-10T13:45:00.000Z', \
        'to': '2020-12-10T14:00:00.000Z' \
    }, \
    'dates': { \
        'from': '2020-12-10T13:45:00.000Z', \
        'to': '2020-12-10T14:00:00.000Z' \
    } \
}"

### FIXTURES ###

@pytest.fixture
def request_validJson():
    return calendarRequest.CalendarRequest(valid_json)


###############################################################################
# TEST FUNCTIONS
###############################################################################

### TESTS FOR JSON ###

@pytest.mark.xfail
def test_json(request_validJson):
    assert request_validJson.getJson() == valid_json

### TESTS FOR USER TOKEN

@pytest.mark.xfail
def test_userToken(request_validJson):
    assert request_validJson.getUserToken() == "testToken123"

@pytest.mark.xfail
def test_userTokenEmpty():
    json = "{ \
        'userToken': '', \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarRequest.CalendarRequest(json)

@pytest.mark.xfail
def test_userTokenInvalid():
    json = "{ \
        'userToken': 12345, \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarRequest.CalendarRequest(json)

### TESTS FOR FIREBASE TOKEN ###

@pytest.mark.xfail
def test_firebaseToken(request_validJson, requests_mock):
    requests_mock.get("/check_token", json="{'token': 'testToken321'}", status_code=200)
    assert request_validJson.getFirebaseToken() == "testToken321"

@pytest.mark.xfail
def test_firebaseTokenEmpty(requests_mock):
    requests_mock.get("/check_token", json="{'token': ''}", status_code=200)
    with pytest.raises(Exception("401")):
        calendarRequest.CalendarRequest(valid_json)

@pytest.mark.xfail
def test_firebaseTokenInvalid(requests_mock):
    requests_mock.get("/check_token", status_code=404)
    with pytest.raises(Exception("401")):
        calendarRequest.CalendarRequest(valid_json)

### TESTS FOR SCHOOL AND TEAM ID ###

@pytest.mark.xfail
def test_schoolAndTeamId(request_validJson, requests_mock):
    requests_mock.get("/users/current", json="{'school': 'school1', 'team': 'team1'}", status_code=200)
    assert request_validJson.getSchoolId() == "school1"
    assert request_validJson.getTeamId() == "team1"

@pytest.mark.xfail
def test_schoolAndTeamIdEmptySchool(requests_mock):
    requests_mock.get("/users/current", json="{'school': '', 'team': 'team1'}", status_code=200)
    with pytest.raises(Exception("401")):
        calendarRequest.CalendarRequest(valid_json)

@pytest.mark.xfail
def test_schoolAndTeamIdEmptyTeam(requests_mock):
    requests_mock.get("/users/current", json="{'school': 'school1', 'team': ''}", status_code=200)
    with pytest.raises(Exception("401")):
        calendarRequest.CalendarRequest(valid_json)

@pytest.mark.xfail
def test_schoolAndTeamIdInvalid(requests_mock):
    requests_mock.get("/users/current", json="{'school': 'school1', 'team': ''}", status_code=200)
    with pytest.raises(Exception("404")):
        calendarRequest.CalendarRequest(valid_json)