class CircuitError(Exception):
    pass
class InvalidValueError(CircuitError):
    pass
class EmptyConnectionError(CircuitError):
    pass
class CircuitFileError(CircuitError):
    pass