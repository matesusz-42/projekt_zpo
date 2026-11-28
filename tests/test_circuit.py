import pytest
from src.elements import Resistor, SeriesConnection, ParallelConnection
from src.exceptions import InvalidValueError, EmptyConnectionError



def test_resistor_valid_creation():
    r = Resistor("R1", 10.0)
    assert r.name == "R1"
    assert r.get_resistance() == 10.0
    assert r.voltage == 0
    assert r.current == 0


def test_resistor_invalid_values():
    with pytest.raises(InvalidValueError):
        Resistor("", 10.0)
    with pytest.raises(InvalidValueError):
        Resistor("R1", 0.0)
    with pytest.raises(InvalidValueError):
        Resistor("R1", -5.0)


def test_series_connection_resistance_and_state():
    r1 = Resistor("R1", 4.0)
    r2 = Resistor("R2", 6.0)

    series = SeriesConnection("S1", [r1, r2])

    assert series.get_resistance() == pytest.approx(10.0)

    series.update_state(20.0,2.0)

    assert r1.current == pytest.approx(2.0)
    assert r2.current == pytest.approx(2.0)
    assert r1.voltage == pytest.approx(8.0)
    assert r2.voltage == pytest.approx(12.0)


def test_parallel_connection_resistance_and_state():
    r1 = Resistor("R1", 6.0)
    r2 = Resistor("R2", 3.0)
    parallel = ParallelConnection("P1", [r1,r2])
    assert parallel.get_resistance() == pytest.approx(2.0)
    parallel.update_state(6.0, 3.0)

    assert r1.voltage == pytest.approx(6.0)
    assert r2.voltage == pytest.approx(6.0)
    assert r1.current == pytest.approx(1.0)
    assert r2.current == pytest.approx(2.0)


def test_empty_connections_raise_error():
    empty_series = SeriesConnection("S_empty")

    empty_parallel = SeriesConnection("P_empty")

    with pytest.raises(EmptyConnectionError):
        empty_series.get_resistance()
    with pytest.raises(EmptyConnectionError):
        empty_parallel.get_resistance()