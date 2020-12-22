"""
Модуль генерации освещения с датчиков
"""
import random
import time

from cloud import send_current_lighting


def generate_lighting():
    return random.uniform(20, 30)


while True:
    time.sleep(2)
    lighting = generate_lighting()
    send_current_lighting(lighting)
