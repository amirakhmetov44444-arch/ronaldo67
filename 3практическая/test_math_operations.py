import pytest
from math_operations import divide_numbers, safe_divide_elements

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (5, 2, 2.5),
    (1.5, 0.5, 3.0),
    (-12, 3, -4.0),   
    (0, 5, 0.0)
])
def test_divide_numbers_positive(a, b, expected):
    assert divide_numbers(a, b) == expected

def test_divide_by_zero_exception():
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

def test_divide_numbers_type_error_string():
    with pytest.raises(TypeError):
        divide_numbers("10", 2)

def test_divide_numbers_type_error_list():
    with pytest.raises(TypeError):
        divide_numbers(10, [2])

def test_divide_numbers_boundary():
    assert divide_numbers(1e-308, 10) == 1e-309

def test_safe_divide_elements_success():
    assert safe_divide_elements([8, 6], [2, 3]) == [4.0, 2.0]

def test_safe_divide_elements_zero_exception():
    with pytest.raises(ZeroDivisionError):
        safe_divide_elements([4, 9], [2, 0])

def test_safe_divide_elements_type_error():
    with pytest.raises(TypeError):
        safe_divide_elements([4, "six"], [2, 3])

def test_safe_divide_elements_length_mismatch():
    with pytest.raises(ValueError):
        safe_divide_elements([4, 5], [2])

def test_safe_divide_elements_empty():
    assert safe_divide_elements([], []) == []