import copy

import calendarErrors

class CalendarUtils:
    """ Utility functions for calendar service. """

    @staticmethod
    def checkFieldInJson(json, field, fieldName, dataType, emptyAllowed=False):
        """
        Checks validity of field in json and returns field if valid, otherwise raises error 400.

        Parameters
            json : {str: <value>}
                A dictionary representing data from the JSON object.
            field : str
                A string representing a key in the json.
            fieldName : str
                A string representing the key to be inserted into error messages.
            dataType : type
                The expected type of the field's value.
            emptyAllowed: bool
                A boolean representing whether the dict value can be nonempty.
        """
        # Checks if field is a key in json dict and dict value is nonempty (if empty not allowed)
        # Checks if dict value is correct data type
        empty = ""
        if dataType == list:
            empty = []
        elif dataType == dict:
            empty = {}

        if emptyAllowed and field not in json:
            return empty
        elif not emptyAllowed and (field not in json or json[field] == empty):
            raise calendarErrors.Error400(fieldName + " was not provided")
        elif type(json[field]) != dataType:
            raise calendarErrors.Error400(fieldName + " is invalid type: " + str(type(json[field])))
        elif dataType == dict:
            return copy.deepcopy(json[field])
        else:
            return json[field]