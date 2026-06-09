import pytest
from calculator import add, subtract, multiply, divide

def test_add_positive():
    assert add(5, 3) == 8

def test_add_zero():
    assert add(7, 0) == 7

def test_add_negative():
    assert add(-4, -6) == -10

def test_subtract_positive_result():
    assert subtract(10, 3) == 7

def test_subtract_negative_result():
    assert subtract(3, 10) == -7

def test_multiply_two_numbers():
    assert multiply(6, 7) == 42

def test_multiply_by_zero():
    assert multiply(999, 0) == 0

def test_divide_exact():
    assert divide(20, 4) == 5

def test_divide_float_result():
    result = divide(10, 3)
    assert abs(result - 3.3333) < 0.001

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

def test_large_numbers():
    assert add(999999999, 1) == 1000000000