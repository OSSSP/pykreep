class InvalidCommandArgument(Exception):
    def __init__(self, message):
        super().__init__(message)


class ConnectionTerminated(Exception):
    def __init__(self, message):
        super().__init__(message)