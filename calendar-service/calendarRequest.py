import logging as logger

class CalendarRequest:
    """
    A class used to store all information related to the calendar API request.

    Attributes
        json : str
            A string representing data from the JSON object.
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
            json : str
                A string representing data from the JSON object.
        """
        # Set the json attribute to the json passed in
        # Call the setter methods to populate all attributes
        pass


    def getJson(self):
        """
        Gets json attribute.

        Returns
            json : str
                A string representing data from the JSON object.
        """
        pass


    def setUserToken(self):
        """
        Extract user token from request and populate userToken attribute.
        """
        # Extract user token from JSON in request 
        # If no user token provided or invalid type, throw ("Error", 400)
        # Otherwise set the userToken attribute
        pass


    def getUserToken(self):
        """
        Gets userToken attribute.

        Returns
            userToken : str
                The user token passed from the front end.
        """
        pass


    def setFirebaseToken(self):
        """
        Gets Firebase token from user token and populates the firebaseToken attribute.

        
        """
        # Call GET /check_token in users service to verify and get Firebase token
        # If invalid token or Firebase token empty, throw ("Error", 401)
        # Otherwise set the firebaseToken attribute
        pass

    
    def getFirebaseToken(self):
        """
        Gets the firebaseToken attribute.

        Returns
            firebaseToken : str
                The Firebase token returned from the users service.
        """
        pass



    def setSchoolAndTeamId(self):
        """
        Get school and team id the user is affiliated with and populates the schoolId and teamId attributes.
        """
        # Call GET /users/current in users service to get user's school and team ids
        # If error or one/both id(s) empty, throw ("Error", 404)
        # Otherwise set the schoolId and teamId attributes
        pass


    def getSchoolId(self):
        """
        Gets the schoolId attribute.

        Returns
            schoolId : str
                The user's school id.
        """
        pass


    def getTeamId(self):
        """
        Gets the teamId attribute.

        Returns
            teamId : id
                The user's team id.
        """
        pass