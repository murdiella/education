"""Модуль для тестирования ПО в процессе разработки"""

import unittest as ut
import calculations as cc


class Test(ut.TestCase):
    """Класс для проведения тестирования"""

    def test_std_criterias(self):
        t = 300  # время операции
        m = 7  # число целей
        n_min = 4  # число БЛА
        n_max = 12
        t1_min = 80  # позже theta
        t1_max = 120
        t2_min = 3  # позже lambda
        t2_max = 10
        t3_min = 0.2  # позже mu
        t3_max = 1
        p = 0.7  # вероятность поражения
        std = cc.Standard(m, n_min, n_max, t1_min, t1_max, t2_min, t2_max, t3_min, t3_max, p)

        self.assertEqual(round(std._p1(100, 0.01, 0.1, 0.1), 4), 0.1819)
        self.assertEqual(round(std._p1(100, 0.01, 0.1, 1), 4), 0.1019)
        self.assertEqual(round(std._p2(100, 0.01, 0.1, 0.1), 4), 0.8263)
        self.assertEqual(round(std._p2(100, 0.01, 0.1, 1), 4), 0.9001)
        self.assertEqual(round(std.crit1(100, 0.01, 0.1, 0.1, 10), 4), 1.8189)
        self.assertEqual(round(std.crit2(100, 0.01, 0.1, 1, 0.7, 10, 15), 4), 5.2337)

    def test_calc_methods(self):
        t = 300  # время операции
        m = 7  # число целей
        n_min = 4  # число БЛА
        n_max = 12
        t1_min = 80  # позже theta
        t1_max = 120
        t2_min = 3  # позже lambda
        t2_max = 10
        t3_min = 0.2  # позже mu
        t3_max = 1
        p = 0.7  # вероятность поражения
        std = cc.Standard(m, n_min, n_max, t1_min, t1_max, t2_min, t2_max, t3_min, t3_max, p)
        calc = cc.Calc(std, t)

        self.assertEqual(round(calc._scalar(0.01, 0.1, 1, 10, 0.5, 0.5), 4), -1.6276)
        self.assertEqual(round(calc._target(0.01, 0.1, 1, 10), 4), 8.4679)


# предотвращение ненужных запусков при имплементации модуля
if __name__ == '__main__':
    ut.main()  # стандартная функция модуля unittest для проведения всех тестов сразу
