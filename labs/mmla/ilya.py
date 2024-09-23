import matplotlib.pyplot as plt
import numpy as np


class Rangefinder:
    """Класс датчика-дальномера"""

    def __init__(self, dt):
        """Конструктор класса дальномера"""

        # модель -- LRF 6742
        self.measures = []
        self.dt = dt
        self.divergence_rms = 3e-3  # СКО ошибки отклонения луча
        self.accuracy_rms = 33e-2  # СКО ошибки точности измерений
        self.ground_inconsistence = 2  # Разброс высот на местности

    def clear_measures(self):
        """Метод, обнуляющий массив измерений"""

        self.measures = []

    def take_measures(self, heights: list, ground_level: float, random_ground: bool = True):
        """Метод проведения измерений дальномером данных с заданного списка"""

        y0 = np.random.uniform(0, 2 * np.pi)  # случайная начальная фаза

        # модель случайного изменения поверхности
        def rand_ground(t, w=0.01):
            return self.ground_inconsistence * np.cos(w * t + y0)

        i = 0
        for height in heights:
            if random_ground:
                self.measures.append(height + ground_level +
                                     1 / np.cos(np.random.normal(0, self.divergence_rms)) +
                                     np.random.normal(0, self.accuracy_rms) +
                                     rand_ground(i * self.dt))
                i += 1
            else:
                self.measures.append(height + ground_level +
                                     1 / np.cos(np.random.normal(0, self.divergence_rms)) +
                                     np.random.normal(0, self.accuracy_rms))

        return self.measures


class Altimeter:
    """Класс датчика-баровысотомера"""

    def __init__(self, dt):
        """Конструктор класса баровысотомера"""

        # модель -- HP206C
        self.measures = []
        self.dt = dt
        self.abs = np.random.normal(0, 1e-3)  # Абсолютная ошибка, т.е. сдвиг от нуля
        self.rel_rms = 0.16e-3  # СКО относительной ошибки, т.е. разброса измерения
        self.power_noise_rms = 0.83e-3  # СКО ошибки от питания
        self.operating_rms = abs(np.random.normal(0, 0.66e-3))  # СКО ошибки от наработки барокамеры

    def clear_measures(self):
        """Метод, обнуляющий массив измерений"""

        self.measures = []

    def take_measures(self, pressures: list, ground_pressure: float = 1):
        """Метод проведения измерений баровысотомером данных с заданного списка"""

        # h = P / ro * g
        ro = 1.27
        g = 9.81

        for pressure in pressures:
            pressure = (pressure + self.abs + np.random.normal(0, self.rel_rms) +
                        np.random.normal(0, self.power_noise_rms) + self.operating_rms)
            h = (ground_pressure - pressure) * 1e5 / (ro * g)
            self.measures.append(h)

        return self.measures


def kalman_filter(input_data, innit_data: list = None, shape: int = 3, init_rms: float = 1, K: float = 0.1):
    """Метод, реализующий фильтр Калмана"""

    # Алгоритм фильтрации взят из книжки Красильщикова М.Н. и Себрякова Г.Г. (ред.)
    # «Современные информационные технологии в задачах навигации и
    # наведения беспилотных маневренных летательных аппаратов»

    # начальные нулевые значения и объявление необходимых матриц
    init_cov = np.eye(shape) * init_rms  # начальное приближение задаем диагональной матрицей с элементами init_rms

    A = np.eye(shape)
    H = np.eye(shape)
    Q = np.eye(shape)
    R = np.eye(shape)

    if innit_data is None:
        curr = np.array([0] * shape)  # текущие значения
    else:
        curr = np.array(innit_data)
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
            cov = np.dot((np.eye(shape) - np.dot(kalman_gain, H)), cov)

        output.append(curr * K)

    return output


def compensation_scheme(path1, path2):
    """Метод, реализующий схему компенсации для комплексирования измерений"""

    temp_path = []
    for i in range(len(path1)):
        temp_path.append(path1[i] - path2[i])
    filtered = kalman_filter(temp_path, shape=1, innit_data=temp_path[0], init_rms=0.1)

    res_path = []
    for i in range(len(path1)):
        res_path.append(path1[i] - filtered[i])

    return res_path


def generate_pressure_path(path, ground_pressure=1):
    pressures = []
    ro = 1.27
    g = 9.81
    for height in path:
        pressures.append(ground_pressure - height * g * ro * 1e-5)

    return pressures


def main():
    dt = 0.1  # частота системы -- 10 ГЦ
    ranger = Rangefinder(dt)
    alter = Altimeter(dt)

    path = []
    for i in range(100):
        path.append(100 + i / 2)
    # path = [100] * 100

    ground_level = 150  # высота поверхности над уровнем моря
    ground_level_pressure = 1  # давление на поверхности
    pressure_path = generate_pressure_path(path, ground_level_pressure)  # давления

    ranges = ranger.take_measures(path, ground_level)  # измерения дальномера
    heights = alter.take_measures(pressure_path, ground_level_pressure)  # измерения высотомера
    heights = [item + ground_level for item in heights]

    ranger.clear_measures()
    ranges2 = ranger.take_measures(path, ground_level)  # фейкуем измерения
    complex_path = compensation_scheme(ranges2, heights)
    complex_path = [item[0] for item in complex_path]  # ФК выдает немного коряво для скаляров

    t = np.arange(1, len(path) + 1, 1)
    t = [item * dt for item in t]

    plt.xlabel('Время, с')
    plt.ylabel('Высота, м')
    plt.plot(t, heights, color='blue')
    plt.title('Измерения баровысотомера')
    plt.show()

    plt.xlabel('Время, с')
    plt.ylabel('Высота, м')
    plt.plot(t, ranges, color='red')
    plt.title('Измерения дальномера')
    plt.show()

    plt.xlabel('Время, с')
    plt.ylabel('Высота, м')
    plt.plot(t, complex_path, color='green', linewidth=1.5, label='Комплексное решение')
    plt.plot(t, heights, color='blue', linewidth=0.5, label='Баровысотомер')
    plt.plot(t, ranges, color='red', linewidth=0.5, label='Дальномер')
    plt.title('Комплексное решение')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
