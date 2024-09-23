import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.stats import linregress
from scipy.signal import periodogram

g = 9.81  # ускорение свободного падения на поверхности Земли


class BBox:
    """Класс "черного ящика", который совершает движение"""
    path = []  # массив перемещений, содержащий ВСЕ данные из файла

    def __init__(self, data=None):
        """Конструктор класса"""
        if data is not None:  # можно создать класс со сразу привязанным к нему файлом
            self.read_file(data)

    def read_file(self, file):
        """Функция, считывающая информацию с файла"""
        for line in file:
            try:
                # split через ';' -> добавляем в массив path сформированный массив из 0-7 элементов line
                self.path.append([float(line.split(';')[x]) for x in range(11)])
            except ValueError:
                # пропуск не числовых строк
                print(f'line <<{line}>> passed\n')


class Worker:
    """Класс "рабочего", реализующего эксперимент и его выводы"""

    def __init__(self):
        """Конструктор класса"""
        self.t = time.time()

    def __del__(self):
        """Деструктор класса"""
        print(f'Service length of worker was increased by {time.time() - self.t} seconds.')

    def spectral_density(self, data, is_slice=False, z_needed=True):
        """Функция, строящая спектральные плотности ускорений"""
        if not is_slice:
            sdx, pxx_x = periodogram([item[5] for item in data], 1e6)
            sdy, pxx_y = periodogram([item[6] for item in data], 1e6)

            plt.title('Spectral Density of aX')
            plt.xlabel('Frequency, Hz')
            plt.ylabel('Power spectral density, W/Hz')
            plt.plot(sdx, np.sqrt(pxx_x), '-o')
            plt.show()

            plt.title('Spectral Density of aY')
            plt.xlabel('Frequency, Hz')
            plt.ylabel('Power spectral density, W/Hz')
            plt.plot(sdy, np.sqrt(pxx_y), '-o')
            plt.show()

            if z_needed:
                sdz, pxx_z = periodogram([item[7] for item in data], 1e6)

                plt.title('Spectral Density of aZ')
                plt.xlabel('Frequency, Hz')
                plt.ylabel('Power spectral density, W/Hz')
                plt.plot(sdz, np.sqrt(pxx_z), '-o')
                plt.show()
        else:
            sdx, pxx_x = periodogram([item[0] for item in data], 1e6)
            sdy, pxx_y = periodogram([item[1] for item in data], 1e6)

            plt.title('Spectral Density of aX')
            plt.xlabel('Frequency, Hz')
            plt.ylabel('Power spectral density, W/Hz')
            plt.plot(sdx, np.sqrt(pxx_x), '-o')
            plt.xlim([0, 1e5])
            plt.show()

            plt.title('Spectral Density of aY')
            plt.xlabel('Frequency, Hz')
            plt.ylabel('Power spectral density, W/Hz')
            plt.plot(sdy, np.sqrt(pxx_y), '-o')
            plt.xlim([0, 1e5])
            plt.show()

            if z_needed:
                try:
                    sdz, pxx_z = periodogram([item[2] for item in data], 1e6)

                    plt.title('Spectral Density of aZ')
                    plt.xlabel('Frequency, Hz')
                    plt.ylabel('Power spectral density, W/Hz')
                    plt.plot(sdz, np.sqrt(pxx_z))
                    plt.show()
                except IndexError:
                    print('no z\'s?')

    def zero_bias(self, data):
        """Функция, оценивающая смещение нуля"""
        xbias = 0
        ybias = 0
        zbias = 0
        # по сути, вычисление среднего по первым и последним 50-ти измерениям
        for i in range(3000):
            xbias += data[i][5]
            ybias += data[i][6]
            zbias += data[i][7]
        xbias = xbias / 3000
        ybias = ybias / 3000
        zbias = zbias / 3000
        return [xbias, ybias, zbias]

    def lin_func(self, y):
        """Функция, возвращающая список значений прямой-тренда y = kx + b"""
        x = [x for x in range(len(y))]  # x -- массив из номеров измерений
        k, b, _, _, _ = linregress(x, y)
        values = []
        for i in range(len(x)):
            values.append(k * x[i] + b)
        return values, k

    def move(self, data, rotation=False, postprocessing=True):
        """Функция, просчитывающая движение по набору данных"""
        acc = []  # для построения графиков
        if postprocessing:
            acc_raw = []  # для обработки
            bias = self.zero_bias(data)
            i = 0
            N = 100  # длина отрезков для линейной регрессии
            crit_k = 0.1  # критическое значение углового коэффициента для линейной регрессии (маркер движения)
            eof = len(data)  # end of file ~ eof -- значение последнего номера строки в файле
            for item in data:
                if i != eof and i < N:
                    acc_raw.append([item[5] - bias[0], item[6] - bias[1], item[7] - bias[2]])
                else:
                    x_trend, kx = self.lin_func([item[0] for item in acc_raw])
                    y_trend, ky = self.lin_func([item[1] for item in acc_raw])
                    z_trend, kz = self.lin_func([item[2] for item in acc_raw])

                    #  возможность посмотреть участки с линейной регрессией
                    # if kx > crit_k or ky > crit_k:
                    #     plt.plot([item[0] for item in acc_raw], color='red')
                    #     plt.plot(x_trend, color='blue')
                    #     plt.title(f'X Regression, kx = {kx}')
                    #     plt.show()
                    #
                    #     plt.plot([item[1] for item in acc_raw], color='red')
                    #     plt.plot(y_trend, color='blue')
                    #     plt.title(f'Y Regression, ky = {ky}')
                    #     plt.show()
                    #
                    #     self.spectral_density(acc_raw, is_slice=True, z_needed=False)

                    new_line = []
                    for j in range(len(x_trend)):
                        if abs(kx) < crit_k:
                            new_line.append(acc_raw[j][0] - x_trend[j])
                        else:
                            new_line.append(acc_raw[j][0])
                        if abs(ky) < crit_k:
                            new_line.append(acc_raw[j][1] - y_trend[j])
                        else:
                            new_line.append(acc_raw[j][1])
                        if abs(kz) < crit_k:
                            new_line.append(acc_raw[j][2] - z_trend[j])
                        else:
                            new_line.append(acc_raw[j][2])
                        acc.append(new_line)
                        new_line = []
                    # print(len(acc))
                    i = -1
                    eof = eof - N
                    # print(f'eof={eof}')
                    acc_raw = []
                i += 1
        else:
            for item in data:
                acc.append([item[5], item[6], item[7]])

        print(len(acc), len(data))
        # возможность посмотреть графики изменения ускорений
        # plt.title('X_acc')
        # plt.plot([item[0] for item in acc])
        # plt.show()
        # plt.title('Y_acc')
        # plt.plot([item[1] for item in acc])
        # plt.show()

        trajectory = []
        if not rotation:
            trajectory.append([0, 0, 0, 0, 0, 0])
            for i in range(len(acc)):
                dt = data[i][1] * 1e-6  # у нас микросекунды, как я понял
                ax = acc[i][0] * g / 300  # ax = line[5] -- без учета размерности
                ay = acc[i][1] * g / 300
                az = (acc[i][2] + 300) * g / 300
                new = [ax * dt * dt / 2, ay * dt * dt / 2, az * dt * dt / 2, ax * dt, ay * dt, az * dt]
                for j in range(6):
                    new[j] += trajectory[-1][j]  # учитываем перемещение
                trajectory.append(new)  # история положений (траектория)
            return trajectory
        else:
            # матрицы поворота по XYZ
            def Mx(theta):
                return np.array([[1,             0,              0],
                                 [0, np.cos(theta), -np.sin(theta)],
                                 [0, np.sin(theta),  np.cos(theta)]])

            def My(theta):
                return np.array([[np.cos(theta), 0, np.sin(theta)],
                                 [0,             1,             0],
                                 [np.sin(theta), 0, np.cos(theta)]])

            def Mz(theta):
                return np.array([[np.cos(theta), -np.sin(theta), 0],
                                 [np.sin(theta),  np.cos(theta), 0],
                                 [0,                          0, 1]])
            print('rotation not included yet')
            return None

    def graph(self, trajectory, scale=True):
        """Функция, реализующая построение графиков"""
        if not scale:
            plt.xlim([-0.3, 0.3])  # из всех измерений, то было самым большим по модулю из координат XY
            plt.ylim([-0.3, 0.3])
        plt.plot([item[0] for item in trajectory], [item[1] for item in trajectory])
        plt.title('XY trajectory')
        plt.xlabel('X coordinates')
        plt.ylabel('Y coordinates')
        plt.show()

    def experiment(self, file, needs_scaling=True, needs_rotation=False,
                   needs_postprocessing=True):
        """Функция, реализующая эксперимент"""
        box = BBox(file)
        # self.spectral_density(box.path)
        data = self.move(box.path, rotation=needs_rotation, postprocessing=needs_postprocessing)
        self.graph(data, scale=needs_scaling)


def main():
    """Основная исполняющая функция"""
    # file = open('lr 1 bins/test_bins2_bins.csv', 'r')
    file = open('test_bins2_bins.csv', 'r')
    somebody = Worker()
    somebody.experiment(file, needs_postprocessing=False)


# предотвращение ненужных запусков при подключении модуля к другим проектам
if __name__ == '__main__':
    main()
