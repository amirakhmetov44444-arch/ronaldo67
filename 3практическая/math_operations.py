def divide_numbers(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Оба аргумента должны быть числового типа (int или float)")
    
    if b == 0:
        raise ZeroDivisionError("Деление на ноль категорически запрещено")
        
    return float(a / b)


def safe_divide_elements(list_a, list_b):
    if not isinstance(list_a, list) or not isinstance(list_b, list):
        raise TypeError("Передаваемые аргументы должны являться списками")
        
    if len(list_a) != len(list_b):
        raise ValueError("Списки должны обладать одинаковой длиной")
        
    results = []
    for elem_a, elem_b in zip(list_a, list_b):
        results.append(divide_numbers(elem_a, elem_b))

    return results