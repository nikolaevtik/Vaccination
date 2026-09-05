import inspect
import sys
from datetime import datetime
from typing import List, Optional

# ========== ПРИМЕР 1: ИССЛЕДУЕМ ФУНКЦИЮ ==========
print("=" * 60)
print("ПРИМЕР 1: Информация о функции")
print("=" * 60)


def example_function(a: int, b: str = "hello", *args, **kwargs) -> List[str]:
    """
    Это пример функции с докстрингом.
    Она возвращает список строк.
    """
    return [str(a), b, *args]


# Получаем сигнатуру функции
sig = inspect.signature(example_function)
print(f"Сигнатура: {sig}")
print(f"Параметры: {list(sig.parameters.keys())}")

# Детально по каждому параметру
for name, param in sig.parameters.items():
    print(f"  {name}: {param.kind} -> default={param.default}")

# Докстринг
print(f"Докстринг: {inspect.getdoc(example_function)}")
print(f"Исходный код:\n{inspect.getsource(example_function)}")
print(
    f"Файл и строка: {inspect.getfile(example_function)} строка {inspect.getsourcelines(example_function)[1]}"
)


# ========== ПРИМЕР 2: ИССЛЕДУЕМ КЛАСС ==========
print("\n" + "=" * 60)
print("ПРИМЕР 2: Информация о классе")
print("=" * 60)


class User:
    """Класс пользователя"""

    default_role = "guest"

    def __init__(self, name: str, age: int = 18):
        self.name = name
        self.age = age

    def greet(self) -> str:
        """Приветствие"""
        return f"Hello, {self.name}"

    @property
    def is_adult(self) -> bool:
        return self.age >= 18

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["name"], data["age"])


# Все методы класса
print(f"Методы класса: {inspect.getmembers(User, inspect.ismethod)}")
print(f"Функции класса: {inspect.getmembers(User, inspect.isfunction)}")

# Проверка типа
print(f"isclass: {inspect.isclass(User)}")
print(f"isroutine: {inspect.isroutine(User.greet)}")  # True для методов/функций

# Дерево наследования
print(f"Наследование: {inspect.getmro(User)}")

# Аннотации
print(f"Аннотации __init__: {inspect.get_annotations(User.__init__)}")


# ========== ПРИМЕР 3: УЗНАЁМ, КТО НАС ВЫЗВАЛ ==========
print("\n" + "=" * 60)
print("ПРИМЕР 3: Стек вызовов (кто вызвал функцию)")
print("=" * 60)


def get_caller_info():
    """Возвращает информацию о том, кто вызвал эту функцию"""
    # Текущий фрейм
    frame = inspect.currentframe()
    print(
        f"Текущий файл: {inspect.getframeinfo(frame).filename}, строка {inspect.getframeinfo(frame).lineno}"
    )

    # Фрейм вызывающего
    caller_frame = frame.f_back
    if caller_frame:
        info = inspect.getframeinfo(caller_frame)
        print(
            f"Вызвано из: {info.filename}, функция {info.function}, строка {info.lineno}"
        )
        print(f"Локальные переменные вызывающего: {caller_frame.f_locals}")

    return "OK"


def wrapper_function():
    """Функция-обёртка, которая вызывает get_caller_info"""
    x = 42
    y = "test"
    result = get_caller_info()
    print(f"Результат: {result}")


wrapper_function()


# ========== ПРИМЕР 4: ПРОВЕРКА ТИПОВ ОБЪЕКТОВ ==========
print("\n" + "=" * 60)
print("ПРИМЕР 4: Проверка типов объектов")
print("=" * 60)


class MyClass:
    pass


obj = MyClass()
func = lambda x: x * 2

print(f"isbuiltin(str): {inspect.isbuiltin(str)}")  # встроенные функции/методы
print(f"isroutine(lambda): {inspect.isroutine(func)}")  # функция/метод/лямбда
print(f"ismodule(sys): {inspect.ismodule(sys)}")
print(f"isclass(MyClass): {inspect.isclass(MyClass)}")
print(f"ismethod(obj.__init__): {inspect.ismethod(obj.__init__)}")
print(f"isfunction(lambda): {inspect.isfunction(func)}")
print(f"iscode(example_function.__code__): {inspect.iscode(example_function.__code__)}")


# ========== ПРИМЕР 5: АРГУМЕНТЫ ФУНКЦИИ ==========
print("\n" + "=" * 60)
print("ПРИМЕР 5: Получение аргументов функции")
print("=" * 60)


def complex_func(a, b=10, *args, c=20, **kwargs):
    pass


# Получаем аргументы
args_spec = inspect.getfullargspec(complex_func)
print(f"args: {args_spec.args}")
print(f"defaults: {args_spec.defaults}")
print(f"varargs: {args_spec.varargs}")  # *args
print(f"varkw: {args_spec.varkw}")  # **kwargs
print(f"kwonlyargs: {args_spec.kwonlyargs}")  # аргументы после *
print(f"kwonlydefaults: {args_spec.kwonlydefaults}")  # c=20


# ========== ПРИМЕР 6: КЛАССЫ С ДАТА-КЛАССАМИ ==========
print("\n" + "=" * 60)
print("ПРИМЕР 6: Исследование дата-класса")
print("=" * 60)

from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int = 0
    email: Optional[str] = None


# Все поля с их типами и значениями по умолчанию
print(f"Поля: {inspect.get_annotations(Person)}")

# Проверяем, что это дата-класс
print(f"isclass: {inspect.isclass(Person)}")

# Все члены класса
members = inspect.getmembers(Person)
for name, value in members[:5]:  # Покажем первые 5 для краткости
    print(f"  {name}: {type(value).__name__}")


# ========== ПРИМЕР 7: ПОЛУЧЕНИЕ ДОКУМЕНТАЦИИ ==========
print("\n" + "=" * 60)
print("ПРИМЕР 7: Получение документации")
print("=" * 60)


def test_doc(a, b):
    """Складывает a и b.

    Аргументы:
        a: первое число
        b: второе число

    Возвращает:
        сумму a и b
    """
    return a + b


print(f"Докстринг: {inspect.getdoc(test_doc)}")
print(f"Комментарии: {inspect.getcomments(test_doc)}")  # Комментарии перед функцией
print(f"Исходник:\n{inspect.cleandoc(inspect.getdoc(test_doc))}")  # Очищенный докстринг


# ========== ПРИМЕР 8: ИНТРОСПЕКЦИЯ ТЕКУЩЕГО МОДУЛЯ ==========
print("\n" + "=" * 60)
print("ПРИМЕР 8: Информация о текущем модуле")
print("=" * 60)

current_module = inspect.getmodule(example_function)
print(f"Имя модуля: {current_module.__name__}")
print(f"Файл модуля: {current_module.__file__}")

# Все функции в текущем модуле
functions = inspect.getmembers(current_module, inspect.isfunction)
print(f"Функции в модуле: {[f[0] for f in functions if not f[0].startswith('_')]}")

print("\n" + "=" * 60)
print("Все примеры выполнены!")
print("=" * 60)
