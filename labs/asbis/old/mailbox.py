"""Модуль для принятия данных из сети"""

import socket
import struct
from keyboard import add_hotkey, is_pressed

window_open = True  # логическая переменная для определения времени работы


def receive():
    """Метод для открытия канала приема"""

    sck = socket.socket(type=socket.SOCK_DGRAM)  # SOCK_DGRAM ~ протокол UDP
    sck.bind(('127.0.0.1', 12346))

    def close_window():
        global window_open
        window_open = False

    add_hotkey('q', lambda: close_window())  # выйти из бесконечного цикла по нажатию Q в будущем

    global window_open
    while window_open:
        data, addr = sck.recvfrom(56)  # 7 значений по 8 бит (float'ы)
        # !ddddddd это буквально 7 float значений
        lat, long, alt, vel, pitch, roll, heading = struct.unpack("!ddddddd", data)
        print(f'\nGot following parameters:\nlatitude = {round(lat, 3)};\nlongitude = {round(long, 3)};\naltitude = '
              f'{round(alt, 3)};\nvelocity = {round(vel, 3)};\npitch = {round(pitch, 3)};\nroll = '
              f'{round(roll, 3)};\nheading = {round(heading, 3)}')

    print(f'Socket channel closed')


def main():
    """Основной исполняющий метод"""

    receive()


if __name__ == '__main__':
    main()
