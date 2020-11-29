from flask import Flask, jsonify, make_response, request
from werkzeug.exceptions import BadRequest

import calendarEvent
import calendarRequest
import calendarApiFirebase
import calendarErrors

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
    try:
        json = request.get_json()
    except request.BadRequest:
        return "Error", 400

    # Create CalendarRequest object to get all setup info for request
    # Return error if error is thrown, otherwise continue
    try:
        calRequest = calendarRequest.CalendarRequest(json)
    except calendarErrors.Error400 as e:
        return e.message, 400
    except calendarErrors.Error401 as e:
        return e.message, 401

    # Call calendarApiFirebase.getEvents() to get events from database
    # Return error if error is returned, otherwise continue
    try:
        calEvents = calendarApiFirebase.getEvents(calRequest.getFirebaseToken(), \
            calRequest.getSchoolId(), calRequest.getTeamId(), calRequest.getUserToken())
    except calendarErrors.Error401 as e:
        return e.message, 401
    except calendarErrors.Error404 as e:
        return e.message, 404

    # # Return list of events (in JSON), 200 for success
    return calEvents, 200


@app.route('/events', methods=['POST'])
def addEvent():
    """
    Adds an event into the database with the given information.
    """
    # Get JSON from request
    # If BadRequest exception raised or empty JSON, return ("Error", 400)
    try:
        json = request.get_json()
    except request.BadRequest:
        return "Error", 400

    # Create CalendarRequest object to get all setup info for request
    # Return error if error is thrown, otherwise continue
    try:
        calRequest = calendarRequest.CalendarRequest(json)
    except calendarErrors.Error400 as e:
        return e.message, 400
    except calendarErrors.Error401 as e:
        return e.message, 401

    # Extract other data for event from JSON in request, create CalendarEvent object (addEvent = True)
    # Return error if error is returned, otherwise continue
    try:
        calEvent = calendarEvent.CalendarEvent(json, True)
    except calendarErrors.Error400 as e:
        return e.message, 400

    # Call calendarApiFirebase.addEvent() to add event to database
    # Return error if error is returned, otherwise continue
    try:
        calendarApiFirebase.addEvent(calRequest.getFirebaseToken(), calRequest.getSchoolId(), \
            calRequest.getTeamId(), calEvent.toDict())
    except calendarErrors.Error401 as e:
        return e.message, 401
    except calendarErrors.Error404 as e:
        return e.message, 404

    # Return "Success", 201 for success
    return "Success", 201


@app.route('/events', methods=['PUT'])
def updateEvent():
    """
    Updates the event in the database with the given information.
    """
    # Get JSON from request
    # If BadRequest exception raised or empty JSON, return ("Error", 400)
    try:
        json = request.get_json()
    except request.BadRequest:
        return "Error", 400

    # Create CalendarRequest object to get all setup info for request
    # Return error if error is thrown, otherwise continue
    try:
        calRequest = calendarRequest.CalendarRequest(json)
    except calendarErrors.Error400 as e:
        return e.message, 400
    except calendarErrors.Error401 as e:
        return e.message, 401

    # Extract other data for event from JSON in request, create CalendarEvent object (addEvent = False)
    # Return error if error is returned, otherwise continue
    try:
        calEvent = calendarEvent.CalendarEvent(json, False)
    except calendarErrors.Error400 as e:
        return e.message, 400

    # Call calendarApiFirebase.updateEvent() to update event in database
    # Return error if error is returned, otherwise continue
    try:
        calendarApiFirebase.updateEvent(calRequest.getFirebaseToken(), calRequest.getSchoolId(), \
            calRequest.getTeamId(), calEvent.getEventId(), calEvent.toDict())
    except calendarErrors.Error401 as e:
        return e.message, 401
    except calendarErrors.Error404 as e:
        return e.message, 404

    # Return "Success", 201 for success
    return "Success", 201


@app.route('/events', methods=['DELETE'])
def deleteEvent():
    """
    Deletes the event from the database.
    """
    # Get JSON from request
    # If BadRequest exception raised or empty JSON, return ("Error", 400)
    try:
        json = request.get_json()
    except request.BadRequest:
        return "Error", 400

    # Create CalendarRequest object to get all setup info for request
    # Return error if error is thrown, otherwise continue
    try:
        calRequest = calendarRequest.CalendarRequest(json)
    except calendarErrors.Error400 as e:
        return e.message, 400
    except calendarErrors.Error401 as e:
        return e.message, 401

    # Extract other data for event from JSON in request, create CalendarEvent object (addEvent = False)
    # Return error if error is returned, otherwise continue
    try:
        calEvent = calendarEvent.CalendarEvent(json, False)
    except calendarErrors.Error400 as e:
        return e.message, 400

    # Call calendarApiFirebase.deleteEvent() to update event in database
    # Return error if error is returned, otherwise continue
    calendarApiFirebase.deleteEvent(calRequest.getFirebaseToken(), calRequest.getSchoolId(), \
        calRequest.getTeamId(), calEvent.getEventId())

    # Return "Success", 201 for success
    return "Success", 201