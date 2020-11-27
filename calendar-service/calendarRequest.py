import logging as logger
import requests

import calendarErrors
from calendarUtils import CalendarUtils

class CalendarRequest:
    """
    A class used to store all information related to the calendar API request.

    Attributes
        json : {str: <value>}
            A dictionary representing data from the JSON object.
        userToken : str
            The user token passed from the front end.
        firebaseToken : str
            The Firebase token returned from the users service.
        schoolId : str
            The user's school id.
        teamId : str
            The user's team id.
    """

    def __init__(self, json):
        """
        Constructor for creating CalendarRequest objects.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
        # Set the json attribute to the json passed in
        self.json = json
        
        # Call the setter methods to populate all attributes
        self.setUserToken()
        self.setFirebaseToken()
        self.setSchoolAndTeamId()


    def getJson(self):
        """
        Gets json attribute.

        Returns
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
        return self.json


    def setUserToken(self):
        """
        Extract user token from request and populate userToken attribute.
        """

        # If no user token provided or invalid type, throw ("Error", 400)
        # Otherwise extract user token from JSON in request and set the userToken attribute
        self.userToken = CalendarUtils.checkFieldInJson(self.json, "userToken", "User token", str)


    def getUserToken(self):
        """
        Gets userToken attribute.

        Returns
            userToken : str
                The user token passed from the front end.
        """
        return self.userToken


    def setFirebaseToken(self):
        """
        Gets Firebase token from user token and populates the firebaseToken attribute.
        """

        # Call GET /check_token in users service to verify and get Firebase token
        # If invalid token or Firebase token empty, throw ("Error", 401)
        request = requests.get('localhost://checktoken')
        if request.status_code != 200:
            raise calendarErrors.Error401("User token is invalid")
        json = request.json() 

        if json == None:
            raise calendarErrors.Error401("Could not get Firebase token from users service")

        # Otherwise set the firebaseToken attribute
        self.firebaseToken = CalendarUtils.checkFieldInJson(json, "firebaseToken", "Firebase token", str)

    
    def getFirebaseToken(self):
        """
        Gets the firebaseToken attribute.

        Returns
            firebaseToken : str
                The Firebase token returned from the users service.
        """
        return self.firebaseToken


    def setSchoolAndTeamId(self):
        """
        Get school and team id the user is affiliated with and populates the schoolId and teamId attributes.
        """
        
        # Call GET /users/current in users service to get user's school and team ids
        # If error or one/both id(s) empty, throw ("Error", 404)
        request = requests.get("localhost://users/current", params={'userToken': self.userToken})
        if request.status_code != 200:
            raise calendarErrors.Error400("Error getting school and/or team id")
        json = request.json()

        if json == None:
            raise calendarErrors.Error400("Could not get school and/or team id from users service")

        # Otherwise set the schoolId and teamId attributes
        self.schoolId = CalendarUtils.checkFieldInJson(json, "schoolId", "School id", str)
        self.teamId = CalendarUtils.checkFieldInJson(json, "teamId", "Team id", str)


    def getSchoolId(self):
        """
        Gets the schoolId attribute.

        Returns
            schoolId : str
                The user's school id.
        """
        return self.schoolId


    def getTeamId(self):
        """
        Gets the teamId attribute.

        Returns
            teamId : id
                The user's team id.
        """
        return self.teamId