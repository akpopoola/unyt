"""Test Matplotlib ConversionInterface"""
from pytest import raises
from unyt._on_demand_imports import _matplotlib, NotAModule
from unyt import s, K
from unyt.exceptions import UnitConversionError


def test_label():
    if isinstance(_matplotlib.pyplot, NotAModule):
        return
    plt = _matplotlib.pyplot
    x = [0, 1, 2] * s
    y = [3, 4, 5] * K
    _, ax = plt.subplots()
    ax.plot(x, y)
    expected_xlabel = "$\\left(\\rm{s}\\right)$"
    assert ax.xaxis.get_label().get_text() == expected_xlabel
    expected_ylabel = "$\\left(\\rm{K}\\right)$"
    assert ax.yaxis.get_label().get_text() == expected_ylabel


def test_convert_unit():
    if isinstance(_matplotlib.pyplot, NotAModule):
        return
    plt = _matplotlib.pyplot
    x = [0, 1, 2] * s
    y = [1000, 2000, 3000] * K
    _, ax = plt.subplots()
    ax.plot(x, y, yunits="Celcius")
    expected = y.to("Celcius")
    line = ax.lines[0]
    original_y_array = line.get_data()[1]
    converted_y_array = line.convert_yunits(original_y_array)
    results = converted_y_array == expected
    assert results.all()


def test_convert_equivalency():
    if isinstance(_matplotlib.pyplot, NotAModule):
        return
    plt = _matplotlib.pyplot
    x = [0, 1, 2] * s
    y = [1000, 2000, 3000] * K
    _, ax = plt.subplots()
    ax.plot(x, y, yunits=("J", "thermal"))
    expected = y.to("J", "thermal")
    line = ax.lines[0]
    original_y_array = line.get_data()[1]
    converted_y_array = line.convert_yunits(original_y_array)
    results = converted_y_array == expected
    assert results.all()


def test_dimensionless():
    if isinstance(_matplotlib.pyplot, NotAModule):
        return
    plt = _matplotlib.pyplot
    x = [0, 1, 2] * s
    y = [3, 4, 5] * K / K
    ax = plt.figure().add_subplot()
    ax.plot(x, y)
    expected_ylabel = ""
    assert ax.yaxis.get_label().get_text() == expected_ylabel


def test_conversionerror():
    if isinstance(_matplotlib.pyplot, NotAModule):
        return
    plt = _matplotlib.pyplot
    x = [0, 1, 2] * s
    y = [3, 4, 5] * K
    ax = plt.figure().add_subplot()
    ax.plot(x, y)
    ax.xaxis.callbacks.exception_handler = None
    with raises((_matplotlib.units.ConversionError, UnitConversionError)):
        ax.xaxis.set_units("V")
