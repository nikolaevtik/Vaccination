# tests/test_calculator.py
import pytest
# 1. Импортируем нашу функцию из папки src
from app.src.calculator import add, divide

# 2. Пишем тестовую функцию, соблюдая правило именования
@pytest.mark.smoke
def test_add():
    # 3. Используем assert для проверки
    assert add(2, 3) == 5

@pytest.mark.regression
def test_divide():
    assert divide(10, 2) == 5
        
# def test_add_with_wrong_expectation():
#     """Этот тест специально написан так, чтобы провалиться."""
#     # Вызываем функцию прямо внутри assert, чтобы увидеть детализацию ошибки
#     assert add(2, 2) == 5    
    
def test_add_raises_type_error_on_string_input():
    with pytest.raises(TypeError):
        add(5, "hello")    
        
@pytest.mark.regression
def test_divide_by_zero_raises_value_error_with_message():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    assert "Нельзя делить на ноль" in str(excinfo.value)    
    
@pytest.mark.slow
def test_very_slow_calculation():
    """Гипотетический тест, который работает очень долго."""
    # для примера просто сделаем его успешным
    assert True    