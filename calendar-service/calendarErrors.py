""" Defines custom Python exceptions """

class Error(Exception):
    """ Base class for other exceptions """
    pass


class Error400(Error):
    """ Raised for Bad Request error """
    def __init__(self, message=""):
        self.message = "Bad Request: " + message
        super().__init__(self.message)


class Error401(Error):
    """ Raised for Unauthorized error """
    def __init__(self, message=""):
        self.message = "Unauthorized: " + message
        super().__init__(self.message)


class Error404(Error):
    """ Raised for Not Found error """
    def __init__(self, message=""):
        self.message = "Not Found: " + message
        super().__init__(self.message)