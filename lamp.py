"""
Модуль имитации работы лампы.
Лампа раз в некоторое время отправляет запросы на облако и относительно полученных данных
регулирует значения освещения и теплоты освещения.
"""

import time

from cloud import get_current_lighting
from cloud import get_reference_lighting
from cloud import get_current_warmth
from cloud import get_reference_warmth
from cloud import send_current_lighting
from cloud import send_current_warmth


TIME_TO_REFRESH = 5  # время на обновление запросов


def regulate_lighting(current_lighting, reference_lighting):
    """
    Функция имитации регуляции освещения. При каждой регуляции выводится сообщение в консоль
    """
    print('--regulate lighting. current: {}, reference: {}---'.format(current_lighting, reference_lighting))


def regulate_warmth(current_warmth, reference_warmth):
    """
    Функция имитации регуляции теплоты освещения. При каждой регуляции выводится сообщение в консоль
    """
    print('--regulate warmth of lighting. current: {}, reference: {}---'.format(current_warmth, reference_warmth))


while True:
    time.sleep(TIME_TO_REFRESH)
    current_lighting = get_current_lighting()
    reference_lighting = get_reference_lighting()
    current_warmth = get_current_warmth()
    reference_warmth = get_reference_warmth()

    regulate_lighting(current_lighting, reference_lighting)
    regulate_warmth(current_warmth, reference_warmth)

    send_current_lighting(reference_lighting)
    send_current_warmth(reference_warmth)
