from abc import ABC, abstractmethod
from src.exceptions import InvalidValueError, EmptyConnectionError


class CircuitElement(ABC):
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise InvalidValueError("nazwa elementu nie moze byc pusta")
        self._name = name.strip()
        self._voltage = 0.0
        self._current = 0.0

    @property
    def name(self) -> str:
        return self._name

    @property
    def voltage(self) -> float:
        return self._voltage

    @property
    def current(self) -> float:
        return self._current

    def _set_electrical_state(self, voltage: float, current: float) -> None:
        if voltage < 0 or current < 0:
            raise InvalidValueError("napiecie i prad nie moga byc ujemne")
        self._voltage = float(voltage)
        self._current = float(current)

    @abstractmethod
    def get_resistance(self) -> float:
        pass

    @abstractmethod
    def update_state(self, voltage: float, current: float) -> None:
        pass

    @abstractmethod
    def get_all_resistors(self) -> list:
        pass


class Resistor(CircuitElement):
    def __init__(self, name: str, resistance: float):
        super().__init__(name)
        if not isinstance(resistance, (int, float)) or resistance <= 0:
            raise InvalidValueError("rezystancja musi byc dodatnia")
        self._resistance = float(resistance)

    def get_resistance(self) -> float:
        return self._resistance

    def update_state(self, voltage: float, current: float) -> None:
        self._set_electrical_state(voltage, current)

    def get_all_resistors(self) -> list:
        return [self]