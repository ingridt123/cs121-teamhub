import pytest
import time
import calendarEvent

""" Test file for CalendarEvent class. """

###############################################################################
# SETUP
###############################################################################

valid_addEvent_json = "{ \
    'userToken': 'testToken123', \
    'userIds': ['user123', 'user321'], \
    'eventType': 'practice', \
    'name': 'Soccer Practice', \
    'location': 'Parents', \
    'times': { \
        'from': '2020-12-10T13:45:00.000Z', \
        'to': '2020-12-10T14:00:00.000Z' \
    }, \
    'dates': { \
        'from': '2020-12-10', \
        'to': '2021-12-10' \
    }, \
    'repeating': { \
	    'frequency': 'w', \
        'daysOfWeek': ['M', 'W'], \
        'startDate': '2020-12-10', \
        'endDate': '2021-01-10' \
    } \
}"

valid_updateEvent_json = "{ \
    'userToken': 'testToken123', \
    'eventId': 'testEvent123', \
    'name': 'Weekly Soccer Practice' \
}"

valid_deleteEvent_json = "{ \
    'userToken': 'testToken123', \
    'eventId': 'testEvent123' \
}"

### FIXTURES ###

@pytest.fixture
def event_validAddEventJson():
    return calendarEvent.CalendarEvent(valid_addEvent_json, True)

@pytest.fixture
def event_validUpdateEventJson():
    return calendarEvent.CalendarEvent(valid_updateEvent_json, True)

# @pytest.fixture(params = [valid_addEvent_json, 
#                           valid_updateEvent_json,
#                           valid_deleteEvent_json])
# def event_validJson(json):
#     addEvent = (json.param == valid_addEvent_json)
#     return calendarEvent.CalendarEvent(json.param, addEvent)

###############################################################################
# TEST FUNCTIONS
###############################################################################

### TESTS FOR EVENT ID ###

# @pytest.mark.xfail
def test_eventId(event_validUpdateEventJson):
    assert event_validUpdateEventJson.eventId == "testEvent123"

# @pytest.mark.xfail
@pytest.mark.parametrize("json", [
    "{ \
        'userToken': 'testToken123', \
        'eventId': True, \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }",
    "{ \
        'userToken': 'testToken123', \
        'eventId': True, \
        'name': 'Weekly Soccer Practice' \
    }",
    "{ \
        'userToken': 'testToken123', \
        'eventId': True \
    }"
])
def test_eventIdInvalidType(json):
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

# @pytest.mark.xfail
@pytest.mark.parametrize("json", [
    "{ \
        'userToken': 'testToken123', \
        'eventId': '', \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }",
    "{ \
        'userToken': 'testToken123', \
        'eventId': '', \
        'name': 'Weekly Soccer Practice' \
    }",
    "{ \
        'userToken': 'testToken123', \
        'eventId': '' \
    }"
])
def test_eventIdEmpty(json):
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

### TESTS FOR USER IDS ###

# @pytest.mark.xfail
def test_userIds(event_validAddEventJson):
    assert event_validAddEventJson.userIds == ["user123", "user321"]

# @pytest.mark.xfail
def test_userIdsEmpty():
    json = "{ \
        'userToken': 'testToken123', \
        'userIds': [], \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }"
    event = calendarEvent.CalendarEvent(json, True)
    assert event_validJson.userIds == []

# @pytest.mark.xfail
def test_userIdsInvalid():
    json = "{ \
        'userToken': 'testToken123', \
        'userIds': [True, False], \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

### TESTS FOR EVENT TYPE ###

# @pytest.mark.xfail
def test_eventType(event_validAddEventJson):
    assert event_validAddEventJson.eventType == "practice"

# @pytest.mark.xfail
def test_eventTypeInvalid(json):
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': '', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

# @pytest.mark.xfail
def test_eventTypeEmpty(json):
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': '', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

### TEST FOR TIMES ###

# @pytest.mark.xfail
def test_times(event_validAddEventJson):
    assert event_validAddEventJson.times == {
        "from": time.strptime("2020-12-10T13:45:00Z", "%y-%m-%dT%H:%M:%SZ"),
        "to": time.strptime("2020-12-10T14:00:00Z", "%y-%m-%dT%H:%M:%SZ")
    }

# @pytest.mark.xfail
def test_timesMissingKey():
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice, \
        'name': 'Soccer Practice', \
        'times': { \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

# @pytest.mark.xfail
def test_timesInvalid():
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice, \
        'name': 'Soccer Practice', \
        'times': { \
            'from': True, \
            'to': False \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

# @pytest.mark.xfail
def test_timesEmpty():
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice, \
        'name': 'Soccer Practice', \
        'times': { \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

### TEST FOR DATES ###

# @pytest.mark.xfail
def test_dates(event_validAddEventJson):
    assert event_validAddEventJson.dates == {
        "from": time.strptime("2020-12-10", "%y-%m-%d"),
        "to": time.strptime("2020-12-10", "%y-%m-%d")
    }

# @pytest.mark.xfail
def test_datesMissingKey():
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice, \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'to': '2020-12-10' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

# @pytest.mark.xfail
def test_datesInvalid():
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice, \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': True, \
            'to': False \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

# @pytest.mark.xfail
def test_datesEmpty():
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)


### TEST FOR LOCATION ###

# @pytest.mark.xfail
def test_location(event_validAddEventJson):
    assert event_validAddEventJson.location == "Parents"

# @pytest.mark.xfail
def test_locationEmpty(event_validUpdateEventJson):
    assert event_validJson.location == ""

# @pytest.mark.xfail
def test_locationInvalid():
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'location': 123, \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2020-12-10' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)


### TEST FOR REPEATING ###

# @pytest.mark.xfail
def test_repeating(event_validAddEventJson):
    assert event_validAddEventJson.repeating == {
	    "frequency": calendarEvent.CalendarEventFrequency.Weekly,
        'daysOfWeek': [calendarEvent.DaysOfWeek.Monday, calendarEvent.DaysOfWeek.Wednesday],
        "from": time.strptime("2020-12-10", "%y-%m-%d"),
        "to": time.strptime("2020-01-10", "%y-%m-%d")
    }

# @pytest.mark.xfail
def test_repeatingEmpty(event_validUpdateEventJson):
    assert event_validUpdateEventJson.repeating == {}

# @pytest.mark.xfail
@pytest.mark.parametrize("json", [
    "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2021-12-10' \
        }, \
        'repeating': { \
            'daysOfWeek': ['M', 'W'], \
            'startDate': '2020-12-10', \
            'endDate': '2021-01-10' \
        } \
    }",
    "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2021-12-10' \
        }, \
        'repeating': { \
            'frequency': 'w', \
            'startDate': '2020-12-10', \
            'endDate': '2021-01-10' \
        } \
    }",
    "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2021-12-10' \
        }, \
        'repeating': { \
            'frequency': 'w', \
            'daysOfWeek': ['M', 'W'], \
            'endDate': '2021-01-10' \
        } \
    }",
    "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2021-12-10' \
        }, \
        'repeating': { \
            'frequency': 'w', \
            'daysOfWeek': ['M', 'W'], \
            'startDate': '2020-12-10', \
        } \
    }"
])
def test_repeatingMissingKey(json):
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)

def test_repeatingMissingKeyInvalid():
    json = "{ \
        'userToken': 'testToken123', \
        'eventType': 'practice', \
        'name': 'Soccer Practice', \
        'times': { \
            'from': '2020-12-10T13:45:00.000Z', \
            'to': '2020-12-10T14:00:00.000Z' \
        }, \
        'dates': { \
            'from': '2020-12-10', \
            'to': '2021-12-10' \
        }, \
        'repeating': { \
            'frequency': 'x', \
            'daysOfWeek': ['M', 'W'], \
            'startDate': '2020-12-10', \
            'endDate': '2021-01-10' \
        } \
    }"
    with pytest.raises(Exception("400")):
        calendarEvent.CalendarEvent(json, True)


### TEST FOR TO_DICT ###

def test_eventToDict(event_validAddEventJson):
    assert event_validAddEventJson.toDict() == {
        "userToken": "testToken123",
        "userIds": ["user123", "userId321"],
        "eventType": "practice",
        "name": "Soccer Practice",
        "location": "Parents",
        "times": {
            "from": time.strptime("2020-12-10T13:45:00Z", "%y-%m-%dT%H:%M:%SZ"),
            "to": time.strptime("2020-12-10T13:45:00Z", "%y-%m-%dT%H:%M:%SZ")
        },
        "dates": {
            "from": time.strptime("2020-12-10", "%y-%m-%d"),
            "to": time.strptime("2020-12-10", "%y-%m-%d")
        },
        "repeating": {
            {
                "frequency": calendarEvent.CalendarEventFrequency.Weekly,
                'daysOfWeek': [calendarEvent.DaysOfWeek.Monday, calendarEvent.DaysOfWeek.Wednesday],
                "from": time.strptime("2020-12-10", "%y-%m-%d"),
                "to": time.strptime("2020-01-10", "%y-%m-%d")
            }
        }
    }