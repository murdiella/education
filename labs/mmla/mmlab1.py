import numpy as np
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod


class AAdapter(metaclass=ABCMeta):
    """Абстрактный класс адаптеров"""

    def __init__(self):
        """Абстрактный конструктор"""
        self.data = None

    @abstractmethod
    def calc(self, filename: str):
        """Абстрактный метод приведения к общему формату данных"""

        pass


class RINEXAdapter(AAdapter):
    """Класс адаптера формата RINEX"""

    def __init__(self):
        """Конструктор адаптера формата RINEX"""

        super().__init__()
        self.data = None

    def calc(self, filename: str):
        """Абстрактный метод вычисления из формата RINEX"""

        rinex_reader = RINEXReader()
        rinex_reader.read(filename)
        raw_data = rinex_reader.data

        mu = 3.9860050e14
        OMGE = 7.2921151467e-5
        self.data = []
        for item in raw_data:
            item = item.split('\n')
            num = int(item[0][1:3])
            time_min = int(item[0][15:17]) * 60 + int(item[0][18:20])

            # дернул вообще с другой лабы по расчету координат по сигналу со спутника GPS
            # embrace the govnocode
            a = float(item[2][61:80]) ** 2
            deln = float(item[1][42:61])
            M0 = float(item[1][61:80])
            e = float(item[2][23:42]) * 2 ** -33
            w = float(item[4][42:61])
            crs = float(item[1][23:42])
            crc = float(item[4][23:42])
            i0 = float(item[4][4:23])
            idot = float(item[5][4:23])
            cis = float(item[3][61:82])
            cic = float(item[3][23:42])
            cus = float(item[2][42:61])
            cuc = float(item[2][4:23])
            omega_0 = float(item[3][42:61])
            OMGd = float(item[4][61:80])

            tks = [1800, 3600, 5400]  # делей в 30, 60 и 90 минут для расчетов точек между замеров
            for tk in tks:
                n = np.sqrt(mu / (a ** 3)) + deln
                M = M0 + tk * n

                def Ei(E_input):
                    return M + e * np.sin(E_input)

                E = M
                for _ in range(3):
                    E = Ei(E)
                nu = np.arctan2(np.sin(E) * np.sqrt(1 - e ** 2), np.cos(E) - e)  # 5
                u = nu + w
                sin2u = np.sin(2 * u)  # 7
                cos2u = np.cos(2 * u)
                r = a * (1 - e * np.cos(E)) + crs * sin2u + crc * cos2u
                i = i0 + idot * tk + cis * sin2u + cic * cos2u
                u += cus * sin2u + cuc * cos2u
                xs = r * np.cos(u)  # 11
                ys = r * np.sin(u)
                omega = omega_0 + OMGd * tk - OMGE * tk
                sin_omega = np.sin(omega)  # 13
                cos_omega = np.cos(omega)
                x_ecef = xs * cos_omega - ys * np.cos(i) * sin_omega  # 14
                y_ecef = xs * sin_omega + ys * np.cos(i) * cos_omega
                z_ecef = ys * np.sin(i)

                # общий формат короче: [время (в минутах), номер спутника, x, y, z]
                # с переводом в метры и минуты
                self.data.append([time_min - (tk / 60), num, x_ecef / 1000, y_ecef / 1000, z_ecef / 1000])
                # print(self.data[-1])


class SP3Adapter(AAdapter):
    """Класс адаптера формата SP3"""

    def __init__(self):
        """Конструктор адаптера формата SP3"""

        super().__init__()
        self.data = None

    def calc(self, filename: str):
        """Абстрактный метод вычисления из формата SP3"""

        sp3_reader = SP3Reader()
        sp3_reader.read(filename)
        raw_data = sp3_reader.data

        # общий формат короче: [время (в минутах), номер спутника, x, y, z]
        self.data = []
        for item in raw_data:
            item = item.split('\n')
            time = 0
            for line in item:
                try:
                    if '*' in line:
                        time = int(line[14:16].strip()) * 60 + int(line[17:19].strip())  # нарезано лучше цезаря
                    else:
                        num = int(line[2:4])
                        x = float(line[5:18])
                        y = float(line[19:32])
                        z = float(line[33:46])
                        self.data.append([time, num, x, y, z])
                        # print(self.data[-1])  # православные методы отладки
                except ValueError:  # хз она вроде выскакивает а вроде ничего не ломается, просто пофиг на нее
                    pass


class AReader(metaclass=ABCMeta):
    """Абстрактный класс ридеров"""

    def __init__(self):
        """Абстрактный конструктор"""
        # нет блин реальный прораб

        self.data = None
        self.reader = None

    @abstractmethod
    def read(self, filename: str):
        """Абстрактный метод чтения"""

        pass


class RINEXReader(AReader):
    """Класс ридера формата RINEX"""

    def __init__(self):
        """Конструктор ридера формата RINEX"""

        super().__init__()
        self.reader = 'RINEX'

    def read(self, filename: str):
        """Метод чтения файлов формата RINEX"""

        self.data = open(filename, 'r').read().split('\n')  # ОГО
        for _ in range(4):
            self.data.pop(0)
        self.data.pop(-1)

        # сразу по спутникам разбиваем данные чтоб сильно потом с этим не париться
        counter = 1
        split_by_satellite_data = []
        new_text = ''
        for line in self.data:
            line = line.replace('D', 'e')
            if counter != 8:
                new_text += line + '\n'
                counter += 1
            else:
                counter = 1
                new_text += line + '\n'
                split_by_satellite_data.append(new_text)
                new_text = ''

        self.data = split_by_satellite_data
        # print(self.data[2])  # отладка вручную еу


class SP3Reader(AReader):
    """Класс ридера формата SP3"""

    def __init__(self):
        """Конструктор ридера формата SP3"""

        super().__init__()
        self.reader = 'SP3'

    def read(self, filename: str):
        """Метод чтения файлов формата SP3"""

        self.data = open(filename, 'r').read().split('\n')  # ОГО
        for _ in range(22):
            self.data.pop(0)
        self.data.pop(-1)  # это для кэжуал 'EOF' впаянного в самом конце
        self.data.pop(-1)  # а это для пустой строки после EOF (вы там накуренные что ли сидите?)

        # сразу разбиваем данные чтоб сильно потом с этим не париться, только теперь по дате
        split_by_date_data = []
        new_text = ''
        for line in self.data:
            if not ('*' in line):
                new_text += line + '\n'
            else:
                split_by_date_data.append(new_text)
                new_text = line + '\n'

        split_by_date_data.pop(0)
        self.data = split_by_date_data
        # print(self.data[0])  # отлад0чка


class Analysis:
    """Класс для анализа данных"""

    def __init__(self):
        """Конструктор анализатора"""

        # формат данных будет короче [номер спутника, [время], [x], [y], [z]]
        self.data = None
        self.reader = None

    def load(self, num_ns, type_ns, td, graphs=True):  # я хз че такое td (точно не Tower Defence), поэтому td = data
        """Метод для загрузки данных и построения графиков"""

        if type_ns == 'GPS':
            self.reader = RINEXAdapter()
        elif type_ns == 'GLONASS':
            self.reader = SP3Adapter()
        else:
            raise ValueError('Unsupported GNSS type or typo')  # на ангельском ошибки потому что я так сказал

        self.reader.calc(td)
        time = []
        x_data = []
        y_data = []
        z_data = []
        for item in self.reader.data:
            if num_ns == item[1]:
                time.append(item[0])
                x_data.append(item[2])
                y_data.append(item[3])
                z_data.append(item[4])

        # спутников 6, 10 и 23 вообще типа не существует. пропили.
        if time == x_data == y_data == z_data == []:
            print(x_data)
            print(y_data)
            print(z_data)
            raise ValueError(f'Sattelite no. {num_ns} does not exist')

        self.data = [num_ns, time, x_data, y_data, z_data]

        if graphs:
            # можно было построить графики с помощью метода в классе, но у нас структура регламентирована емое
            x0 = x_data[0]
            y0 = y_data[0]
            z0 = z_data[0]
            ax = plt.figure().add_subplot(projection='3d')

            ax.scatter(0, 0, 0, color='green', s=6400)  # ПЛАНЕТА

            # ax.scatter(0, 0, 0, color='black')
            # ax.text(0, 0, 0, 'earth center', color='black')

            ax.scatter(x0, y0, z0, color='red')
            ax.text(x0, y0, z0, 'start', color='red')
            ax.plot(x_data, y_data, z_data, color='blue', markersize=0.5)

            ax.set_xlabel('x, km')
            ax.set_ylabel('y, km')
            ax.set_zlabel('z, km')
            plt.show()


def main():
    rinex_file = 'Brdc0880.24n'
    sp3_file = 'Sta23074.sp3.glo'
    analysist = Analysis()

    analysist.load(5, 'GPS', rinex_file)
    # analysist.load(4, 'GLONASS', sp3_file)


if __name__ == '__main__':
    main()
