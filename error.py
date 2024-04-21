class Error():
    """A class to store error messages and line numbers"""
    def __init__(self, type, message = ""):
        self.type = type
        self.message = message
    def __str__(self):
        return f"{self.type}: {self.message}"
    @property
    def message(self):
        return self._message
    @message.setter
    def message(self, message):
        self._message = message
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, type):
        self._type = type