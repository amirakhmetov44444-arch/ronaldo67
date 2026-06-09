import pytest

def calculate_expression(expression):
    return eval(expression)

def test_addition_tc01():
    assert calculate_expression("15+25") == 40

def test_float_multiplication_tc03():
    assert calculate_expression("5.5*2") == 11.0

def test_empty_input_tc04():
    assert calculate_expression("0") == 0

def test_division_by_zero_tc02():

    with pytest.raises(ZeroDivisionError):
        calculate_expression("10/0")