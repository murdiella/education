import numpy as np
import matplotlib.pyplot as plt

g = 9.81  # Ускорение свободного падения
dt = 1e-3  # dt для всей системы, равное 1 мс


class Accelerometer:
    """Класс датчика-акселерометра ADXL3X5"""

    def __init__(self, model='335'):
        """Конструктор класса"""

        if model == '335':
            nl = np.random.normal(0, 0.001)  # выставляем по умолчанию случайные значения в соответствие со спецификацией
            casx = np.random.normal(0, 0.0033)
            casy = np.random.normal(0, 0.0033)
            casz = np.random.normal(0, 0.0033)
            vtog = np.random.normal(0.3, 0.0033)
            zbx = np.random.normal(1.5, 0.05)
            zby = np.random.normal(1.5, 0.05)
            zbz = np.random.normal(1.5, 0.1)
            ndx = np.random.normal(150, 10)
            ndy = np.random.normal(150, 10)
            ndz = np.random.normal(300, 20)
            self.bandwidth_xy = 1600
            self.bandwidth_z = 550
        elif model == '345':
            nl = np.random.normal(0, 0.01667)
            casx = np.random.normal(0, 0.0033)
            casy = np.random.normal(0, 0.0033)
            casz = np.random.normal(0, 0.0033)
            vtog = 1 / g  # смещение ноля дано сразу в g
            zbx = np.random.normal(0.04, 0.05)
            zby = np.random.normal(0.04, 0.05)
            zbz = np.random.normal(0.08, 0.0833)
            ndx = 265
            ndy = 265
            ndz = 265
            self.bandwidth_xy = 100
            self.bandwidth_z = 100
        elif model == '355':
            nl = np.random.normal(0, 0.01667)
            casx = np.random.normal(0, 0.0033)
            casy = np.random.normal(0, 0.0033)
            casz = np.random.normal(0, 0.0033)
            vtog = 1 / g
            zbx = np.random.normal(0, 0.025)
            zby = np.random.normal(0, 0.025)
            zbz = np.random.normal(0, 0.025)
            ndx = np.random.normal(0, 25)
            ndy = np.random.normal(0, 25)
            ndz = np.random.normal(0, 25)
            self.bandwidth_xy = 1000
            self.bandwidth_z = 1000
        else:
            raise Exception('Данной модели в скрипте нет')

        self.model = f'ADXL{model}'
        self.measures = []
        self.nonlinearity = abs(nl)  # nonlinearity
        self.cross_axis_sensivity_x = casx  # cross-axis sensivity
        self.cross_axis_sensivity_y = casy
        self.cross_axis_sensivity_z = casz
        self.V_to_g = vtog  # перевод вольтов из спецификации в м/c^2
        self.zero_bias_x = zbx / (self.V_to_g * g)  # zero bias
        self.zero_bias_y = zby / (self.V_to_g * g)
        self.zero_bias_z = zbz / (self.V_to_g * g)
        self.noise_rms_x = abs(ndx) * np.sqrt(self.bandwidth_xy * 1.6) * 1e-6  # noise density rms в м/с^2
        self.noise_rms_y = abs(ndy) * np.sqrt(self.bandwidth_xy * 1.6) * 1e-6  # такой коэф. выбран по рекоммендации Analog Devices
        self.noise_rms_z = abs(ndz) * np.sqrt(self.bandwidth_z * 1.6) * 1e-6  # для частот среза 1600 и 550 соответвенно по XY и Z

    def clear_measures(self):
        """Функция, обнуляющая массив измерений"""

        self.measures = []

    def info(self):
        """Функция для просмотра характеристик акселерометра"""

        print(f'\nУ этого {self.model} следующие характеристики:')
        print(f'Нелинейность: {self.nonlinearity * 100} %')
        print(f'Междуосная чувствительность по XYZ: {self.cross_axis_sensivity_x * 100, self.cross_axis_sensivity_y * 100, self.cross_axis_sensivity_z * 100} %')
        print(f'Смещение нуля по XYZ: {self.zero_bias_x, self.zero_bias_y, self.zero_bias_z} м/c^2')
        print(f'СКО шумов для XYZ: {self.noise_rms_x, self.noise_rms_y, self.noise_rms_z}, м/с^2')

    def take_measures(self, wanderer_path: list):
        """Функция проведения измерений акселерометром данных с заданного списка"""

        step = []
        for item in wanderer_path:
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

    def show_measured_path(self, wanderer_path: list):
        """Функция для построения и сравнения траекторий истинной и измеренной"""

        if len(self.measures) == 0:
            raise Exception('Замеры не были проведены')

        x_real = []
        y_real = []
        z_real = []
        vx_real = []
        vy_real = []
        vz_real = []

        x_measured = []
        y_measured = []
        z_measured = []
        vx_measured = []
        vy_measured = []
        vz_measured = []

        for item in wanderer_path:
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

        for item in self.measures:
            try:
                vx_measured.append(vx_measured[-1] + item[0] * dt)
                vy_measured.append(vy_measured[-1] + item[1] * dt)
                vz_measured.append(vz_measured[-1] + item[2] * dt)
                x_measured.append(x_measured[-1] + vx_measured[-1] * dt)
                y_measured.append(y_measured[-1] + vy_measured[-1] * dt)
                z_measured.append(z_measured[-1] + vz_measured[-1] * dt)
            except IndexError:
                vx_measured.append(item[0] * dt)
                vy_measured.append(item[1] * dt)
                vz_measured.append(item[2] * dt)
                x_measured.append(vx_measured[-1] * dt)
                y_measured.append(vy_measured[-1] * dt)
                z_measured.append(vz_measured[-1] * dt)

        plt.plot(x_real, y_real, color='b')
        plt.plot(x_measured, y_measured, color='r')
        plt.xlabel('X, метры\nКрасным - измерения, синим - истинная траектория')
        plt.ylabel('Y, метры')
        plt.title(f'Траектория движения в XY, истина + измеренное {self.model}')
        plt.show()


class Wanderer:
    """Класс объекта, совершающего движение"""

    def __init__(self):
        """Конструктор класса"""

        self.path = [[0, 0, 0]]  # начальная позиция траектории, [x, y, z] в м/c^2

    def clear_path(self):
        """Функция для очистки траектории"""

        self.path.clear()

    def linear(self, length: int, a_x=0, a_y=0, a_z=g):
        """Добавить отрезок движения с постоянными ускорениями"""

        for _ in range(length):
            step = [a_x, a_y, a_z - g]
            self.path.append(step)

    def harmonic_along_x(self, length: int, a_y, amp=1, w=1, ph=np.pi / 2):
        """Добавить отрезок гармонического колебания вдоль оси Х"""

        for i in range(length):
            step = [amp * np.sin(w * i + ph), a_y, 0]
            self.path.append(step)

    def harmonic_along_y(self, length: int, a_x, amp=1, w=1, ph=np.pi / 2):
        """Добавить отрезок гармонического колебания вдоль оси Y"""

        for i in range(length):
            step = [a_x, amp * np.sin(w * i + ph), 0]
            self.path.append(step)

    def show_path_xy(self):
        """Посмотреть текущую траекторию в плоскости xOy"""

        x = []
        y = []
        vx = []
        vy = []

        for item in self.path:
            try:
                vx.append(vx[-1] + item[0] * dt)
                vy.append(vy[-1] + item[1] * dt)
                x.append(x[-1] + vx[-1] * dt)
                y.append(y[-1] + vy[-1] * dt)
            except IndexError:
                vx.append(item[0] * dt)
                vy.append(item[1] * dt)
                x.append(vx[-1] * dt)
                y.append(vy[-1] * dt)

        plt.plot(x, y)
        plt.xlabel('X, метры')
        plt.ylabel('Y, метры')
        plt.show()


def main():
    # создаем объекты классов и запрашиваем информацию об акселерометре
    obj = Wanderer()
    adxl = Accelerometer(model='355')
    adxl.info()

    # создаем траекторию движения
    obj.harmonic_along_x(2000, 2, -20, 0.01)
    obj.harmonic_along_y(2000, -4, 30, 0.01)

    # проводим измерения и получаем результаты
    adxl.take_measures(obj.path)
    adxl.show_measured_path(obj.path)

    # очищаем траекторию и измерения, повторяем манипуляцию на другой траектории
    obj.clear_path()
    adxl.clear_measures()

    obj.harmonic_along_x(2000, 0.2, -2, 0.01)
    obj.harmonic_along_y(2000, -0.4, 3, 0.01)

    adxl.take_measures(obj.path)
    adxl.show_measured_path(obj.path)


if __name__ == "__main__":
    main()
