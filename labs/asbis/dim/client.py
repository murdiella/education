import socket
from ctypes import *
import numpy as np
import pickle

SERVER_ADDR = ('127.0.0.1', 12346)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Моделируем данные самолета
initial_latitude = 40.7128
initial_longitude = -74.0060
initial_speed_east = 250
initial_speed_north = 50
delta_t = 1
num_steps = 100

latitude = [initial_latitude]
longitude = [initial_longitude]
east_projection_speed = [initial_speed_east]
north_projection_speed = [initial_speed_north]

class ErrorSNS:

    def __init__(self):
        pass


class ErrorNKA(ErrorSNS):

    def __init__(self):
        self.error_value = np.random.normal(0, 0.08)

class ErrorION(ErrorSNS):

    def __init__(self):
        self.error_value = np.random.normal(0, 0.06)

class ErrorTROPO(ErrorSNS):

    def __init__(self):
        self.error_value = np.random.normal(0, 0.09)

class ErrorINTERNALNOISE(ErrorSNS):

    def __init__(self):
        self.error_value = np.random.normal(0, 0.08)



for i in range(num_steps):


    # Моделирование изменения параметров полета с учетом ошибок
    new_latitude = latitude[i] + np.random.normal(0, 0.02)
    new_longitude = longitude[i] + np.random.normal(0, 0.02)
    new_east_speed = initial_speed_east + np.random.normal(0, 5)
    new_north_speed = initial_speed_north + np.random.normal(0, 2)

    # Применение погрешностей и ошибок
    new_latitude += new_latitude + (ErrorNKA().error_value + ErrorION().error_value + ErrorTROPO().error_value + ErrorINTERNALNOISE().error_value)
    new_longitude += new_longitude + (ErrorNKA().error_value + ErrorION().error_value + ErrorTROPO().error_value + ErrorINTERNALNOISE().error_value)
    new_east_speed += new_east_speed + (ErrorNKA().error_value + ErrorION().error_value + ErrorTROPO().error_value + ErrorINTERNALNOISE().error_value)
    new_north_speed += new_north_speed + (ErrorNKA().error_value + ErrorION().error_value + ErrorTROPO().error_value + ErrorINTERNALNOISE().error_value)

    latitude.append(new_latitude)
    longitude.append(new_longitude)
    east_projection_speed.append(new_east_speed)
    north_projection_speed.append(new_north_speed)

data = {
    'latitude': latitude,
    'longitude': longitude,
    'east_speed': east_projection_speed,
    'north_speed': north_projection_speed
}



# Определяем структур
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

# Структура INS
class INS(Structure):
    _fields_ = [
        ('roll', c_float),
        ('pitch', c_float),
        ('yaw', c_float)
    ]

# Главная структура SNS
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

#экземпляр структуры SNS и заполняем данными
sns_data = SNS()
sns_data.hour.hours = 12
sns_data.hour.minutes = 30
sns_data.hour.seconds = 45
sns_data.date.day = 15
sns_data.date.month = 3
sns_data.date.year = 2024
sns_data.cur_lat = 54.9841
sns_data.cur_long = 82.8986
sns_data.speed = 45.6
sns_data.braking = True
sns_data.raining = False
sns_data.ins.roll = 1.23
sns_data.ins.pitch = -0.56
sns_data.ins.yaw = 2.34


sock.sendto(sns_data, SERVER_ADDR)
sock.sendto(pickle.dumps(data), SERVER_ADDR)
sock.close()
