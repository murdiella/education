import numpy as np
from pyrtcm import RTCMReader
import pyproj


class Acceptor:
    """Класс, реализующий вычисление координат принимающего устройства"""

    def __init__(self):
        """Конструктор класса"""
        self.P = np.array([0, 0, 0, 0])  # x y z с начальным приближением равным 0, метры
        self.dpr = 0  # погрешность часов передатчика, мкс (после в с)

    def set_P(self, dP):
        """Функция, обновляющая вектор состояния"""
        # return np.subtract(self.P, dP)
        self.P = self.P + dP

    def get_ro_0(self, data_line):
        """Функция получения априорного расстояния до спутника"""
        return np.sqrt((data_line[0] - self.P[0]) ** 2 + (data_line[1] - self.P[1]) ** 2 + (data_line[2] - self.P[2]) ** 2)

    def get_V(self, data):
        """Функция рассчета вектора невязок"""
        c = 299792458  # скорость света, м/с
        V = np.array([])
        for i in range(len(data)):
            V = np.append(V, (data[i][4] - self.get_ro_0(data[i]) + c * data[i][3] * 1e-6))
        return V

    def get_H(self, data):
        """Функция рассчета матрицы H"""
        line = []
        H = np.empty((0, 4))
        for i in range(len(data)):
            ro_i = self.get_ro_0(data[i])
            line.append((self.P[0] - data[i][0]) / ro_i)
            line.append((self.P[1] - data[i][1]) / ro_i)
            line.append((self.P[2] - data[i][2]) / ro_i)
            line.append(1)
            H = np.vstack([H, line])
            line = []
        return H

    def mnk(self, inputs):
        """Функция, реализующая МНК по набору данных"""
        data = np.array(inputs)
        dP = np.array([1, 1, 1, 1])  # начальное приближение
        while abs(dP[0]) > 0.1 and abs(dP[1]) > 0.1 and abs(dP[2]) > 0.1:
            H = self.get_H(data)
            V = self.get_V(data)
            HtH = np.matmul(np.transpose(H), H)
            HtHinvHt = np.matmul(np.linalg.inv(HtH), np.transpose(H))
            dP = np.matmul(HtHinvHt, V)
            # print(dP)
            # print('\n')
            self.set_P(dP)

        real = self.P
        print(f'real = {self.P}')
        print(f'rad = {np.sqrt(self.P[0] ** 2 + self.P[1] ** 2 + self.P[2] ** 2)}')
        return real


def ephemeris(ephs):
    """Функция, извлекающая эфимириды спутников"""
    coords = []
    bin1019 = open(ephs, "rb").read()
    bininfo1019 = [bin1019[i:i + 67] for i in range(0, len(bin1019), 67)]
    for i in bininfo1019:
        data = RTCMReader.parse(i)

        tk = -10
        a = data.DF092 ** 2  # 1

        mu = 3.9860050e14  # 2
        deln = data.DF087
        n = np.sqrt(mu / (a ** 3)) + deln

        M0 = data.DF088 * 3.1415926535898  # 3
        M = M0 + tk * n

        e = data.DF090 * 2 ** -33  # 4
        def Ei(E_input):
            return M + e * np.sin(E_input)
        E = M
        for _ in range(3):
            E = Ei(E)

        nu = np.arctan2(np.sin(E) * np.sqrt(1 - e**2), np.cos(E) - e)  # 5

        w = data.DF099 * 3.1415926535898  # 6
        u = nu + w

        sin2u = np.sin(2 * u)  # 7
        cos2u = np.cos(2 * u)

        crs = data.DF086  # 8
        crc = data.DF098
        r = a * (1 - e * np.cos(E)) + crs * sin2u + crc * cos2u

        i0 = data.DF097 * 3.1415926535898  # 9
        idot = data.DF079 * 3.1415926535898
        cis = data.DF096
        cic = data.DF094
        i = i0 + idot * tk + cis * sin2u + cic * cos2u

        cus = data.DF091  # 10
        cuc = data.DF089
        u += cus * sin2u + cuc * cos2u

        xs = r * np.cos(u)  # 11
        ys = r * np.sin(u)

        omega_0 = data.DF095 * 3.1415926535898  # 12
        OMGd = data.DF100 * 3.1415926535898
        OMGE = 7.2921151467E-5
        omega = omega_0 + OMGd * tk - OMGE * tk

        sin_omega = np.sin(omega)  # 13
        cos_omega = np.cos(omega)

        x_ecef = xs * cos_omega - ys * np.cos(i) * sin_omega  # 14
        y_ecef = xs * sin_omega + ys * np.cos(i) * cos_omega
        z_ecef = ys * np.sin(i)
        coords.append([x_ecef, y_ecef, z_ecef])
        # print(x_ecef, y_ecef, z_ecef)

    return coords


def pseudodistance_parser(pseudos, coords):
    """Функция, создающая готовый набор данных для МНК по полученным координатам спутников и их измерениям"""
    with open(pseudos, 'rb') as file:
        f = file.read()
        data = RTCMReader.parse(f)
    print(data)
    parsed_array = []
    parsed_array.append(coords[0] + [data.DF013_01, data.DF011_01])
    parsed_array.append(coords[1] + [data.DF013_02, data.DF011_02])
    parsed_array.append(coords[2] + [data.DF013_03, data.DF011_03])
    parsed_array.append(coords[3] + [data.DF013_04, data.DF011_04])
    parsed_array.append(coords[4] + [data.DF013_05, data.DF011_05])
    parsed_array.append(coords[5] + [data.DF013_06, data.DF011_06])
    return parsed_array


def main():
    ephs = '1019.rtcm'
    pseudos = '1002.rtcm'

    sat_coords = ephemeris(ephs)
    sat_parsed_data = pseudodistance_parser(pseudos, sat_coords)
    # for item in sat_parsed_data:
    #     print(item)

    thing = Acceptor()
    ecef = thing.mnk(sat_parsed_data)

    transformer = pyproj.Transformer.from_crs({"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
                                              {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},)
    lon, lat, alt = transformer.transform(ecef[0], ecef[1], ecef[2], radians=False)  # долгота, широта, высота
    print(f'Долгота = {lon} град.\nШирота = {lat} град.')
    print(f'Высота = {alt}')


if __name__ == "__main__":
    main()
