import numpy as np


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
            print(dP)
            print('\n')
            self.set_P(dP)

        print(f'real = {self.P}')
        print(f'rad = {np.sqrt(self.P[0] ** 2 + self.P[1] ** 2 + self.P[2] ** 2)}')


def main():
    data = [[16678843, -2634637, 20579559, -50.014071, 21293946],
            [13020628, -12527567, 19099436, -148.368549, 22744995],
            [-2555568, 16762578, 20311833, 526.543696, 21565628],
            [16181563, -957262, 21758956, 53.373334, 21513278],
            [-1405082, 15628413, 21394716, 78.206308, 21488700],
            [20637508, 8906797, 14267852, -409.011384, 21246116]]

    thing = Acceptor()
    thing.mnk(data)


if __name__ == '__main__':
    main()
