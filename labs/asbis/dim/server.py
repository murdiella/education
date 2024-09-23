import socket
from ctypes import *
import pickle
import tkinter as tk
from matplotlib import pyplot as plt

SERVER_ADDR = ('127.0.0.1', 12346)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SERVER_ADDR)

class BNR(Structure):
    _fields_ = [
        ('field1', c_int),
        ('field2', c_float)
    ]

class Time(Structure):
    _fields_ = [
        ('hours', c_int),
        ('minutes', c_int),
        ('seconds', c_int)
    ]

class Date(Structure):
    _fields_ = [
        ('day', c_int),
        ('month', c_int),
        ('year', c_int)
    ]

class SRNS(Structure):
    _fields_ = [
        ('field1', c_int),
        ('field2', c_float)
    ]

class INS(Structure):
    _fields_ = [
        ('roll', c_float),
        ('pitch', c_float),
        ('yaw', c_float)
    ]

class SNS(Structure):
    _fields_ = [
        ('hour', Time),
        ('date', Date),
        ('cur_lat', c_double),
        ('cur_long', c_double),
        ('speed', c_float),
        ('braking', c_bool),
        ('raining', c_bool),
        ('ins', INS),
        ('srns', SRNS),
        ('bnr', BNR)
    ]

def unpack(ctype, buf):
    cstring = create_string_buffer(buf)
    ctype_instance = cast(pointer(cstring), POINTER(ctype)).contents
    return ctype_instance

# Функция для декодирования полученных данных
def decode(value, n_bit, h_price):
    return h_price * value / 2 ** (n_bit - 1)

def show_data():
    data, addr = sock.recvfrom(10240)
    if len(data) == sizeof(SNS):
        received_sns = unpack(SNS, data)
        decoded_lat = decode(received_sns.cur_lat, 20, 90)
        decoded_long = decode(received_sns.cur_long, 20, 180)
        result_label.config(text=f"Декодированные координаты: Широта: {decoded_lat}, Долгота: {decoded_long}")
        decoded_speed = decode(received_sns.speed, 16, 200)
        result_label2.config(text=f"Декодированная скорость: {decoded_speed} км/ч")
        result_label3.config(text=f"Состояние торможения: {'Включено' if received_sns.braking else 'Выключено'}")
        result_label4.config(text=f"Дождь: {'Да' if received_sns.raining else 'Нет'}")
        decoded_roll = received_sns.ins.roll
        decoded_pitch = received_sns.ins.pitch
        decoded_yaw = received_sns.ins.yaw
        result_label5.config(text=f"Декодированные данные INS: Roll: {decoded_roll}, Pitch: {decoded_pitch}, Yaw: {decoded_yaw}")

def show_graph():
    received_data, addr = sock.recvfrom(10240)
    if received_data:
        received_data = pickle.loads(received_data)

        latitude = received_data['latitude']
        longitude = received_data['longitude']
        east_speed = received_data['east_speed']
        north_speed = received_data['north_speed']

        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.plot(latitude, 'r-', label='Latitude')
        plt.title('Географическая широта')

        plt.subplot(2, 2, 2)
        plt.plot(longitude, 'b-', label='Longitude')
        plt.title('Географическая долгота')

        plt.subplot(2, 2, 3)
        plt.plot(east_speed, 'g-', label='East Speed')
        plt.title('Восточная проекция скорости')

        plt.subplot(2, 2, 4)
        plt.plot(north_speed, 'm-', label='North Speed')
        plt.title('Северная проекция скорости')

        plt.tight_layout()
        plt.show()

root = tk.Tk()
root.title("INS")

result_label = tk.Label(root)
result_label.pack()

result_label2 = tk.Label(root)
result_label2.pack()

result_label3 = tk.Label(root)
result_label3.pack()

result_label4 = tk.Label(root)
result_label4.pack()

result_label5 = tk.Label(root)
result_label5.pack()

btn_show_data = tk.Button(root, text="Отобразить данные", command=show_data)
btn_show_data.pack()

btn_show_graph = tk.Button(root, text="Показать график эволюции", command=show_graph)
btn_show_graph.pack()

root.mainloop()

sock.close()

