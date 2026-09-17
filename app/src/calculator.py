# src/calculator.py


def add(a, b):
    """
    Эта функция принимает два числа и возвращает их сумму.
    """
    return a + b

def divide(a, b):
    """
    Эта функция делит a на b.
    Вызывает ValueError при делении на ноль.
    """
    if b == 0:
        raise ValueError("Нельзя делить на ноль")
    return a / b

# import inspect
# source = inspect.getsource(add)
# print(source)


