import datetime
import time
import enum

class CalendarEvent:
    """
    A class used to represent a calendar event.
    
    Attributes
        addEvent : bool
            A boolean that is True for adding events, False for updating events.
        eventId : str, optional
            The id associated with the calendar event in the database.
        userIds : [str], optional
            A list of ids of the users added to the event.
        eventType : CalendarEventType, optional
            The type of the event.
        name : str, optional
            The name of the event.
        times : {str: time}, optional
            A dictionary of string -> time of when the event begins and ends.
            Not specified if event is full-day or multiple full days.
        dates : {str: datetime}, optional
            A dictionary of string -> datetime of the date the event begins and ends (times is 00:00:00.000000).
            Date of first event if repeating event.
        location : str, optional
            The location of the event.
        description : str, optional
            The description of the event.
        repeating : {str: str}, optional
            The repeating configurations for the event.

    Rationale: This class was created to represent a calendar event and store all the 
    data related to an event, which makes the code more readable and allows for easier
    validation.
    """

    def __init__(self, json, addEvent):
        """
        Constructor for creating CalendarEvent objects.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
            addEvent : bool
                A boolean that is True for adding events, False for updating events.
        """
        # Set addEvent attribute

        # Extract required fields from JSON in request and use setter methods to populate attributes
        # If addEvent is True, required fields are eventType, name, dates
        # If addEvent is False, required field is eventId
        # If any of required fields not provided or invalid, return ("Error", 400)

        # Extract userId/teamId from JSON in request and use setter methods to populate attributes
        # If both fields in JSON, use teamId field
        # If neither field in JSON, set userId to user creating the event (from userToken)

        # Extract all other (optional) fields from JSON in request and use setter methods to populate attributes
        pass


    def setEventId(self, eventId):
        """
        Setter method to populate eventId attribute.

        Parameters
            eventId : str
        """
        # Verify that eventId is a string
        # Set self.eventId to eventId
        pass


    def setUserIds(self, memberIds):
        """
        Setter method to populate userIds attribute.

        Parameters
            userIds : [str]
        """
        # Verify that userId is a list of strings
        # Set self.userIds to userId
        pass


    def setEventType(self, eventType):
        """
        Setter method to populate eventType attribute.

        Parameters
            eventType : str
        """
        # Verify that eventType is a string and one of CalendarEventType's member values
        # Set self.eventType to CalendarEventType corresponding to eventType
        pass


    def setTimes(self, times):
        """
        Setter method to populate times attribute.

        Parameters
            times : {str: time}
        """
        # Verify that times' keys are strings "from" and "to"
        # Verify that times' values are times
        # Set self.times to times
        pass


    def setDates(self, dates):
        """
        Setter method to populate dates attribute.

        Parameters
            dates : {str: datetime}
        """
        # Verify that dates' keys are strings "from" and "to"
        # Verify that dates' values are datetimes
        # If dates' values' times not 00:00:00.000000, set to 00:00:00.000000
        # Set self.dates to dates
        pass

    
    def setLocation(self, location):
        """
        Setter method to populate location attribute.

        Parameters
            location : str
        """
        # Verify that location is a string
        # Set self.location to location
        pass


    def setRepeating(self, repeating):
        """
        Setter method to populate repeating attribute.

        Parameters
            repeating : {str: str}
        """
        # Verify that repeating' keys are strings "frequency", "startDate", "endDate"
        # If "frequency" is CalendarEventFrequency Weekly, then check for key "daysOfWeek"
        #   then set self.repeating "daysOfWeek" to corresponding DaysOfWeek
        # Set self.repeating "frequency" to corresponding CalendarEventFrequency
        # Set self.repeating "startDate" and "endDate" to repeating "startDate" and "endDate"
        pass


    def toDict(self):
        """
        Convert CalendarEvent object to dictionary.

        Returns
            dict : {str: <value>}
                A dictionary of the fields in the CalendarEvent object.
        """
        # Insert all required fields into dictionary
        # If addEvent is True, required fields are eventType, name, dates
        # If addEvent is False, required field is eventId

        # For all other attributes, insert into dictionary only if not None
        pass


"""
Rationale: use of enums to make validation easier and also to improve extensibility, 
as adding additional values just requires adding more enum values.
"""

class CalendarEventType(enum.Enum):
    """
    Enum for calendar event types.
    """
    Workout = "workout"
    Practice = "practice"
    Competition = "competition"
    Meeting = "meeting"
    TrainingRoom = "training room"


class CalendarEventFrequency(enum.Enum):
    """
    Enum for calendar event repeating frequency.
    """
    Daily = "d"
    Weekly = "w"
    Monthly = "m"
    Yearly = "y"


class DaysOfWeek(enum.Enum):
    """
    Enum for days of week.
    """
    Monday = "M"
    Tuesday = "T"
    Wednesday = "W"
    Thursday = "H"
    Friday = "F"
    Saturday = "S"
    Sunday = "U"