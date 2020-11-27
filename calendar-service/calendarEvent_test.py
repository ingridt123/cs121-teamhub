import pytest

import time

import calendarEvent
import calendarErrors

""" Test file for CalendarEvent class. """

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

valid_addEvent_json = {
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

valid_updateEvent_json = {
    'userToken': valid_userToken,
    'eventId': valid_eventId,
    'name': valid_name2
}

valid_deleteEvent_json = {
    'userToken': valid_userToken,
    'eventId': valid_eventId
}

### FIXTURES ###

# Found that since dictionaries not creating deep copies when making
# changes in times and dates, so return deepcopy in calendarUtils
@pytest.fixture
def event_validAddEventJson():
    return calendarEvent.CalendarEvent(valid_addEvent_json, True)

@pytest.fixture
def event_validUpdateEventJson():
    return calendarEvent.CalendarEvent(valid_updateEvent_json, False)

###############################################################################
# TEST FUNCTIONS
###############################################################################

### TESTS FOR EVENT ID ###

# Found logic error in calendarUtils checking for whether field was in json
# as always raised exception if field not in json even if could be empty
def test_eventId(event_validUpdateEventJson):
    assert event_validUpdateEventJson.eventId == valid_eventId

# Tests immediately passed
@pytest.mark.parametrize("json", [
    {
        'userToken': valid_userToken,
        'eventId': True,
        'name': valid_name2
    },
    {
        'userToken': valid_userToken,
        'eventId': True
    }
])
def test_eventIdInvalidType(json):
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

# Tests immediately passed
def test_eventIdEmpty(event_validUpdateEventJson):
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(valid_updateEvent_json, True)

### TESTS FOR USER IDS ###

# Test immediately passed
def test_userIds(event_validAddEventJson):
    assert event_validAddEventJson.userIds == ["user123", "user321"]

# Test immediately passed
def test_userIdsEmpty():
    json = {
        'userToken': valid_userToken,
        'userIds': [],
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date1
        }
    }
    event = calendarEvent.CalendarEvent(json, True)
    assert event.userIds == []

# Found that code only checked that userIds was list, so added check that all
# elements of list were strings
def test_userIdsInvalid():
    json = {
        'userToken': valid_userToken,
        'userIds': ['a', False],
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

### TESTS FOR EVENT TYPE ###

# Found that accessing enum by programmatic access uses () not [] so made this change
# for eventType, frequency and daysOfWeek (latter two not directly tested here)
def test_eventType(event_validAddEventJson):
    assert event_validAddEventJson.eventType == calendarEvent.CalendarEventType.Practice.value

# Test immediately passed
def test_eventTypeInvalid():
    json = {
        'userToken': valid_userToken,
        'eventType': '',
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

# Test immediately passed
def test_eventTypeEmpty():
    json = {
        'userToken': valid_userToken,
        'eventType': '',
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

# ### TEST FOR TIMES ###

# Found that the correct date/time format uses %Y instead of %y since the century
# is also included in the date, and requires %f for millseconds
def test_times(event_validAddEventJson):
    assert event_validAddEventJson.times == {
        "from": time.strptime("2020-12-10T13:45:00.000Z", time_format),
        "to": time.strptime("2020-12-10T14:00:00.000Z", time_format)
    }

# Test immediately passed
# Test was originally incorrect as it anticipated raising an error, but it should not
def test_timesEmpty():
    json = {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date1
        }
    }
    event = calendarEvent.CalendarEvent(json, True)
    assert event.times == {}

# Test immediately passed
def test_timesMissingKey():
    json = {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

# Test immediately passed
def test_timesInvalid():
    json = {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': True,
            'to': False
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

# ### TEST FOR DATES ###

# Test immediately passed
def test_dates(event_validAddEventJson):
    assert event_validAddEventJson.dates == {
        "from": time.strptime(valid_date1, date_format),
        "to": time.strptime(valid_date1, date_format)
   }

# Test immediately passed
def test_datesMissingKey():
    json = {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'to': valid_date1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

# Test immediately passed
def test_datesInvalid():
    json = {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': True,
            'to': False
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

# Test immediately passed
def test_datesEmpty():
    json = {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)


# ### TEST FOR LOCATION ###

# Test immediately passed
def test_location(event_validAddEventJson):
    assert event_validAddEventJson.location == "Parents"

# Test immediately passed
def test_locationEmpty(event_validUpdateEventJson):
    assert event_validUpdateEventJson.location == ""

# Test immediately passed
def test_locationInvalid():
    json = {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'location': 123,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)


# ### TEST FOR REPEATING ###

# Test immediately passed
# Test incorrectly had "from" and "to" instead of "startDate" and "endDate"
def test_repeating(event_validAddEventJson):
    assert event_validAddEventJson.repeating == {
	    "frequency": calendarEvent.CalendarEventFrequency.Weekly.value,
        'daysOfWeek': [calendarEvent.DaysOfWeek.Monday.value, calendarEvent.DaysOfWeek.Wednesday.value],
        "startDate": time.strptime(valid_date1, date_format),
        "endDate": time.strptime(valid_date2, date_format)
    }

# Test immediately passed
def test_repeatingEmpty(event_validUpdateEventJson):
    assert event_validUpdateEventJson.repeating == {}

# Tests for json0, json2 and json3 immediately passed
# Test for json1 found that check for daysOfWeek should be list instead of string,
# and each item in daysOfWeek should be converted to the DaysOfWeek enum
@pytest.mark.parametrize("json", [
    {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date1
        },
        'repeating': {
            'daysOfWeek': valid_daysOfWeek,
            'startDate': valid_date1,
            'endDate': valid_date2
        }
    },
    {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date2
        },
        'repeating': {
            'frequency': valid_weeklyFreq,
            'startDate': valid_date1,
            'endDate': valid_date2
        }
    },
    {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date2
        },
        'repeating': {
            'frequency': valid_weeklyFreq,
            'daysOfWeek': valid_daysOfWeek,
            'endDate': valid_date2
        }
    },
    {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date2
        },
        'repeating': {
            'frequency': valid_weeklyFreq,
            'daysOfWeek': valid_daysOfWeek,
            'startDate': valid_date1,
        }
    }
])
def test_repeatingMissingKey(json):
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

# Test immediately passed
def test_repeatingMissingKeyInvalid():
    json = {
        'userToken': valid_userToken,
        'eventType': valid_eventType,
        'name': valid_name1,
        'times': {
            'from': valid_time1,
            'to': valid_time2
        },
        'dates': {
            'from': valid_date1,
            'to': valid_date2
        },
        'repeating': {
            'frequency': 'x',
            'daysOfWeek': valid_daysOfWeek,
            'startDate': valid_date1,
            'endDate': valid_date2
        }
    }
    with pytest.raises(ValueError):
        calendarEvent.CalendarEvent(json, True)


### TEST FOR TO_DICT ###

# Found that not checks for None and not empty string/list/dict thus need to check
# separately for that
# Also found that the time attribute was not included in the toDict method, so this was
# added
# Test also shouldn't include userToken as that is stored in the CalendarRequest object
# not the CalendarEvent object, so this key-value pair was removed
def test_eventToDict(event_validAddEventJson):
    assert event_validAddEventJson.toDict() == {
        "userIds": valid_userIds,
        "eventType": valid_eventType,
        "name": valid_name1,
        "location": valid_location,
        "times": {
            "from": time.strptime(valid_time1, time_format),
            "to": time.strptime(valid_time2, time_format)
        },
        "dates": {
            "from": time.strptime(valid_date1, date_format),
            "to": time.strptime(valid_date1, date_format)
        },
        "repeating": {
            "frequency": calendarEvent.CalendarEventFrequency.Weekly.value,
            'daysOfWeek': [calendarEvent.DaysOfWeek.Monday.value, calendarEvent.DaysOfWeek.Wednesday.value],
            "startDate": time.strptime(valid_date1, date_format),
            "endDate": time.strptime(valid_date2, date_format)
        }
    }