import pytest

import google.api_core.datetime_helpers

import calendarEvent
import calendarErrors
from testConstants import *

""" Test file for CalendarEvent class. """

###############################################################################
# FIXTURES
###############################################################################

# Found that since dictionaries not creating deep copies when making
# changes in times and dates, so return deepcopy in calendarUtils
@pytest.fixture
def event_validAddEventJson():
    return calendarEvent.CalendarEvent(valid_json_add1, True)

@pytest.fixture
def event_validUpdateEventJson():
    return calendarEvent.CalendarEvent(valid_json_update, False)

###############################################################################
# TEST FUNCTIONS
###############################################################################

### TESTS FOR EVENT ID ###

# Found logic error in calendarUtils checking for whether field was in json
# as always raised exception if field not in json even if could be empty
def test_eventId(event_validUpdateEventJson):
    assert event_validUpdateEventJson.eventId == EVENT2_ID

# Tests immediately passed
def test_eventIdInvalidType():
    invalid_json = {
        'userToken': USER_ID,
        'eventId': True,
        'name': EVENT1_NAME
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(invalid_json, True)

# Tests immediately passed
def test_eventIdEmpty(event_validUpdateEventJson):
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(valid_json_update, True)

### TESTS FOR USER IDS ###

# Test immediately passed
def test_userIds(event_validAddEventJson):
    assert event_validAddEventJson.userIds == EVENT1_USERIDS

# Test immediately passed
def test_userIdsEmpty():
    json = {
        'userToken': USER_ID,
        'userIds': [],
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
    event = calendarEvent.CalendarEvent(json, True)
    assert event.userIds == []

# Found that code only checked that userIds was list, so added check that all
# elements of list were strings
def test_userIdsInvalid():
    json = {
        'userToken': USER_ID,
        'userIds': ['a', False],
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
        calendarEvent.CalendarEvent(json, True)

### TESTS FOR EVENT TYPE ###

# Found that accessing enum by programmatic access uses () not [] so made this change
# for eventType, frequency and daysOfWeek (latter two not directly tested here)
def test_eventType(event_validAddEventJson):
    assert event_validAddEventJson.eventType == calendarEvent.CalendarEventType.Practice.value

# Test immediately passed
def test_eventTypeInvalid():
    json = {
        'userToken': USER_ID,
        'eventType': '',
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
        calendarEvent.CalendarEvent(json, True)

# Test immediately passed
def test_eventTypeEmpty():
    invalid_json = {
        'userToken': USER_ID,
        'eventType': '',
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
        calendarEvent.CalendarEvent(invalid_json, True)

# ### TEST FOR TIMES ###

# Found that the correct date/time format uses %Y instead of %y since the century
# is also included in the date, and requires %f for millseconds
def test_times(event_validAddEventJson):
    assert event_validAddEventJson.times == {
        "from": google.api_core.datetime_helpers.from_rfc3339(EVENT1_TIME1),
        "to": google.api_core.datetime_helpers.from_rfc3339(EVENT1_TIME2)
    }

# Test immediately passed
# Test was originally incorrect as it anticipated raising an error, but it should not
def test_timesEmpty():
    json = {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE1
        }
    }
    event = calendarEvent.CalendarEvent(json, True)
    assert event.times == None

# Test immediately passed
def test_timesMissingKey():
    invalid_json = {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'to': EVENT1_TIME2
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(invalid_json, True)

# Test immediately passed
def test_timesInvalid():
    invalid_json = {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'from': True,
            'to': False
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(invalid_json, True)

# ### TEST FOR DATES ###

# Test immediately passed
def test_dates(event_validAddEventJson):
    assert event_validAddEventJson.dates == {
        "from": google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE1),
        "to": google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE1)
    }

# Test immediately passed
def test_datesMissingKey():
    invalid_json = {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
            'to': EVENT1_DATE1
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(invalid_json, True)

# Test immediately passed
def test_datesInvalid():
    invalid_json = {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
            'from': True,
            'to': False
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(invalid_json, True)

# Test immediately passed
def test_datesEmpty():
    invalid_json = {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
        }
    }
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(invalid_json, True)


# ### TEST FOR LOCATION ###

# Test immediately passed
def test_location(event_validAddEventJson):
    assert event_validAddEventJson.location == EVENT1_LOCATION

# Test immediately passed
def test_locationEmpty(event_validUpdateEventJson):
    assert event_validUpdateEventJson.location == None

# Test immediately passed
def test_locationInvalid():
    invalid_json = {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'location': 123,
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
        calendarEvent.CalendarEvent(invalid_json, True)


# ### TEST FOR REPEATING ###

# Test immediately passed
# Test incorrectly had "from" and "to" instead of "startDate" and "endDate"
def test_repeating(event_validAddEventJson):
    assert event_validAddEventJson.repeating == {
	    "frequency": EVENT1_REPEATINGFREQ,
        'daysOfWeek': EVENT1_REPEATINGDAYS,
        "startDate": google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE1),
        "endDate": google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE2)
    }

# Test immediately passed
def test_repeatingEmpty(event_validUpdateEventJson):
    assert event_validUpdateEventJson.repeating == None

# Tests for json0, json2 and json3 immediately passed
# Test for json1 found that check for daysOfWeek should be list instead of string,
# and each item in daysOfWeek should be converted to the DaysOfWeek enum
@pytest.mark.parametrize("json", [
    {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE1
        },
        'repeating': {
            'daysOfWeek': EVENT1_REPEATINGDAYS,
            'startDate': EVENT1_DATE1,
            'endDate': EVENT1_DATE2
        }
    },
    {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE2
        },
        'repeating': {
            'frequency': EVENT1_REPEATINGFREQ,
            'startDate': EVENT1_DATE1,
            'endDate': EVENT1_DATE2
        }
    },
    {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE2
        },
        'repeating': {
            'frequency': EVENT1_REPEATINGFREQ,
            'daysOfWeek': EVENT1_REPEATINGDAYS,
            'endDate': EVENT1_DATE2
        }
    },
    {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE2
        },
        'repeating': {
            'frequency': EVENT1_REPEATINGFREQ,
            'daysOfWeek': EVENT1_REPEATINGDAYS,
            'startDate': EVENT1_DATE1,
        }
    }
])
def test_repeatingMissingKey(json):
    with pytest.raises(calendarErrors.Error400):
        calendarEvent.CalendarEvent(json, True)

# Test immediately passed
def test_repeatingMissingKeyInvalid():
    invalid_json = {
        'userToken': USER_ID,
        'eventType': EVENT1_EVENTTYPE,
        'name': EVENT1_NAME,
        'times': {
            'from': EVENT1_TIME1,
            'to': EVENT1_TIME2
        },
        'dates': {
            'from': EVENT1_DATE1,
            'to': EVENT1_DATE2
        },
        'repeating': {
            'frequency': 'x',
            'daysOfWeek': EVENT1_REPEATINGDAYS,
            'startDate': EVENT1_DATE1,
            'endDate': EVENT1_DATE2
        }
    }
    with pytest.raises(ValueError):
        calendarEvent.CalendarEvent(invalid_json, True)


### TEST FOR TO_DICT ###

# Found that not checks for None and not empty string/list/dict thus need to check
# separately for that
# Also found that the time attribute was not included in the toDict method, so this was
# added
# Test also shouldn't include userToken as that is stored in the CalendarRequest object
# not the CalendarEvent object, so this key-value pair was removed
def test_eventToDict(event_validAddEventJson):
    assert event_validAddEventJson.toDict() == {
        "userIds": EVENT1_USERIDS,
        "eventType": EVENT1_EVENTTYPE,
        "name": EVENT1_NAME,
        "location": EVENT1_LOCATION,
        "times": {
            "from": google.api_core.datetime_helpers.from_rfc3339(EVENT1_TIME1),
            "to": google.api_core.datetime_helpers.from_rfc3339(EVENT1_TIME2)
        },
        "dates": {
            "from": google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE1),
            "to": google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE1)
        },
        "repeating": {
            "frequency": EVENT1_REPEATINGFREQ,
            'daysOfWeek': EVENT1_REPEATINGDAYS,
            "startDate": google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE1),
            "endDate": google.api_core.datetime_helpers.from_rfc3339(EVENT1_DATE2)
        }
    }