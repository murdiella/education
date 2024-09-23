import my_matrix_package as mp


# класс модели
class Model:
    # _x это protected
    _x0 = mp.TVector  # начальные условия
    _sampling_increment = float  # требуемый интервал выдачи результатов
    _t0 = float  # начало интегрирования
    _t1 = float  # конец интегрирования
    _result = mp.TMatrix  # результат интегрирования
    _n = int  # счетчик строк в матрице результатов

    # конструктор объекта класса (включая значения по умолчанию)
    def __init__(self, f_samp_inc=0.1, f_t0=0, f_t1=1, f_n=0):
        self._sampling_increment = f_samp_inc
        self._t0 = f_t0
        self._t1 = f_t1
        self._n = f_n

    # получение интервала выдачи результата
    def get_samp_inc(self):
        return self._sampling_increment

    def get_init_cond(self):
        return self._x0

    # порядок размерности системы т.е. размер вектора состояния
    def get_order(self):
        return self._x0.get_length()

    # получение начальных условий
    def get_x0(self):
        return self._x0

    # управление временным интервалом интегрирования
    def get_t0(self):
        return self._t0

    def get_t1(self):
        return self._t1

    # получение матрицы результатов
    def get_result(self):
        return self._result

    # запись результатов
    def add_result(self, X, t):
        if self._n == self._result.get_row_count():
            self._result.set_size(self._n + 1, self.get_order() + 1)
        self._result[self._n][0] = t
        for i in range(X.get_length(), 1, -1):
            self._result[self._n][i] = X[i - 1]
        self._n += 1

    # очистка результатов
    def clear_result(self):
        self._result.set_size(0, 0)
        self._n = 0

    # подготовка результата под более эффективное выделение памяти
    # зададим такой размер, чтоб поместились все значения вектора состояния и соотв. им моментов времени на интервале
    # [t0, t1] с шагом sampling_increment
    def prep_result(self):
        self._result.set_size(self._result, (self._t1 - self._t0) / self._sampling_increment + 1, self.get_order() + 1)
        # сброс счетчика строк в матрице результатов
        self._n = 0
