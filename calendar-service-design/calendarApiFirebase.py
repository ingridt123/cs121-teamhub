from google.cloud import firestore
from firebase_admin import credentials, firestore, initialize_app

import calendarEvent

"""
Helper functions for all Firebase-related operations.

Rationale: All of the operations related to communicating with Firebase is
put in this class to promote modularity and readability. Only this class will
need to be altered if we use firebase for another database, for example.
"""

"""
Rationale for change: The getFirebaseClient() function was added in response to
an issue raised during the reviews, since before communicating with the Firebase
database, a client must be created, with configurations such as the credentials 
and project ID, to communicate with the Firestore API. In addition, due to the
changes described above, the functions getEvents(), addEvent(), updateEvent() and
deleteEvent() have an added firebaseToken parameter to initilize the Firestore
client. The getEventsReference() will then take in the Firestore client to get
the reference using this client.
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
    # Initialize Firebase app using credentials
    # Return Cloud Firestore database client
    pass


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
    pass


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
    # Calls getEventsReference to get the database reference
    # Use Firebase function .where().stream() to get events from the database, using the
    #   conditions where the event has an empty list of userIds or userId is in the list
    # If fails while getting events, return "Error", 404

    # Jsonifiy and return the results
    pass


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
    # Calls getEventsReference to get the database reference
    # Use Firebase function .add() to add eventDict to the database
    # If user not authorized to add event to database, return "Error", 401
    # If otherwise fails while adding event, return "Error", 404
    pass


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
    # Calls getEventsReference to get the database reference
    # Use Firebase function .update() to update event with eventId to eventDict in the database
    # If user not authorized to update event in database, return "Error", 401
    # If otherwise fails while updating event, return "Error", 404
    pass


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
    # Calls getEventsReference to get the database reference
    # Use Firebase function .delete() to delete event with eventId from the database
    # If user not authorized to delete event from database, return "Error", 401
    # If otherwise fails while deleting event, return "Error", 404
    pass