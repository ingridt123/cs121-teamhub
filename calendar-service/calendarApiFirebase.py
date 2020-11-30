from google.cloud import firestore
import google.api_core.datetime_helpers
import google.api_core.exceptions
from google.oauth2.credentials import Credentials
from google.cloud.firestore import Client
import time

import calendarEvent
import calendarErrors

"""
Helper functions for all Firebase-related operations.
"""
FIREBASE_PROJECT_ID = "cs121-teamhub-test"

def getFirebaseClient(firebaseToken):
    """
    Initializes Cloud Firebase database client for interacting with the Google Cloud Firestore API.

    Parameters
        firebaseToken : str
            The Firebase token for the given user.

    Returns
        db : Client
            A client for interacting with the Firestore API.
    """
    # Get Firebase credentials using firebaseToken
    cred = Credentials(firebaseToken)

    # Return Cloud Firestore database client
    return Client(FIREBASE_PROJECT_ID, cred)


def getEventsReference(db, schoolId, teamId, eventId=None):
    """
    Gets Firebase database reference for the events of the given school and team id.

    Parameters
        db : Client
            A client for interacting with the Firestore API.
        schoolId : str
            The user's school id.
        teamId : str
            The user's team id.
        eventId : str, optional
            The event's id.

    Returns
        ref : CollectionReference or DocumentReference
            The reference for the events of the given school and team id.
    """
    # Get and return reference:
    #   schools -> schoolId -> teams -> teamId -> events -> eventId
    # If eventId is None, then return reference up to events collection.
    ref = db.collection(u'schools').document(schoolId).collection(u'teams').document(teamId).collection(u'events')
    if eventId != None:
        ref = ref.document(eventId)
    return ref


def getEvents(firebaseToken, schoolId, teamId, userId):
    """
    Gets all events for the given user id with their school and team id.

    Parameters
        firebaseToken : str
            The Firebase token for the given user.
        schoolId : str
            The user's school id.
        teamId : str
            The user's team id.
        userId : str
            The user's user id.

    Returns
        results : {str: <value>}
            The events returned from the database.
    """
    # Calls getFirebaseClient to get a client for interacting with the Firestore API
    db = getFirebaseClient(firebaseToken)

    # Calls getEventsReference to get the database reference
    ref = getEventsReference(db, schoolId, teamId)

    # Use Firebase function .where().stream() to get events from the database, using the
    #   conditions where the event has an empty list of userIds or userId is in the list
    # If fails while getting events, return "Error", 404
    try:
        docs1 = ref.where(u'userIds', u'==', []).stream()
        docs2 = ref.where(u'userIds', u'array_contains_any', [userId]).stream()
    except google.api_core.exceptions.GoogleAPIError:
        raise calendarErrors.Error404("GoogleAPIError")

    # Jsonifiy and return the results
    eventsList = []
    try:
        eventsList += extractEvents(docs1)
        eventsList += extractEvents(docs2)
    except calendarErrors.Error400 as e:
        raise calendarErrors.Error400(e.message)

    return eventsList


def extractEvents(docs):
    """ 
    Helper function for getEvents() to extract events from docs.

    docs : Document
        A document containing events from database.
    """
    eventsList = []
    for doc in docs:
        d = doc.to_dict()
        try:
            if "dates" in d:
                d["dates"]["from"] = d["dates"]["from"].rfc3339()
                d["dates"]["to"] = d["dates"]["to"].rfc3339()
            if "times" in d:
                d["times"]["from"] = d["times"]["from"].rfc3339()
                d["times"]["to"] = d["times"]["to"].rfc3339()
            if "repeating" in d:
                d["repeating"]["startDate"] = d["repeating"]["startDate"].rfc3339()
                d["repeating"]["endDate"] = d["repeating"]["endDate"].rfc3339()
        except KeyError:
            raise calendarErrors.Error400("Dict key(s) missing.")
        except ValueError:
            raise calendarErrors.Error400("Dict value(s) is/are invalid type or format.")
        eventsList.append(d)

    return eventsList


def addEvent(firebaseToken, schoolId, teamId, eventDict):
    """
    Adds eventDict to the events collection for the given school and team id.

    Parameters
        firebaseToken : str
            The Firebase token for the given user.
        schoolId : str
            The user's school id.
        teamId : str
            The user's team id.
        eventDict : dict()
            A dictionary representing the calendar event to be added to the database.
    """
    # Calls getFirebaseClient to get a client for interacting with the Firestore API
    db = getFirebaseClient(firebaseToken)

    # Calls getEventsReference to get the database reference
    ref = getEventsReference(db, schoolId, teamId)

    # Use Firebase function .add() to add eventDict to the database
    # If user not authorized to add event to database, return "Error", 401
    # If otherwise fails while adding event, return "Error", 404
    try:
        ref.add(eventDict)
    except google.api_core.exceptions.Unauthorized as e:
        raise calendarErrors.Error401(e.message)
    except google.api_core.exceptions.GoogleAPIError:
        raise calendarErrors.Error404("GoogleAPIError")
    

def updateEvent(firebaseToken, schoolId, teamId, eventId, eventDict):
    """
    Updates event to eventDict in the events collection for the given school and team id.

    Parameters
        firebaseToken : str
            The Firebase token for the given user.
        schoolId : str
            The user's school id.
        teamId : str
            The user's team id.
        eventId : str
            The event's id.
        eventDict : dict()
            A dictionary representing the calendar event to be updated in the database.
    """
    # Calls getFirebaseClient to get a client for interacting with the Firestore API
    db = getFirebaseClient(firebaseToken)

    # Calls getEventsReference to get the database reference
    ref = getEventsReference(db, schoolId, teamId, eventId)

    # Use Firebase function .update() to update event with eventId to eventDict in the database
    # If user not authorized to update event in database, return "Error", 401
    # If otherwise fails while updating event, return "Error", 404
    try:
        ref.update(eventDict)
    except google.api_core.exceptions.Unauthorized as e:
        raise calendarErrors.Error401(e.message)
    except google.api_core.exceptions.ClientError as e:
        raise calendarErrors.Error404(e.message)


def deleteEvent(firebaseToken, schoolId, teamId, eventId):
    """
    Deletes event with eventId from events collection for the given school and team id.

    Parameters
        firebaseToken : str
            The Firebase token for the given user.
        schoolId : str
            The user's school id.
        teamId : str
            The user's team id.
        eventId : str
            The event's id.
    """
    # Calls getFirebaseClient to get a client for interacting with the Firestore API
    db = getFirebaseClient(firebaseToken)

    # Calls getEventsReference to get the database reference
    ref = getEventsReference(db, schoolId, teamId, eventId)

    # Use Firebase function .delete() to delete event with eventId from the database
    # If user not authorized to delete event from database, return "Error", 401
    # If otherwise fails while deleting event, return "Error", 404
    try:
        ref.delete()
    except google.api_core.exceptions.Unauthorized as e:
        raise calendarErrors.Error401(e.message)
    except google.api_core.exceptions.GoogleAPIError:
        raise calendarErrors.Error404("GoogleAPIError")