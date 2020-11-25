import logging as logger
from flask import Flask

import calendarEvent
import calendarRequest
import calendarApiFirebase

"""
The calendar service will be responsible for providing all services related to 
the calendar for the frontend (i.e. its operations will be called by the frontend 
through its external interface to read and write data to and from database). 
Specifically, the frontend can call the service to get, create, update and delete 
event(s) from/to the database. When performing these operations, the calendar 
service will check with the users service to ensure that the user has access.
"""
app = Flask(__name__)

@app.route('/events', methods=['GET'])
def getEvents():
    """
    Returns a list of the team and individual events for the given user.
    """
    # Get JSON from request
    # If BadRequest exception raised or empty JSON, return ("Error", 400)

    # Create CalendarRequest object to get all setup info for request
    # Return error if error is thrown, otherwise continue

    # Call calendarApiFirebase.getEvents() to get events from database
    # Return error if error is returned, otherwise continue

    # Return list of events (in JSON), 200 for success
    pass


@app.route('/events', methods=['POST'])
def addEvent():
    """
    Adds an event into the database with the given information.
    """
    # Get JSON from request
    # If BadRequest exception raised or empty JSON, return ("Error", 400)

    # Create CalendarRequest object to get all setup info for request
    # Return error if error is thrown, otherwise continue

    # Extract other data for event from JSON in request, create CalendarEvent object (addEvent = True)
    # Return error if error is returned, otherwise continue

    # Call calendarApiFirebase.addEvent() to add event to database
    # Return error if error is returned, otherwise continue

    # Return "Success", 201 for success
    pass


@app.route('/events', methods=['PUT'])
def updateEvent():
    """
    Updates the event in the database with the given information.
    """
    # Get JSON from request
    # If BadRequest exception raised or empty JSON, return ("Error", 400)

    # Create CalendarRequest object to get all setup info for request
    # Return error if error is thrown, otherwise continue

    # Extract other data for event from JSON in request, create CalendarEvent object (addEvent = False)
    # Return error if error is returned, otherwise continue

    # Call calendarApiFirebase.updateEvent() to update event in database
    # Return error if error is returned, otherwise continue

    # Return "Success", 201 for success
    pass


@app.route('/events', methods=['DELETE'])
def deleteEvent():
    """
    Deletes the event from the database.
    """
    # Get JSON from request
    # If BadRequest exception raised or empty JSON, return ("Error", 400)

    # Create CalendarRequest object to get all setup info for request
    # Return error if error is thrown, otherwise continue

    # Extract event id from JSON in request
    # If no event id provided or invalid, return "Error", 400

    # Call calendarApiFirebase.deleteEvent() to update event in database
    # Return error if error is returned, otherwise continue

    # Return "Success", 201 for success
    pass