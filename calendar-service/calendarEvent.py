import time
import enum

import calendarErrors
from calendarUtils import CalendarUtils

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
        self.addEvent = addEvent

        # Extract required fields from JSON in request and use setter methods to populate attributes
        # If addEvent is True, required fields are eventType, name, dates
        # If addEvent is False, required field is eventId
        # If any of required fields not provided or invalid, return ("Error", 400)
        self.setEventId(json)
        self.setEventType(json)
        self.setName(json)
        self.setDates(json)

        # Extract all other (optional) fields from JSON in request and use setter methods to populate attributes
        self.setUserIds(json)
        self.setTimes(json)
        self.setLocation(json)
        self.setRepeating(json)


    def setEventId(self, json):
        """
        Setter method to populate eventId attribute.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
        # No eventId if adding new event
        # Verify that eventId is a string
        # Set self.eventId to eventId
        if self.addEvent:
            self.eventId = ""
        else:
            self.eventId = CalendarUtils.checkFieldInJson(json, "eventId", "Event id", str)


    def setEventType(self, json):
        """
        Setter method to populate eventType attribute.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
        # Verify that eventType is a string 
        # Set self.eventType to CalendarEventType corresponding to eventType
        self.eventType = CalendarUtils.checkFieldInJson(json, "eventType", "Event type", str, not self.addEvent)

        # Verify that eventType is one of CalendarEventType's member values
        if self.eventType != "":
            try:
                self.eventType = CalendarEventType(self.eventType).value
            except KeyError:
                raise calendarErrors.Error400("Event type is invalid value")


    def setName(self, json):
        """
        Setter method to populate name attribute.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
        # Verify that name is a string
        # Set self.name to name
        self.name = CalendarUtils.checkFieldInJson(json, "name", "Name", str, not self.addEvent)


    def setDates(self, json):
        """
        Setter method to populate dates attribute.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
    
        # Set self.dates to dates
        self.dates = CalendarUtils.checkFieldInJson(json, "dates", "Dates", dict, not self.addEvent)

        # Verify that dates' keys are strings "from" and "to"
        if self.dates != {}:
            self.dates["from"] = CalendarUtils.checkFieldInJson(self.dates, "from", "Dates (from)", str)
            self.dates["to"] = CalendarUtils.checkFieldInJson(self.dates, "to", "Dates (to)", str)

            # Verify that dates' values can be extracted as dates
            # If dates' values' times not 00:00:00.000000, set to 00:00:00.000000
            try:
                self.dates["from"] = time.strptime(self.dates["from"], "%Y-%m-%d")
                self.dates["to"] = time.strptime(self.dates["to"], "%Y-%m-%d")
            except ValueError:
                raise calendarErrors.Error400("Dates dict key(s) is/are invalid type or format.")
    

    def setUserIds(self, json):
        """
        Setter method to populate userIds attribute.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
        # Verify that userId is a list of strings
        # Set self.userIds to userId
        if "userIds" not in json:
            self.userIds = []
        else:
            self.userIds = CalendarUtils.checkFieldInJson(json, "userIds", "User ids", list, True)
            if not all(type(i) == str for i in self.userIds):
                raise calendarErrors.Error400("User id element(s) is/are invalid type.")
        print(self.userIds)


    def setTimes(self, json):
        """
        Setter method to populate times attribute.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
        
        # Set self.times to times
        self.times = CalendarUtils.checkFieldInJson(json, "times", "Times", dict, True)

        # Verify that times' keys are strings "from" and "to"
        if self.times != {}:
            self.times["from"] = CalendarUtils.checkFieldInJson(self.times, "from", "Times (from)", str)
            self.times["to"] = CalendarUtils.checkFieldInJson(self.times, "to", "Times (to)", str)

            # Verify that times' values can be extracted as times
            try:
                self.times["from"] = time.strptime(self.times["from"], "%Y-%m-%dT%H:%M:%S.%fZ")
                self.times["to"] = time.strptime(self.times["to"], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                raise calendarErrors.Error400("Times dict key(s) is/are invalid type or format.")

    
    def setLocation(self, json):
        """
        Setter method to populate location attribute.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
        # Verify that location is a string
        # Set self.location to location
        self.location = CalendarUtils.checkFieldInJson(json, "location", "Location", str, True)


    def setRepeating(self, json):
        """
        Setter method to populate repeating attribute.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
        """
        # Verify that repeating' keys are strings "frequency", "startDate", "endDate"
        self.repeating = CalendarUtils.checkFieldInJson(json, "repeating", "Repeating", dict, True)
        if self.repeating != {}:
            self.repeating["frequency"] = CalendarUtils.checkFieldInJson(self.repeating, "frequency", "Repeating (frequency)", str)
            self.repeating["startDate"] = CalendarUtils.checkFieldInJson(self.repeating, "startDate", "Repeating (startDate)", str)
            self.repeating["endDate"] = CalendarUtils.checkFieldInJson(self.repeating, "endDate", "Repeating (endDate)", str)

            # Set self.repeating "frequency" to corresponding CalendarEventFrequency
            self.repeating["frequency"] = CalendarEventFrequency(self.repeating["frequency"]).value

            # If "frequency" is CalendarEventFrequency Weekly, then check for key "daysOfWeek"
            #   then set self.repeating "daysOfWeek" to corresponding DaysOfWeek
            if self.repeating["frequency"] == CalendarEventFrequency.Weekly.value:
                self.repeating["daysOfWeek"] = CalendarUtils.checkFieldInJson(self.repeating, "daysOfWeek", "Repeating (daysOfWeek)", list)
                self.repeating["daysOfWeek"] = [DaysOfWeek(d).value for d in self.repeating["daysOfWeek"]]

            # Verify that startDate and endDate values can be extracted as dates

            try:
                self.repeating["startDate"] = time.strptime(self.repeating["startDate"], "%Y-%m-%d")
                self.repeating["endDate"] = time.strptime(self.repeating["endDate"], "%Y-%m-%d")
            except ValueError:
                raise calendarErrors.Error400("Repeating dict key(s) is/are invalid type or format.")


    def toDict(self):
        """
        Convert CalendarEvent object to dictionary.

        Returns
            dict : {str: <value>}
                A dictionary of the fields in the CalendarEvent object.
        """
        outputDict = {}

        # Insert all required fields into dictionary
        # If addEvent is True, required fields are eventType, name, dates
        # If addEvent is False, required field is eventId
        outputDict = self.toDictHelper(outputDict, "eventType", self.eventType, str, not self.addEvent)
        outputDict = self.toDictHelper(outputDict, "name", self.name, str, not self.addEvent)
        outputDict = self.toDictHelper(outputDict, "dates", self.dates, dict, not self.addEvent)
        outputDict = self.toDictHelper(outputDict, "eventId", self.eventId, str, self.addEvent)

        # For all other attributes, insert into dictionary only if not None or empty
        outputDict = self.toDictHelper(outputDict, "userIds", self.userIds, list)
        outputDict = self.toDictHelper(outputDict, "times", self.times, dict)
        outputDict = self.toDictHelper(outputDict, "location", self.location, str)
        outputDict = self.toDictHelper(outputDict, "repeating", self.repeating, dict)

        return outputDict

    def toDictHelper(self, outputDict, field, fieldVal, dataType, emptyAllowed=True):
        """
        Inserts field into dictionary if nonempty.

        Parameters
            outputDict : dict
                The output dictionary of the toDict function.
            field : str
                A string representing a key in the output dict.
            fieldVal
                The value of the field.
            dataType : type
                The expected type of the field's value.
            emptyAllowed : bool
                A boolean representing whether the dict value can be nonempty.

        Returns
            outputDict : dict
        """
        print(field, fieldVal)
        # If fieldVal is empty and field is required, raise exception
        # Otherwise add field to outputDict
        empty = ""
        if dataType == list:
            empty = []
        elif dataType == dict:
            empty = {}

        if type(fieldVal) != dataType:
            raise calendarErrors.Error400("Field has invalid data type")
        elif fieldVal != empty:
            outputDict[field] = fieldVal
        elif not emptyAllowed:
            raise calendarErrors.Error400("Required field is empty")
            
        return outputDict


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