""" Constants for testing. """

### USERS SERVICE ###

CHECK_TOKEN_URL = "localhost://checktoken"
CURRENT_USERS_URL = "localhost://users/current"

FIREBASE_TOKEN = 'testToken321'
SCHOOL_ID = 'school1'
TEAM_ID = 'team123'


### FLASK ###

FLASK_ENDPOINT = '/events'


### FIREBASE ###

FIREBASE_PATH = 'schools/' + SCHOOL_ID + '/teams/' + TEAM_ID + '/events'


### EVENTS ###

USER_ID = 'user123'

EVENT1_ID = 'gkjtuYvCOGkiVeEsmD7T'
EVENT1_USERIDS, EVENT1_EVENTTYPE, EVENT1_NAME, EVENT1_LOCATION = \
    [USER_ID, 'user321'], 'practice', 'Soccer Practice', 'Parents'
EVENT1_TIME1, EVENT1_TIME2, EVENT1_DATE1, EVENT1_DATE2 = \
    '2020-12-10T07:45:00.000000Z', '2020-12-10T08:00:00.000000Z', \
    '2020-12-10T00:00:00.000000Z', '2021-01-10T00:00:00.000000Z'
EVENT1_REPEATINGFREQ, EVENT1_REPEATINGDAYS = \
    'w', ['M', 'W']

EVENT2_ID = '0d3IKB9awt0FtzN7z1Qv'
EVENT2_USERIDS, EVENT2_EVENTTYPE, EVENT2_NAME, EVENT2_LOCATION = \
    ['user456', 'user234'], 'practice', 'Basketball Practice', 'Rains'
EVENT2_DATE1 = \
    '2020-11-12T00:00:00.000000Z'

EVENT3_ID = '6w3mDhxwunaqVOVvUqDG'
EVENT3_USERIDS, EVENT3_EVENTTYPE, EVENT3_NAME = \
    [], 'competition', 'Track Meet'
EVENT3_DATE1 = \
    '2020-11-08T00:00:00.000000Z'

EVENT4_USERIDS, EVENT4_EVENTTYPE, EVENT4_NAME, EVENT4_LOCATION = \
    [], 'practice', 'Softball Practice', 'Pritzlaff'
EVENT4_DATE1, EVENT4_DATE2, EVENT4_TIME1, EVENT4_TIME2 = \
    '2020-12-28T00:00:00.000000Z', '2021-12-28T00:00:00.000000Z', \
    '2020-12-28T10:00:00.000000Z', '2020-12-28T18:00:00.000000Z'
EVENT4_REPEATINGFREQ, EVENT4_REPEATINGDAYS = \
    'w', ['W']


### JSON ###

event1 = {
    'location': EVENT1_LOCATION, 
    'eventType': EVENT1_EVENTTYPE, 
    'repeating': {
        'frequency': EVENT1_REPEATINGFREQ, 
        'daysOfWeek': EVENT1_REPEATINGDAYS, 
        'startDate': EVENT1_DATE1,
        'endDate': EVENT1_DATE2
    }, 
    'times': {
        'from': EVENT1_TIME1,
        'to': EVENT1_TIME2
    },
    'dates': {
        'to': EVENT1_DATE1,
        'from': EVENT1_DATE1
    },
    'userIds': EVENT1_USERIDS,
    'name': EVENT1_NAME
}

event2_afterUpdate = {
    "userIds": [],
    "name": EVENT2_NAME,
    "location": EVENT2_LOCATION,
    "eventType": EVENT2_EVENTTYPE,
    "dates": {
        "from": EVENT2_DATE1,
        "to": EVENT2_DATE1
    }
}

event3 = {
    'dates': {
        'to': EVENT3_DATE1,
        'from': EVENT3_DATE1
    }, 
    'name': EVENT3_NAME, 
    'eventType': EVENT3_EVENTTYPE, 
    'userIds': EVENT3_USERIDS
}

event4 = {
    "userIds": EVENT4_USERIDS,
    "eventType": EVENT4_EVENTTYPE,
    "name": EVENT4_NAME,
    "location": EVENT4_LOCATION,
    "times": {
        "from": EVENT4_TIME1,
        "to": EVENT4_TIME2
    },
    "dates": {
        "from": EVENT4_DATE1,
        "to": EVENT4_DATE1
    },
    "repeating": {
        "frequency": EVENT4_REPEATINGFREQ,
        'daysOfWeek': EVENT4_REPEATINGDAYS,
        "startDate": EVENT4_DATE1,
        "endDate": EVENT4_DATE2
    }
}

valid_json = {
    'userToken': USER_ID, 
    'eventType': EVENT1_EVENTTYPE, 
    'name': EVENT1_NAME, 
    'times': { 
        'from': EVENT1_TIME1, 
        'to':  EVENT1_TIME2
    }, 
    'dates': { 
        'from': EVENT1_DATE1, 
        'to': EVENT1_DATE1
    } 
}

valid_json_get = {
    'userToken': USER_ID
}

valid_json_add1 = {
    'userToken': USER_ID,
    'userIds': EVENT1_USERIDS,
    'eventType': EVENT1_EVENTTYPE,
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

valid_json_add2 = {
    'userToken': USER_ID,
    "userIds": EVENT4_USERIDS,
    "eventType": EVENT4_EVENTTYPE,
    "name": EVENT4_NAME,
    "location": EVENT4_LOCATION,
    "times": {
        "from": EVENT4_TIME1,
        "to": EVENT4_TIME2
    },
    "dates": {
        "from": EVENT4_DATE1,
        "to": EVENT4_DATE1
    },
    "repeating": {
        "frequency": EVENT4_REPEATINGFREQ,
        'daysOfWeek': EVENT4_REPEATINGDAYS,
        "startDate": EVENT4_DATE1,
        "endDate": EVENT4_DATE2
    }
}

valid_json_update = {
    'userToken': USER_ID,
    'eventId': EVENT2_ID,
    'userIds': []
}

valid_json_delete = {
    'userToken': USER_ID,
    'eventId': EVENT1_ID,
}