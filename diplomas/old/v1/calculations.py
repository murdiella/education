"""Основной рассчетный модуль"""

import numpy as np
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
import time


class Calc:
    """Класс, выполняющий основные вычисления критериев и т.п."""

    def __init__(self, req, t: int, steps: int = 10):
        """Метод-конструктор экземпляра класса для расчетов
        Ввод: request: Request - экземпляр класса Request
              t: int - время операции, сек
              steps: int = 10 - количество значений на интервале [min, max]
        Вывод: None"""

        if not isinstance(req, Request):
            raise ValueError('Ввод должен содержать экземпляр класса Request')

        self._obj = req
        # массивы всех значений к перебору. для целочисленных с шагом 1, для плавающих точек разбивка на steps шагов
        self.targets = req.targets_count  # не варьируется
        self.nums = np.linspace(req.ucavs_min, req.ucavs_max, req.ucavs_max - req.ucavs_min + 1)
        self.thetas = np.linspace(req.theta_min, req.theta_max, steps)
        self.lambdas = np.linspace(req.lambda_min, req.lambda_max, steps)
        self.mus = np.linspace(req.mu_min, req.mu_max, steps)
        self.p = req.kill_prob  # не варьируется
        self.t = t

        # массив из значений для каждой точки
        # будет содержать подмассивы вида [координата точки, значение критерия 1, значение критерия 2]
        self.values = []

    def _scalar(self, theta: float, lambda_: float, mu: float, num: int, a1: float, a2: float) -> float:
        """Метод, реализующий поиск решения на основе скалярной свертки критериев
        Ввод: theta, lambda_, mu: float -- текущие значения соответствующих параметров
              num: int -- текущее число БЛА
              a1, a2: float -- значения весовых коэффициентов для критерия 1 и критерия 2 соответственно, притом
              положительные и дающие в сумме 1
        Вывод: float -- значение критерия для точки"""

        n1 = self._obj.crit1(self.t, theta, lambda_, mu, num)
        n2 = self._obj.crit2(self.t, theta, lambda_, mu, self.p, num, self.targets)

        if a1 > 0 and a2 > 0 and np.isclose(a1 + a2, 1):
            if n1 is not None and n2 is not None:
                return a1 * n1 - a2 * n2
            else:
                raise ValueError('Один из критериев не считается')
        else:
            raise ValueError('Неверные значения коэффициентов при критериях')

    def _target(self, theta: float, lambda_: float, mu: float, num: int) -> float:
        """Метод, реализующий поиск решения на основе прицельной точки
            Ввод: theta, lambda_, mu: float -- текущие значения соответствующих параметров
                  num: int -- текущее число БЛА
            Вывод: float -- значение критерия для точки"""

        n1 = self._obj.crit1(self.t, theta, lambda_, mu, num)
        n2 = self._obj.crit2(self.t, theta, lambda_, mu, self.p, num, self.targets)

        if n1 is not None and n2 is not None:
            return n1 ** 2 + (n2 - self.targets) ** 2
        else:
            raise ValueError('Один из критериев не считается')

    def overkill(self, method: str, a1: float = 0.5, a2: float = 0.5, background: bool = False, rounded: bool = True):
        """Метод, реализующий подбор решения перебором
        Ввод:
        Вывод:"""

        if not (a1 > 0 and a2 > 0 and np.isclose(a1 + a2, 1)):
            raise ValueError('Неверные значения коэффициентов при критериях')

        skipcount = 0
        count = 0
        min_crit = None
        params = None
        output = False
        graph = False
        n1s = []  # x -- МО упавших БЛА
        n2s = []  # y -- МО количества пораженных целей
        labels = []  # массив для подписей под график

        # собственно, перебор значений
        for th in self.thetas:
            for la in self.lambdas:
                for mu in self.mus:
                    for n in self.nums:

                        match method.upper():
                            case 'SCALAR':
                                output = True
                                try:
                                    count += 1
                                    val = self._scalar(th, la, mu, n, a1, a2)
                                    if min_crit is not None:
                                        if val < min_crit:
                                            min_crit = val
                                            params = [th, la, mu, n]
                                    else:
                                        min_crit = val
                                        params = [th, la, mu, n]
                                except ValueError:
                                    # print(th, la, mu, n)
                                    skipcount += 1
                                    pass

                            case 'TARGET':
                                output = True
                                try:
                                    count += 1
                                    val = self._target(th, la, mu, n)
                                    if min_crit is not None:
                                        if val < min_crit:
                                            min_crit = val
                                            params = [th, la, mu, n]
                                    else:
                                        min_crit = val
                                        params = [th, la, mu, n]
                                except ValueError:
                                    # print(th, la, mu, n)
                                    skipcount += 1
                                    pass

                            case 'PARETO':
                                graph = True
                                try:
                                    count += 1
                                    n1 = self._obj.crit1(self.t, th, la, mu, n)
                                    n2 = self._obj.crit2(self.t, th, la, mu, self.p, n, self.targets)
                                    if n1 is not None and n2 is not None:
                                        n1s.append(n1)
                                        n2s.append(n2)
                                        labels.append(f't{round(th, 3)}l{round(la, 3)}m{round(mu, 3)}n{n}')
                                    else:
                                        skipcount += 1
                                        break
                                except ValueError:
                                    # print(th, la, mu, n)
                                    skipcount += 1
                                    pass

                            case _:
                                raise ValueError('Данный алгоритм не предусмотрен программой')

        if background:
            print(f'Всего {count} комбинаций')
            print(f'Пропущено {skipcount} комбинаций')
            if graph:
                print(f'Отрисовано {len(n1s)} точек\n')

        if graph:
            ax = plt.figure().add_subplot()

            if not rounded:
                ax.scatter(n1s, n2s)
            else:
                n1s_out = [round(x) for x in n1s]
                n2s_out = [round(x) for x in n2s]
                ax.scatter(n1s_out, n2s_out)

            ax.scatter(0, self.targets)

            ax.text(0, self.targets, 'Прицельная точка')

            ax.set_title('Множество Парето')
            ax.set_xlabel('N1')
            ax.set_ylabel('N2')
            plt.show()

        if output:
            return min_crit, params


class Request(metaclass=ABCMeta):
    """Класс, формирующий запрос на подачу для рассчета критериев"""

    def __init__(self, m: int, n_min: int, n_max: int, t1_min: float, t1_max: float, t2_min: float, t2_max: float,
                 t3_min: float, t3_max: float, p: float):
        """Метод-конструктор экземпляра любого из "потомков" класса
        Ввод: m: int - предполагаемое число целей в целевой области, ед.
              n_min, n_max: int - диапазон количества БЛА, участвующих в операции, сек
              t1_min, t1_max: float - диапазон дня среднего времени сохранения работоспособности, сек
              t2_min, t2_max: float - диапазон среднего времени обнаружения цели, сек
              t3_min, t3_max: float - диапазон среднего времени поражения обнаруженной цели, сек
              p: float - вероятность поражения обнаруженной идентифицированной цели, сек
        Вывод: None"""

        try:
            self.targets_count = m  # число целей
            self.ucavs_min = n_min  # UCAV это Unmanned Combat Aerial Vehicle - Боевой БЛА
            self.ucavs_max = n_max
            self.theta_max = 1 / t1_min  # несколько параметров для расчетов критериев
            self.theta_min = 1 / t1_max
            self.lambda_max = 1 / t2_min
            self.lambda_min = 1 / t2_max
            self.mu_max = 1 / t3_min
            self.mu_min = 1 / t3_max
        except TypeError:
            raise TypeError('Неверный тип вводных данных (см. help(Request.__init__))')
        if 0. < p < 1.:  # без точек ругает за плохие операции с булями
            self.kill_prob = p  # вероятность поразить цель
        else:
            raise ValueError('Неверно задана вероятность поражения цели')

    @abstractmethod
    def crit1(self, t: int, theta: float, lambda_: float, mu: float, n: int):
        """Метод, выполняющий расчет критерия 1 -- математического ожидания числа БЛА,
        которые будут потеряны к моменту времени t
        Ввод: t - момент времени, сек
              theta, lambda_, mu - значения соответствующих параметров
              n: int - число БЛА
        Вывод: float - значение критерия """
        pass

    @abstractmethod
    def crit2(self, t: int, theta: float, lambda_: float, mu: float, p: float, n: int, m: int):
        """Метод, выполняющий расчет критерия 2 -- математического ожидания числа целей,
        которые будут уничтожены к моменту времени t
        Ввод: t - момент времени, сек
              theta, lambda_, mu - значения соответствующих параметров
        Вывод: float - значение критерия """
        pass


class Standard(Request):
    """Класс, формирующий запрос на подачу для рассчета критериев стандартного БПЛА"""

    def __init__(self, m: int, n_min: int, n_max: int, t1_min: float, t1_max: float, t2_min: float, t2_max: float,
                 t3_min: float, t3_max: float, p: float):
        """Метод-конструктор экземпляра классического простейшего экземпляра БЛА
        Ввод/вывод: см. help(Request.__init__)"""

        super().__init__(m, n_min, n_max, t1_min, t1_max, t2_min, t2_max, t3_min, t3_max, p)

    @staticmethod
    def _p1(t: int, theta: float, lambda_: float, mu: float) -> float:
        """Метод, выполняющий расчет вероятности потери БЛА к моменту времени t
        Ввод: t - момент времени, сек
              theta, lambda_, mu - значения соответствующих параметров
        Вывод: float - значение критерия """

        if lambda_ != mu:
            p = (lambda_ * theta / (mu + theta) * (((1 - np.exp(-(lambda_ + theta) * t)) / lambda_ + theta)
                                                   - ((1 - np.exp(-(mu + theta) * t)) / (lambda_ - mu)))
                 + theta / (lambda_ + theta) * (1 - np.exp(-(lambda_ + theta) * t)))
        else:
            p = (lambda_ * theta / (mu + theta) * (((1 - np.exp(-(lambda_ + theta) * t)) / lambda_ + theta)
                                                   - (t * np.exp(-(lambda_ + theta) * t)))
                 + theta / (lambda_ + theta) * (1 - np.exp(-(lambda_ + theta) * t)))
        if 0. <= p <= 1.:
            return p
        else:
            raise ValueError('Вероятность p1 вне своего диапазона')

    @staticmethod
    def _p2(t: int, theta: float, lambda_: float, mu: float) -> float:
        """Метод, выполняющий расчет вероятности потери БЛА к моменту времени t
        Ввод: t - момент времени, сек
              theta, lambda_, mu - значения соответствующих параметров
        Вывод: float - значение критерия """

        if lambda_ != mu:
            p = (lambda_ * mu / (mu + theta)) * (((1 - np.exp(-(lambda_ + theta) * t)) / (lambda_ + theta))
                                                 - ((np.exp(-(mu + theta) * t)) * (1 - np.exp(-(lambda_ - mu) * t)))
                                                 / (lambda_ - mu))
        else:
            p = (lambda_ * mu / (mu + theta)) * (((1 - np.exp(-(lambda_ + theta) * t)) / (lambda_ + theta))
                                                 - (t * np.exp(-(lambda_ + theta) * t)))
        if 0. <= p <= 1.:
            return p
        else:
            raise ValueError('Вероятность p2 вне своего диапазона')

    def crit1(self, t: int, theta: float, lambda_: float, mu: float, n: int) -> float:
        """Метод, выполняющий расчет критерия 1 -- математического ожидания числа БЛА,
        которые будут потеряны к моменту времени t
        Ввод/вывод: см. help(Request._crit1)"""

        return self._p1(t, theta, lambda_, mu) * n

    def crit2(self, t: int, theta: float, lambda_: float, mu: float, p: float, n: int, m: int) -> float:
        """Метод, выполняющий расчет критерия 2 -- математического ожидания числа целей,
        которые будут уничтожены к моменту времени t
        Ввод/вывод: см. help(Request._crit2)"""

        return m * (1 - (1 - self._p2(t, theta, lambda_, mu) * p / m) ** n)


def main():
    """Основная исполняющая функция"""
    start = time.time()  # для слежения за быстродействием
    np.seterr(all='ignore')  # игнорируем варнинги

    # в статье приведены значения theta = 0.01 ~ t1 = 100, lambda_ = 0.2 ~ t2 = 5, mu = 2 ~ t3 = 0.5
    t = 300  # время операции
    m = 7  # число целей
    n_min = 4  # число БЛА
    n_max = 12
    t1_min = 80  # позже theta
    t1_max = 1200
    t2_min = 3  # позже lambda
    t2_max = 100
    t3_min = 0.2  # позже mu
    t3_max = 1
    p = 0.7  # вероятность поражения
    s = 10
    std = Standard(m, n_min, n_max, t1_min, t1_max, t2_min, t2_max, t3_min, t3_max, p)
    calc = Calc(std, t, steps=s)

    bck = False
    rnd = True

    # для демонтрации скалярной свертки критериев
    min_, params = calc.overkill('scalar', background=bck, rounded=rnd)
    print(f'Скалярная свертка критериев. Минимум критерия = {min_}')
    print(f'Параметры: theta = {params[0]}, lambda = {params[1]}, mu = {params[2]}, n = {params[3]}\n')

    # для демонстрации метода с прицельной точкой
    min_, params = calc.overkill('target', background=bck, rounded=rnd)
    print(f'Метод прицельной точки. Минимум критерия = {round(min_)} ({min_})')
    print(f'Параметры: theta = {params[0]}, lambda = {params[1]}, mu = {params[2]}, n = {params[3]}\n')

    # для демонстрации множества Парето
    calc.overkill('pareto', background=bck, rounded=rnd)

    print(f'Время выполнения: {time.time() - start} секунд')


# во избежание лишних запусков при подключении
if __name__ == '__main__':
    main()
