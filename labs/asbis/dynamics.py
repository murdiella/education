from numpy.random import normal
from abc import ABC, abstractmethod
from courier import ins_data, sns_data
from gui import graph
import numpy as np


class DynSns(ABC):
    """Класс формирования ошибок для СНС"""

    @abstractmethod
    def __init__(self):
        """Абстрактный метод для ошибок СНС"""
        pass


class SnsNap(DynSns):
    """Класс-потомок для погрешности от навигационной аппаратуры потребителя"""

    def __init__(self):
        self.error = normal(0, 0.1)


class SnsIon(DynSns):
    """Класс-потомок для погрешности от ионосферы"""

    def __init__(self):
        self.error = normal(0, 0.15)


class SnsTrop(DynSns):
    """Класс-потомок для погрешности от тропосферы"""

    def __init__(self):
        self.error = normal(0, 0.12)


class SnsNoise(DynSns):
    """Класс-потомок для погрешности от шумов"""

    def __init__(self):
        self.error = normal(0, 0.05)


def sim(ending_time: int = 10):
    """Метод для симуляции динамики процесса"""

    # начальные значения параметров и массивы для них
    init_lat = ins_data['latitude']['value']
    lat = [init_lat]
    init_long = ins_data['longitude']['value']
    long = [init_long]
    init_north_vel = ins_data['velocity_north']['value']
    north_vel = [init_north_vel]
    init_west_vel = ins_data['velocity_west']['value']
    east_vel = [init_west_vel]

    # симуляция динамики
    for i in range(ending_time):
        new_lat = lat[-1] + SnsNap().error + SnsIon().error + SnsTrop().error + SnsNoise().error
        lat.append(new_lat)
        new_long = long[-1] + SnsNap().error + SnsIon().error + SnsTrop().error + SnsNoise().error
        long.append(new_long)
        new_north_vel = north_vel[-1] + SnsNap().error + SnsIon().error + SnsTrop().error + SnsNoise().error
        north_vel.append(new_north_vel)
        new_east_vel = east_vel[-1] + SnsNap().error + SnsIon().error + SnsTrop().error + SnsNoise().error
        east_vel.append(new_east_vel)

    return lat, long, north_vel, east_vel


def kalman_filter(input_data):
    """Метод, реализующий фильтр Калмана"""

    # начальные нулевые значения и объявление необходимых матриц
    init_lat = 0
    init_long = 0
    init_north_vel = 0
    init_east_vel = 0
    init_cov = np.eye(4)

    A = np.eye(4)
    H = np.eye(4)
    Q = np.eye(4)
    R = np.eye(4)

    curr = np.array([init_lat, init_long, init_north_vel, init_east_vel])  # текущие значения
    cov = init_cov  # ковариационная матрица
    output = []  # массив результатов для вывода

    # основной цикл ФК
    for _ in range(len(input_data)):
        for data in input_data:
            curr = np.dot(A, curr)
            cov = np.dot(A, np.dot(cov, A.T)) + Q

            corr = data - np.dot(H, curr)
            corr_cov = np.dot(H, np.dot(cov, H.T)) + R
            kalman_gain = np.dot(cov, np.dot(H.T, np.linalg.inv(corr_cov)))

            curr = curr + np.dot(kalman_gain, corr)
            cov = np.dot((np.eye(4) - np.dot(kalman_gain, H)), cov)

        output.append(curr)

    return output


def show(input: list = None):
    """Метод для реализации динамики"""
    # запуск симуляции и введение нужных массивов
    if input is None:
        lat, long, north, east = sim()
    else:
        lat = input[0]
        long = input[1]
        north = input[2]
        east = input[3]
    data = []
    lats_sns = []
    lats_ins = []
    longs_sns = []
    longs_ins = []
    norths_sns = []
    norths_ins = []
    easts_sns = []
    easts_ins = []
    
    # разбивка на массивы для вывода для последующего применения
    for i in range(len(lat)):
        data.append([lat[i], long[i], north[i], east[i]])
        lats_sns.append(lat[i])
        lats_ins.append(ins_data['latitude']['value'])
        longs_sns.append(long[i])
        longs_ins.append(ins_data['longitude']['value'])
        norths_sns.append(north[i])
        norths_ins.append(ins_data['velocity_north']['value'])
        easts_sns.append(east[i])
        easts_ins.append(ins_data['velocity_west']['value'])
        
    out = kalman_filter(data)
    lats_complex = []
    longs_complex = []
    norths_complex = []
    easts_complex = []

    for item in out:
        lats_complex.append(item[0])
        longs_complex.append(item[1])
        norths_complex.append(item[2])
        easts_complex.append(item[3])
        
    # вывод графиков
    graph(lats_ins, lats_sns, lats_complex, title='ДОЛГОТА')
    graph(longs_ins, longs_sns, longs_complex, title='ШИРОТА')
    graph(norths_ins, norths_sns, norths_complex, title='СЕВЕРНАЯ ПРОЕКЦИЯ СКОРОСТИ')
    graph(easts_ins, easts_sns, easts_complex, title='ВОСТОЧНАЯ ПРОЕКЦИЯ СКОРОСТИ')


def app_exec(app):
    app.exec_()
    show()
