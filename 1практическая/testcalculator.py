import pytest
# Импортируем функцию вычислений из нашего основного файла калькулятора
from calculator import calculate_expression

def test_addition_tc01():
    """Тест-кейс TC-01: Проверка базового сложения целых чисел"""
    assert calculate_expression("15+25") == 40


def test_float_multiplication_tc03():
    """Тест-кейс TC-03: Проверка умножения дробных чисел"""
    assert calculate_expression("5.5*2") == 11.0


def test_division_by_zero_tc02():
    """
    Тест-кейс TC-02 (Негативный): Проверка реакции на деление на ноль.
    Мы ожидаем, что калькулятор упадет с ошибкой ZeroDivisionError.
    Если ошибка вылетает — PyTest считает, что этот автотест пройден успешно,
    так как дефект зафиксирован.
    """
    with pytest.raises(ZeroDivisionError):
        calculate_expression("10/0")