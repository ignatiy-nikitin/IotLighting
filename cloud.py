"""
Модуль взаимодействия с IoT облаком.
"""

import requests

from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo


HOST = 'demo.thingsboard.io'
HTTP_TELEMETRY_URL = 'http://demo.thingsboard.io/api/plugins/telemetry/DEVICE/{}/values/timeseries'

LIGHTING_DEVICE_TOKEN = '941XbBZH5qpm19dOsOwY'
LIGHTING_DEVICE_ID = '256ff3f0-43ce-11eb-8cad-3d8873d86e51'

CURRENT_LIGHTING = 'current_lighting'
REFERENCE_LIGHTING = 'reference_lighting'
CURRENT_WARMTH = 'current_warmth'
REFERENCE_WARMTH = 'reference_warmth'

TOKEN = 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ2bGFkX3pnQGJrLnJ1Iiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJ1c2VySWQiOiJmNWI2NzEzMC00M2I4LTExZWItOGNhZC0zZDg4NzNkODZlNTEiLCJmaXJzdE5hbWUiOiJWbGFkaXNsYXYiLCJsYXN0TmFtZSI6IlphbWFldiIsImVuYWJsZWQiOnRydWUsInByaXZhY3lQb2xpY3lBY2NlcHRlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6ImY0YmEwZmQwLTQzYjgtMTFlYi04Y2FkLTNkODg3M2Q4NmU1MSIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAiLCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTYwODU4NDIyMCwiZXhwIjoxNjEwMzg0MjIwfQ.i_UowYR8k3aKYC01y1g5wWJSipaGNjuCZV118bCWo66_MaiS8WJmsrlD378wUyz5N4joEq7VV1fFO7_g0MvBFw'


def _send(token, data):
    """
    Отправка словаря с данными на облако по MQTT
    :param data: Данные - dict
    :retun: None
    """
    client = TBDeviceMqttClient(HOST, token)
    client.connect()
    result = client.send_telemetry(data)
    success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
    client.disconnect()


def _get_telemetry(device_id, telemetry_name):
    """
    Получение телеметрии с облака по HTTP
    :param device_id: ID девайса - str
    :param telemetry_name: Наименование телеметрии - str
    :return: json
    """
    return requests.get(
        url=HTTP_TELEMETRY_URL.format(device_id),
        headers={'X-Authorization': TOKEN},
    ).json()[telemetry_name][0]['value']


def send_current_lighting(value):
    """
    Отправка текущего освещения. Измеряется в люксах
    :param value: Значение освещения - int
    :return: None
    """
    _send(LIGHTING_DEVICE_TOKEN, {CURRENT_LIGHTING: value})


def send_reference_lighting(value):
    """
    Отправка рекомендованного освещения. Измеряется в люксах
    :param value: Значение освещения - int
    :return: None
    """
    _send(LIGHTING_DEVICE_TOKEN, {REFERENCE_LIGHTING: value})


def send_current_warmth(value):
    """
    Отправка текущей теплоты освещения. Градация от 0% (холодное) до 100% (теплое)
    :param value: Теплота освещения - int
    :return: None
    """
    _send(LIGHTING_DEVICE_TOKEN, {CURRENT_WARMTH: value})


def send_reference_warmth(value):
    """
    Отправка рекомендованной теплоты освещения. Градация от 0% (холодное) до 100% (теплое)
    :param value: Теплота освещения - int
    :return: None
    """
    _send(LIGHTING_DEVICE_TOKEN, {REFERENCE_WARMTH: value})


def get_current_lighting():
    """
    Получение текущего значения освещения
    :param: None
    :return: int
    """
    return _get_telemetry(LIGHTING_DEVICE_ID, CURRENT_LIGHTING)


def get_reference_lighting():
    """
    Получение рекомендуемого значения освещения
    :param: None
    :return: int
    """
    return _get_telemetry(LIGHTING_DEVICE_ID, REFERENCE_LIGHTING)


def get_current_warmth():
    """
    Получение текущего значения теплоты
    :param: None
    :return: int
    """
    return _get_telemetry(LIGHTING_DEVICE_ID, CURRENT_WARMTH)


def get_reference_warmth():
    """
    Получение рекомендованного значения теплоты
    :param: None
    :return: int
    """
    return _get_telemetry(LIGHTING_DEVICE_ID, REFERENCE_WARMTH)
