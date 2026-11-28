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


class CompositeConnection(CircuitElement):
    def __init__(self, name: str, elements: list = None):
        super().__init__(name)
        self._elements = []
        if elements:
            for element in elements:
                self.add_element(element)

    @property
    def elements(self) -> list:
        return list(self._elements)

    def add_element(self, element: CircuitElement) -> None:
        if not isinstance(element, CircuitElement):
            raise InvalidValueError("element musi dziedziczyc po CircuitElement")
        self._elements.append(element)

    def _validate_not_empty(self) -> None:
        if not self._elements:
            raise EmptyConnectionError(f"polaczenie {self._name} jest puste")

    def get_all_resistors(self) -> list:
        resistors = []
        for element in self._elements:
            resistors.extend(element.get_all_resistors())
        return resistors


class SeriesConnection(CompositeConnection):
    def get_resistance(self) -> float:
        self._validate_not_empty()
        total_resistance = 0.0
        for element in self._elements:
            total_resistance += element.get_resistance()
        return total_resistance

    def update_state(self, voltage: float, current: float) -> None:
        self._validate_not_empty()
        self._set_electrical_state(voltage, current)
        for element in self._elements:
            element_voltage = current * element.get_resistance()
            element.update_state(element_voltage, current)


class ParallelConnection(CompositeConnection):
    def get_resistance(self) -> float:
        self._validate_not_empty()
        conductance_sum = 0.0
        for element in self._elements:
            conductance_sum += 1.0/element.get_resistance()
        return 1.0 / conductance_sum

    def update_state(self, voltage: float, current: float) -> None:
        self._validate_not_empty()
        self._set_electrical_state(voltage, current)

        for element in self._elements:
            element_current = voltage/element.get_resistance()
            element.update_state(voltage, element_current)