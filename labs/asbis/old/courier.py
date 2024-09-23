"""Модуль для отправки данных по сети"""
import socket
import struct
import sched
import time


def send_data(sck, addr, data: list):
    """Метод для отправки одного сообщения"""

    # проверка на содержание массива
    if len(data) != 7:
        raise ValueError('Неверный формат массива отправляемых данных, неверное число отправленных данных')

    for item in data:
        if not (isinstance(item, float) or isinstance(item, int)):
            raise ValueError('Неверный формат массива отправляемых данных')

    data = struct.pack("!ddddddd", *data)  # *data это *arg с содержанием массива
    sck.sendto(data, addr)


def send_stream(addr, data: list):
    """Метод для непрерывной передачи данных"""

    sck = socket.socket(type=socket.SOCK_DGRAM)  # SOCK_DGRAM ~ протокол UDP
    stream = sched.scheduler(time.time, time.sleep)

    while True:
        stream.enter(0.1, 1, send_data, (sck, addr, data))
        stream.run()


def main():
    """Основной исполняющий метод"""

    # lat long alt vel pitch roll heading
    data = [12, 34, 56, 78, 90, 12, 34]  # заполнением этого массива можно изменить параметры к отправке
    addr = ('127.0.0.1', 12346)  # изменение адреса отправки сообщения

    send_stream(addr, data)


if __name__ == '__main__':
    main()
