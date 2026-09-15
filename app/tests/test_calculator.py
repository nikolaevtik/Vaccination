# tests/test_calculator.py

# 1. Импортируем нашу функцию из папки src
from app.src.calculator import add

# 2. Пишем тестовую функцию, соблюдая правило именования
def test_add():
    # 3. Используем assert для проверки
    assert add(2, 3) == 5