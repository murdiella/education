import my_matrix_package as mp
import model as mo


# задача Аренсторфа (нач. условия 1)
class TArenstorfModel1(mo.Model):
    _m = float

    def __init__(self, _t0, _t1, _sampling_increment):
        super().__init__()
        self._m = 0.012277471
        self._x0 = mp.TVector([0, 0, 0, 0])
        self._x0[0] = 0.994
        self._x0[1] = 0
        self._x0[2] = 0
        self._x0[3] = -2.00158510637908252240537862224

    # функция правых частей ДУ
    def get_right(self, X, t):
        y = mp.TVector([0, 0, 0, 0])
        d1 = pow((pow((self._x0[0] - self._m), 2) + pow((self._x0[1] - self._m), 2)), 3/2)
        d2 = pow((pow((self._x0[0] - (1 - self._m)), 2) + pow((self._x0[1] - (1 - self._m)), 2)), 3/2)
        y[0] = self._x0[0]
        y[1] = self._x0[0]
        y[2] = self._x0[0] + 2 * y[1] - (1 - self._m) * (self._x0[0] + self._m) / d1 - self._m * (self._x0[0] + (1 - self._m)) / d2
        y[3] = self._x0[1] - 2 * y[0] - ((1 - self._m) * self._x0[1]) / d1 - (self._m*self._x0[1]) / d2
        return y


# задача Аренсторфа (нач. условия 2)
class TArenstorfModel2(mo.Model):
    _m = float

    def __init__(self, _t0, _t1, _sampling_increment):
        super().__init__()
        self._m = 0.012277471
        self._x0 = mp.TVector([0, 0, 0, 0])
        self._x0[0] = 0.994
        self._x0[1] = 0
        self._x0[2] = 0
        self._x0[3] = -2.0317326295573368357302057924

    # функция правых частей ДУ
    def get_right(self, X, t):
        y = mp.TVector([0, 0, 0, 0])
        d1 = pow((pow((self._x0[0] - self._m), 2) + pow((self._x0[1] - self._m), 2)), 3 / 2)
        d2 = pow((pow((self._x0[0] - (1 - self._m)), 2) + pow((self._x0[1] - (1 - self._m)), 2)), 3 / 2)
        y[0] = self._x0[0]
        y[1] = self._x0[0]
        y[2] = self._x0[0] + 2 * y[1] - (1 - self._m) * (self._x0[0] + self._m) / d1 - self._m * (
                    self._x0[0] + (1 - self._m)) / d2
        y[3] = self._x0[1] - 2 * y[0] - ((1 - self._m) * self._x0[1]) / d1 - (self._m * self._x0[1]) / d2
        return y
