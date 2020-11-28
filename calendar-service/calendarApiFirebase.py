from google.cloud import firestore
# import google.api_core.datetime_helpers.DatetimeWithNanoseconds
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import time

import calendarEvent
import calendarErrors

"""
Helper functions for all Firebase-related operations.
"""
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
    # Get Firebase credentials using JSON file and firebaseToken
    cred = credentials.Certificate('./key.json') #TODO: ???

    # Initialize Firebase app using credentials
    firebase_admin.initialize_app(cred)

    # Return Cloud Firestore database client
    return firestore.client()


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
    # If fails while getting events, return "Error", 404 TODO no need?
    try:
        docs1 = ref.where(u'userIds', u'==', []).stream()
        docs2 = ref.where(u'userIds', u'array_contains_any', [userId]).stream()
    except Exception:
        raise calendarErrors.Error404("Error getting events from database")

    # Jsonifiy and return the results
    eventsList = []
    for d in docs1:
        eventsList.append(d)
    for d in docs2:
        eventsList.append(d)
    # eventsList = extractEvents(docs1)
    # eventsList += extractEvents(docs2)
    return eventsList


def extractEvents(docs):
    """ 
    Helper function for getEvents() to extract events from docs.

    docs : Document
        A document containing events from database.
    """
    # eventsList = []
    # for d in docs:
    #     if "dates" in d:
    #         d["dates"]["from"] = time.strptime

    # return []


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
    # If otherwise fails while adding event, return "Error", 404 TODO: no need?
    ref.add(eventDict)
    

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
    # If user not authorized to update event in database, return "Error", 401 TODO no need?
    # If otherwise fails while updating event, return "Error", 404
    ref.update(eventDict)


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
    # If user not authorized to delete event from database, return "Error", 401 TODO no need?
    # If otherwise fails while deleting event, return "Error", 404
    ref.delete()