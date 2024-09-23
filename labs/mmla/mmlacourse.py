import numpy as np
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod

g = 9.81


class Accelerometer(metaclass=ABCMeta):
    """Абстрактный класс акселерометра"""

    @abstractmethod
    def __init__(self):
        """Абстрактный конструктор класса"""

        pass

    @abstractmethod
    def take_measures(self, path: list):
        """Абстрактный метод получения измерений на траектории"""

        pass


class ADXL335(Accelerometer):
    """Класс датчика-акселерометра ADXL335"""

    def __init__(self):
        """Конструктор класса конкретного акселерометра"""

        # выставляем по умолчанию случайные значения в пределах, соответствующих спецификации
        nl = np.random.normal(0, 0.001)
        casx = np.random.normal(0, 0.0033)
        casy = np.random.normal(0, 0.0033)
        casz = np.random.normal(0, 0.0033)
        vtog = np.random.normal(0.3, 0.0033)
        zbx = np.random.normal(0.15, 0.05)
        zby = np.random.normal(0.15, 0.05)
        zbz = np.random.normal(0.15, 0.1)
        ndx = np.random.normal(150, 10)
        ndy = np.random.normal(150, 10)
        ndz = np.random.normal(300, 20)

        self.measures = []
        self.bandwidth_xy = 1600
        self.bandwidth_z = 550
        self.nonlinearity = abs(nl)  # nonlinearity / нелинейность
        self.cross_axis_sensivity_x = casx  # cross-axis sensivity / межосная чувствительность
        self.cross_axis_sensivity_y = casy
        self.cross_axis_sensivity_z = casz
        self.V_to_g = vtog  # перевод вольтов из спецификации в м/c^2
        self.zero_bias_x = zbx / (self.V_to_g * g)  # zero bias / смещение нуля
        self.zero_bias_y = zby / (self.V_to_g * g)
        self.zero_bias_z = zbz / (self.V_to_g * g)
        self.noise_rms_x = abs(ndx) * np.sqrt(self.bandwidth_xy * 1.6) * 1e-6  # noise density rms в м/с^2
        # такой коэф. выбран по рекоммендации Analog Devices
        self.noise_rms_y = abs(ndy) * np.sqrt(self.bandwidth_xy * 1.6) * 1e-6
        # для частот среза 1600 и 550 соответвенно по XY и Z
        self.noise_rms_z = abs(ndz) * np.sqrt(self.bandwidth_z * 1.6) * 1e-6

    def clear_measures(self):
        """Метод, обнуляющий массив измерений"""

        self.measures = []

    def info(self):
        """Метод для просмотра характеристик акселерометра"""

        print(f'\nУ этого акселерометра модели ADXL335 следующие характеристики:')
        print(f'Нелинейность: {self.nonlinearity * 100} %')
        # длинная строка, но если разбивать, то интерпретатор ругается, потому так оставлю
        print(
            f'Междуосная чувствительность по XYZ: {self.cross_axis_sensivity_x * 100, self.cross_axis_sensivity_y * 100, self.cross_axis_sensivity_z * 100} %')
        print(f'Смещение нуля по XYZ: {self.zero_bias_x, self.zero_bias_y, self.zero_bias_z} м/c^2')
        print(f'СКО шумов для XYZ: {self.noise_rms_x, self.noise_rms_y, self.noise_rms_z}, м/с^2')

    def take_measures(self, path: list):
        """Метод проведения измерений акселерометром данных с заданного списка"""

        step = []
        for item in path:
            # замер = истина + смещение ноля + нелинейность + шум + межосная чувствительность по Y + по Z
            step.append(item[0] + self.zero_bias_x + np.random.normal(0, self.nonlinearity / 3) * item[0]
                        + np.random.normal(0, self.noise_rms_x) + self.cross_axis_sensivity_y * item[1]
                        + self.cross_axis_sensivity_z * item[2])
            step.append(item[1] + self.zero_bias_y + np.random.normal(0, self.nonlinearity / 3) * item[1]
                        + np.random.normal(0, self.noise_rms_y) + self.cross_axis_sensivity_x * item[0]
                        + self.cross_axis_sensivity_z * item[2])
            step.append(item[2] + self.zero_bias_z + np.random.normal(0, self.nonlinearity / 3) * item[2]
                        + np.random.normal(0, self.noise_rms_z) + self.cross_axis_sensivity_x * item[0]
                        + self.cross_axis_sensivity_y * item[1])

            self.measures.append(step)
            step = []

        return self.measures


class GNSS(metaclass=ABCMeta):
    """Абстрактный класс акселерометра"""

    @abstractmethod
    def __init__(self):
        """Абстрактный конструктор класса"""

        pass

    @abstractmethod
    def take_measures(self, path: list, delay: int):
        """Абстрактный метод получения измерений на траектории"""

        pass


class Satellite(GNSS):
    """Класс некого спутника"""

    def __init__(self, receiver_error: float = 1, ion_error: float = 3,
                 trop_error: float = 2, noise_error: float = 0.5):
        """Конструктор некого спутника"""

        # Модель ошибок измерителя ГНСС взята из книжки Красильщикова М.Н. и Себрякова Г.Г. (ред.)
        # «Современные информационные технологии в задачах навигации и
        # наведения беспилотных маневренных летательных аппаратов»

        self.measures = []
        self.delay = 0
        self.receiver_error = receiver_error  # погрешность от навигационной аппаратуры потребителя
        self.ion_error = ion_error  # погрешность от ионосферы
        self.trop_error = trop_error  # погрешность от тропосферы
        self.noise_error = noise_error  # СКО шумов

    def take_measures(self, path: list, delay: int):
        """Метод проведения измерений спутником данных с заданного списка"""

        step = []
        self.delay = delay  # задержка измерителя (по сути, сколько значений пропускать до следующей обработки)
        if delay != 0:
            delay_count = 0  # счетчик для пропуска значений
            for item in path:
                if delay_count == 0:
                    # замер = истина + смещение ноля + нелинейность + шум + межосная чувствительность по Y + по Z
                    step.append(item[0] + np.random.normal(0, self.receiver_error) + np.random.normal(0, self.ion_error)
                                + np.random.normal(0, self.trop_error) + np.random.normal(0, self.noise_error))
                    step.append(item[1] + np.random.normal(0, self.receiver_error) + np.random.normal(0, self.ion_error)
                                + np.random.normal(0, self.trop_error) + np.random.normal(0, self.noise_error))
                    step.append(item[2] + np.random.normal(0, self.receiver_error) + np.random.normal(0, self.ion_error)
                                + np.random.normal(0, self.trop_error) + np.random.normal(0, self.noise_error))
                    delay_count = self.delay
                    self.measures.append(step)
                    step = []
                else:
                    delay_count -= 1
                    self.measures.append(self.measures[-1])
        else:
            for item in path:
                # замер = истина + смещение ноля + нелинейность + шум + межосная чувствительность по Y + по Z
                step.append(item[0] + np.random.normal(0, self.receiver_error) + np.random.normal(0, self.ion_error)
                            + np.random.normal(0, self.trop_error) + np.random.normal(0, self.noise_error))
                step.append(item[1] + np.random.normal(0, self.receiver_error) + np.random.normal(0, self.ion_error)
                            + np.random.normal(0, self.trop_error) + np.random.normal(0, self.noise_error))
                step.append(item[2] + np.random.normal(0, self.receiver_error) + np.random.normal(0, self.ion_error)
                            + np.random.normal(0, self.trop_error) + np.random.normal(0, self.noise_error))
                self.measures.append(step)
                step = []

        return self.measures


def kalman_filter(input_data, innit_data: list = None, shape: int = 3, init_rms: float = 1, K: float = 0.1):
    """Метод, реализующий фильтр Калмана"""

    # Алгоритм фильтрации взят из книжки Красильщикова М.Н. и Себрякова Г.Г. (ред.)
    # «Современные информационные технологии в задачах навигации и
    # наведения беспилотных маневренных летательных аппаратов»

    # начальные нулевые значения и объявление необходимых матриц
    init_cov = np.eye(shape) * init_rms  # начальное приближение задаем диагональной матрицей с элементами init_rms

    # все начальные значения задаем единичными
    A = np.eye(shape)
    H = np.eye(shape)
    Q = np.eye(shape)
    R = np.eye(shape)

    if innit_data is None:
        curr = np.array([0] * shape)  # текущие значения
    else:
        if len(innit_data) != shape:
            raise ValueError('Неверный размер начального вектора')
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


def compensation_scheme(acc_path, gnss_path):
    """Метод, реализующий схему компенсации для комплексирования измерений"""

    temp_path = []
    for i in range(len(acc_path)):
        temp_path.append([acc_path[i][0] - gnss_path[i][0], acc_path[i][1] - gnss_path[i][1],
                          acc_path[i][2] - gnss_path[i][2]])
    filtered = kalman_filter(temp_path, innit_data=temp_path[0], init_rms=0.1)

    res_path = []
    for i in range(len(acc_path)):
        res_path.append([acc_path[i][0] - filtered[i][0], acc_path[i][1] - filtered[i][1],
                         acc_path[i][2] - filtered[i][2]])

    return res_path


def calc_measured_path(path: list, dt: float):
    """Функция для вычисления траектории по ускорениям"""

    if len(path) == 0:
        raise Exception('Замеры не были проведены')

    x_real = []
    y_real = []
    z_real = []
    vx_real = []
    vy_real = []
    vz_real = []

    for item in path:
        try:
            vx_real.append(vx_real[-1] + item[0] * dt)
            vy_real.append(vy_real[-1] + item[1] * dt)
            vz_real.append(vz_real[-1] + item[2] * dt)
            x_real.append(x_real[-1] + vx_real[-1] * dt)
            y_real.append(y_real[-1] + vy_real[-1] * dt)
            z_real.append(z_real[-1] + vz_real[-1] * dt)
        except IndexError:
            vx_real.append(item[0] * dt)
            vy_real.append(item[1] * dt)
            vz_real.append(item[2] * dt)
            x_real.append(vx_real[-1] * dt)
            y_real.append(vy_real[-1] * dt)
            z_real.append(vz_real[-1] * dt)

    output = []
    for i in range(len(x_real)):
        output.append([x_real[i], y_real[i], z_real[i]])

    return output


def show_paths(acc_path: list, gnss_path: list, complex_path: list, title: str = '', dt: float = 0.01):
    """Метод для отображения всех координат траектории"""

    x = np.arange(1, len(acc_path) + 1, 1)
    x = [item * dt for item in x]
    plt.plot(x, acc_path, label='Акселерометр')
    plt.plot(x, gnss_path, label='ГНСС')
    plt.plot(x, complex_path, '-.', label='Комплексное решение')

    plt.xlabel("Время, с")
    plt.ylabel('Измеренное значение координаты, м')
    plt.legend()
    plt.title(title)
    plt.show()


def main():
    """Основной исполняющий метод"""

    gnss = Satellite()
    acc = ADXL335()
    dt = 0.1
    end_t = 10

    def x_path(t):
        return 0

    def ax_path(t):
        return 0

    def y_path(t):
        return 0.5 * t * t

    def ay_path(t):
        return 1

    def z_path(t):
        return 0

    def az_path(t):
        return 0

    gnss_path = []
    acc_path = []
    for t in range(round(end_t / dt)):
        t = t * dt
        gnss_path.append([x_path(t), y_path(t), z_path(t)])
        acc_path.append([ax_path(t), ay_path(t), az_path(t)])

    acc_path = acc.take_measures(acc_path)
    gnss_path = gnss.take_measures(gnss_path, 0)
    acc_path = calc_measured_path(acc_path, dt)
    complex_path = compensation_scheme(acc_path, gnss_path)

    x_acc_path = [item[0] for item in acc_path]
    y_acc_path = [item[1] for item in acc_path]
    z_acc_path = [item[2] for item in acc_path]

    x_gnss_path = [item[0] for item in gnss_path]
    y_gnss_path = [item[1] for item in gnss_path]
    z_gnss_path = [item[2] for item in gnss_path]

    x_complex_path = [item[0] for item in complex_path]
    y_complex_path = [item[1] for item in complex_path]
    z_complex_path = [item[2] for item in complex_path]

    show_paths(x_acc_path, x_gnss_path, x_complex_path, title='Движение по оси X', dt=dt)
    show_paths(y_acc_path, y_gnss_path, y_complex_path, title='Движение по оси Y', dt=dt)
    show_paths(z_acc_path, z_gnss_path, z_complex_path, title='Движение по оси Z', dt=dt)


if __name__ == "__main__":
    main()
