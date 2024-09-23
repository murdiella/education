import numpy as np
import matplotlib.pyplot as plt
from utm import from_latlon

g = 9.81  # ускорение свободного падения, без изменений от высоты


class INS:
    """Класс бортовой инерциальной навигационной системы"""

    def __init__(self):
        """Конструктор класса
        Ввод: None
        Вывод: None"""

        # блок параметров акселерометра
        self.__acc_tau = 100  # интервал корреляции шумов
        self.__acc_nonlinearity = np.random.normal(0, 1e-6 * g)  # нелинейность

        self.__acc_scale_error_x = np.random.normal(0, 1e-6 * g)  # ошибка масштабного коэффициента
        self.__acc_scale_error_y = np.random.normal(0, 1e-6 * g)
        self.__acc_scale_error_z = np.random.normal(0, 1e-6 * g)

        # вариант 4 -- замена мат. ожидания смещения нуля с 0 на 0.0001 * g, 0.001 * g, 0.01 * g (параметр loc)
        self.__acc_zero_bias_x = np.random.normal(0, 1e-6 * g)  # смещение ноля
        self.__acc_zero_bias_y = np.random.normal(0, 1e-6 * g)
        self.__acc_zero_bias_z = np.random.normal(0, 1e-6 * g)

        self.__acc_noise_rms_x = np.random.normal(0, 1e-6 * g)  # ско шумов
        self.__acc_noise_rms_y = np.random.normal(0, 1e-6 * g)
        self.__acc_noise_rms_z = np.random.normal(0, 1e-6 * g)

        self.__acc_noise_x = np.random.normal(0, self.__acc_noise_rms_x ** 2 / self.__acc_tau)  # шумы
        self.__acc_noise_y = np.random.normal(0, self.__acc_noise_rms_y ** 2 / self.__acc_tau)
        self.__acc_noise_z = np.random.normal(0, self.__acc_noise_rms_z ** 2 / self.__acc_tau)

        # блок параметров гироскопа
        self.__gyro_tau = 10  # интервал корреляции шумов
        self.__gyro_nonlinearity = np.random.normal(0, 1e-6 * g)  # нелинейность

        self.__gyro_scale_error_x = np.random.normal(0, 1e-6 * g)  # ошибка масштабного коэффициента
        self.__gyro_scale_error_y = np.random.normal(0, 1e-6 * g)
        self.__gyro_scale_error_z = np.random.normal(0, 1e-6 * g)

        self.__gyro_acc_influence_x = np.random.normal(0, 1e-6 * g)  # ошибка влияния линейных ускорений
        self.__gyro_acc_influence_y = np.random.normal(0, 1e-6 * g)
        self.__gyro_acc_influence_z = np.random.normal(0, 1e-6 * g)

        self.__gyro_noise_rms_x = np.random.normal(0, 1e-6 * g)  # ско шумов
        self.__gyro_noise_rms_y = np.random.normal(0, 1e-6 * g)
        self.__gyro_noise_rms_z = np.random.normal(0, 1e-6 * g)

        self.__gyro_noise_x = np.random.normal(0, self.__gyro_noise_rms_x ** 2 / self.__gyro_tau)  # шумы
        self.__gyro_noise_y = np.random.normal(0, self.__gyro_noise_rms_y ** 2 / self.__gyro_tau)
        self.__gyro_noise_z = np.random.normal(0, self.__gyro_noise_rms_z ** 2 / self.__gyro_tau)

    def __acc_noises(self, rms):
        """Класс для симуляции шумов акселерометра
        Ввод: СКО шумов на оси (собственный параметр)
        Вывод: значение шума на шаге"""

        if rms is self.__acc_noise_rms_x:
            self.__acc_noise_x = self.__acc_noise_x + np.sqrt(2) * self.__acc_noise_rms_x * np.random.normal(0, 1)
            return self.__acc_noise_x
        elif rms is self.__acc_noise_rms_y:
            self.__acc_noise_y = self.__acc_noise_y + np.sqrt(2) * self.__acc_noise_rms_y * np.random.normal(0, 1)
            return self.__acc_noise_y
        elif rms is self.__acc_noise_rms_z:
            self.__acc_noise_z = self.__acc_noise_z + np.sqrt(2) * self.__acc_noise_rms_z * np.random.normal(0, 1)
            return self.__acc_noise_z
        else:
            raise ValueError('Несуществующий параметр СКО шумов')

    def get_acc_measures(self, x: np.array):
        """Класс для снятия измерений акселерометра
        Ввод: x: np.ndarray - вектор истинных ускорений
        Вывод: np.ndarray - вектор измеренных ускорений"""

        if np.shape(x) == (3, ):
            return x + np.array([
                self.__acc_nonlinearity * x[0] ** 2 + self.__acc_scale_error_x * x[0] + self.__acc_zero_bias_x * x[0]
                + self.__acc_noises(self.__acc_noise_rms_x),
                self.__acc_nonlinearity * x[1] ** 2 + self.__acc_scale_error_y * x[1] + self.__acc_zero_bias_y * x[1]
                + self.__acc_noises(self.__acc_noise_rms_y),
                self.__acc_nonlinearity * x[2] ** 2 + self.__acc_scale_error_z * x[2] + self.__acc_zero_bias_z * x[2]
                + self.__acc_noises(self.__acc_noise_rms_z)
                ])
        else:
            raise ValueError('Неверный размер входного вектора ускорений')

    def __gyro_noises(self, rms):
        """Класс для симуляции шумов гироскопа
        Ввод: СКО шумов на оси (собственный параметр)
        Вывод: значение шума на шаге"""

        if rms is self.__gyro_noise_rms_x:
            self.__gyro_noise_x = self.__gyro_noise_x + np.sqrt(2) * self.__gyro_noise_rms_x * np.random.normal(0, 1)
            return self.__gyro_noise_x
        elif rms is self.__gyro_noise_rms_y:
            self.__gyro_noise_y = self.__gyro_noise_y + np.sqrt(2) * self.__gyro_noise_rms_y * np.random.normal(0, 1)
            return self.__gyro_noise_y
        elif rms is self.__gyro_noise_rms_z:
            self.__gyro_noise_z = self.__gyro_noise_z + np.sqrt(2) * self.__gyro_noise_rms_z * np.random.normal(0, 1)
            return self.__gyro_noise_z
        else:
            raise ValueError('Несуществующий параметр СКО шумов')

    def get_gyro_measures(self, a: np.array, omega: np.array):
        """Класс для снятия измерений гироскопа
        Ввод: a: np.ndarray - вектор истинных ускорений, omega: np.array - вектор истинных угловых скоростей
        Вывод: np.ndarray - вектор измеренных угловых скоростей"""

        if np.shape(a) == (3, ) and np.shape(omega) == (3, ):
            return omega + np.array([
                self.__gyro_scale_error_x * omega[0] + self.__gyro_scale_error_x * omega[0] ** 2
                + self.__gyro_acc_influence_x * a[0] + self.__gyro_acc_influence_x * a[0] ** 2
                + self.__gyro_noises(self.__gyro_noise_rms_x),
                self.__gyro_scale_error_y * omega[1] + self.__gyro_scale_error_y * omega[1] ** 2
                + self.__gyro_acc_influence_y * a[1] + self.__gyro_acc_influence_y * a[1] ** 2
                + self.__gyro_noises(self.__gyro_noise_rms_y),
                self.__gyro_scale_error_z * omega[2] + self.__gyro_scale_error_z * omega[2] ** 2
                + self.__gyro_acc_influence_z * a[2] + self.__gyro_acc_influence_z * a[2] ** 2
                + self.__gyro_noises(self.__gyro_noise_rms_z)
                ])
        else:
            raise ValueError('Неверный размер входного вектора угловых скоростей или линейных ускорений')


class LAX:
    """Класс, содержащий модель движения ЛА"""

    def __init__(self, r_g: np.ndarray = np.array([0, 0, 0]), v_g: np.ndarray = np.array([0, 0, 0]),
                 angles: np.ndarray = np.array([0, 0, 0]), dt=0.1):
        """Конструктор класса
        ввод: r_g: np.ndarray - начальный вектор оценок положения ЛА в ЗССК,
              v_g: np.ndarray - начальный вектор оценок скоростей ЛА в ЗССК
        вывод: None"""

        self.__dt = dt  # временной шаг
        self.__ins = INS()

        # начальные приближения
        [x, y, _, _] = from_latlon(r_g[0], r_g[1])
        self._r_g = np.array([x, y, r_g[2]])   # вектор оценок положения ЛА в ЗССК
        self._v_g = v_g  # вектор оценок скорости ЛА в ЗССК
        self.__n_g = np.array([0, 0, 0])  # вектор кажущегося ускорения ЛА в ЗССК
        self.__eulers = angles  # вектор углового положения ЛА в ЗССК (углы Эйлера)
        self.__u = np.array([0, 0, 7.292e-5])  # вектор угловой скорости вращения Земли в ЗССК
        self.__g = np.array([0, 0, -g])  # вектор проекций ускорения свободного падения на оси ЗССК
        self.__n_acs = np.array([0, 0, 0])  # вектор измерений ускорений акселерометром в ССК
        self.__mat = self.__pa_to_ecs()  # матрица перехода М, начальное приближение

    def __pa_to_ecs(self):
        """Метод перевода из СК ЛА в ЗССК
        ввод: eulers: np.ndarray - вектор углов Эйлера
        вывод: np.ndarray - матрица поворота/перехода"""
        # https://en.wikipedia.org/wiki/Rotation_matrix#General_3D_rotations
        a = self.__eulers[0]  # phi ~ alpha
        b = self.__eulers[1]  # theta ~ beta
        ga = self.__eulers[2]  # gamma ~ gamma
        return np.array([
            [np.cos(a) * np.cos(b), np.cos(a) * np.sin(b) * np.sin(ga) - np.sin(a) * np.cos(ga),
             np.cos(a) * np.sin(b) * np.cos(ga) + np.sin(a) * np.sin(ga)],
            [np.sin(a) * np.cos(b), np.sin(a) * np.sin(b) * np.sin(ga) + np.cos(a) * np.cos(ga),
             np.sin(a) * np.sin(b) * np.cos(ga) - np.cos(a) * np.sin(ga)],
            [-np.sin(b), np.cos(b) * np.sin(ga), np.cos(b) * np.cos(ga)]
        ])

    def __screw_matrix(self, omega: np.ndarray):
        """Метод, содержащий кососиметрическую матрицу (screw matrix)
        ввод: omega: np.ndarray - вектор измерений с ДУС угловых скоростей ЛА
        вывод: np.ndarray - кососиметричная матрица M (screw matrix)"""
        if np.shape(omega) == (3, ):
            gamma = omega - self.__u
            return np.array([
                [0, -gamma[2], gamma[1]],
                [gamma[2], 0, -gamma[0]],
                [-gamma[1], gamma[0], 0]
            ])
        else:
            raise ValueError('Неверный размер вектора измерений угловых скоростей ЛА')

    def __make_n_g(self, a: np.ndarray):
        """Метод, содержащий вычисление вектора кажущегося ускорения ЛА в ЗССК (Ng)
        ввод: a: np.ndarray - вектор измерений с акселерпометра ускорений ЛА
        вывод: np.array - вектор кажущихся ускорений ЛА в ЗССК"""
        if np.shape(a) == (3, ):
            return np.dot(self.__mat.T, a)
        else:
            raise ValueError('Неверный размер вектора измерений ускорений ЛА')

    def dynamics_step(self, a: np.ndarray, omega: np.ndarray):
        """Метод, содержащий динамическую систему ЛА
        ввод: a: np.ndarray - вектор истинных ускорений, omega: np.array - вектор истинных угловых скоростей
        вывод:"""
        if np.shape(a) == (3,) and np.shape(omega) == (3, ):
            eu = Integrator(self.__dt)
            a = self.__ins.get_acc_measures(a)
            omega = self.__ins.get_gyro_measures(a, omega)

            self.__mat = eu.integrate(-1 * np.multiply(self.__mat, self.__screw_matrix(omega)), self.__mat)
            self.__n_g = self.__make_n_g(a)
            vx_dot = self.__u[0] * self._v_g[1] - self.__u[1] * self._v_g[2] + self.__n_g[0] + self.__g[0]
            vy_dot = -self.__u[2] * self._v_g[0] + self.__u[0] * self._v_g[2] + self.__n_g[1] + self.__g[1]
            vz_dot = self.__u[1] * self._v_g[0] - self.__u[0] * self._v_g[1] + self.__n_g[2] + self.__g[2]
            self._v_g = eu.integrate(np.array([vx_dot, vy_dot, vz_dot]), self._v_g)
            self._r_g = eu.integrate(self._v_g, self._r_g)
        else:
            raise ValueError('Неверный размер вектора ускорений или угловых скоростей')


class Integrator:
    """Класс для создания простейшего интегратора методом Эйлера"""

    def __init__(self, h=0.1):
        """Конструктор класса
        ввод: h - шаг интегрирования
        вывод: None"""

        self.__h = h

    def integrate(self, f, x0=None):
        """Интегратор для одного шага
        Должен использоваться в цикле с вносом новых значений аргументов при эмуляции движения ЛА
        ввод: f - значение аргумента, x0 - начальное положение (по умолчанию нулевой вектор)
        вывод: результат шага интегрирования методом Эйлера"""

        if x0 is None:
            x0 = np.zeros(np.shape(f))
        return x0 + self.__h * f


def main():
    """Основная исполняющая функция"""
    dt = 0.01
    t = round(5 / dt)  # желаемое конечное время в сек указать перед делением

    # начальные условия
    coords_cm = np.array([55, 24, 20000])  # координаты ЦМ ЛА в ЗССК (земная связанная, долгота, широта и высота)]
    velocity_cm = np.array([200, 0, 0])  # скорости ЦМ ЛА в НСК (нормальная земная)
    euler_angles = np.array([0, 0, 0])  # углы эйлера
    la = LAX(coords_cm, velocity_cm, euler_angles)

    # поле боя
    # короткие функции для задавания векторов угловых скоростей и линейных ускорений без особых аннотаций к ним
    def f_a(t):
        return np.array([1, 2.5, g])
        # return np.array([2, 200 * np.sin(t / 100 + 50), g])  # можно всякие функции от t прописывать внутрь

    def f_omega(t):
        return np.array([0, 0, 0])

    coords = []
    for t in range(t):
        la.dynamics_step(f_a(t), f_omega(t))
        coords.append(la._r_g.tolist())  # мы по хорошему переменную la._r_g не должны видеть вне класса
    x = []
    y = []
    z = []
    for item in coords:
        x.append(item[0])
        y.append(item[1])
        z.append(item[2])

    [x0, y0, _, _] = from_latlon(coords_cm[0], coords_cm[1])

    # можно было построить графики с помощью метода в классе, но ограничимся этим
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot(x, y, z, color='blue', markersize=0.5)
    ax.scatter(x0, y0, coords_cm[2], color='red')
    ax.scatter(x0, y0, 0, color='black')
    # надписи содержат какое-то невероятное количество варнингов, но к сожалению так надо
    ax.text(x0, y0, 0,  'floor')
    ax.text(x0, y0, coords_cm[2], 'start', color='red')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

# пример интегрирования ускорений (успешный)
    # movement = []
    # for _ in range(100):
    #     movement.append([0, 0, 100])
    # movement = np.array(movement)
    # x = np.array([0, 0, 0])  # нулевые координаты
    # vx = np.array([0, 0, 0])  # нулевые скорости
    # xs = []
    # for move in movement:
    #     vx = eu.integrate(ac.get_acc_measures(move), vx)
    #     x = eu.integrate(vx, x)
    #     xs.append(x.tolist())
    # print(xs[-1])

    # пример интегрирования угловых скоростей (тоже успешный)
    # movement = []
    # for _ in range(100):
    #     movement.append([0, 0, 100])
    # movement = np.array(movement)
    # x = np.array([0, 0, 0])  # только координаты начальные. у нас таки дус а не аксел
    # xs = []
    # for move in movement:
    #     x = eu.integrate(ac.get_gyro_measures(move, move), x)
    #     xs.append(x.tolist())
    # print(xs[-1])


#  во избежание ненужных запусков кода при подключении модуля в другие проекты:
if __name__ == '__main__':
    main()
