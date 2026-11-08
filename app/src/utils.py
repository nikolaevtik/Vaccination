# src/utils.py
import random
import external_logger
import requests

def get_random_number():
    return random.randint(1, 100)


def get_data():
    response = requests.get("http://example.com")
    response.raise_for_status()
    return response.json()



def log_message(message):
    # Эта функция ничего не возвращает, только вызывает другую
    external_logger.send(message)