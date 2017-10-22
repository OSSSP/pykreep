class InvalidCommandArgumentError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ConnectionTerminatedError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ParameterError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ModuleError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ExploitFailed(Exception):
    def __init__(self, message):
        super().__init__(message)