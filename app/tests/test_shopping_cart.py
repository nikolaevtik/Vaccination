# tests/test_shopping_cart.py
import pytest

# Вспомогательный класс для нашего примера
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, price):
        self.items[item_name] = price
    
    def get_total_price(self):
        return sum(self.items.values())

# 1. Создаем фикстуру
@pytest.fixture
def filled_cart():
    """Создает и возвращает корзину с двумя товарами."""
    # 2. Здесь находится наш код ПОДГОТОВКИ (Setup)
    cart = ShoppingCart()
    cart.add_item("apple", price=10)
    cart.add_item("banana", price=20)
    # 3. Возвращаем подготовленный объект
    return cart

# 4. Пишем тест, который ЗАПРАШИВАЕТ фикстуру
def test_add_item(filled_cart):
    # `filled_cart` здесь - это тот самый объект `cart`, 
    # который вернула наша фикстура
    filled_cart.add_item("cherry", price=30)
    assert "cherry" in filled_cart.items

def test_get_total_price(filled_cart):
    # Мы можем использовать ту же самую фикстуру в другом тесте!
    assert filled_cart.get_total_price() == 30