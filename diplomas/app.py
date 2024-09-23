"""Модуль для визуализации и создания приложения"""

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import calculations as cal
import sys
import warnings
from numpy import isclose
from numpy import round as np_round

warnings.filterwarnings("ignore")  # игнор варнингов


class App(QMainWindow):
    """Класс для GUI программы"""

    def __init__(self):
        """Метод-конструктор класса
        Ввод: None
        Вывод: None"""

        super().__init__()
        uic.loadUi('diplomas.ui', self)
        self.setWindowIcon(QtGui.QIcon('assets/icon.png'))  # подключение иконки приложения
        self.pareto_button.clicked.connect(self.show_pareto)  # подключение функционала для кнопок
        self.calc_button.clicked.connect(self.show_crit)

    def show_crit(self):
        """Метод для вывода результатов расчетов скалярного и прицельно-точечного критериев в GUI
        Ввод: None
        Вывод: None"""

        bck = False
        rnd = True
        msg = 'Неверный формат ввода данных!'

        try:
            t = float(self.input_t.text())  # default = 300
            if not (t > 0):
                msg = 'Неверно задано время эксперимента!'
                raise ArithmeticError
            n_min = int(self.input_nmin.text())  # default = 4
            n_max = int(self.input_nmax.text())  # default = 12
            if not (n_max >= n_min > 0):
                msg = 'Неверно заданы пределы числа БЛА!'
                raise ArithmeticError
            p = float(self.input_p.text())  # default = 0.7
            if not (0 < p < 1):
                msg = 'Неверно задана вероятность поражения цели!'
                raise ArithmeticError
            m = int(self.input_m.text())  # default = 7
            if not (m > 0):
                msg = 'Неверно задано количество целей!'
                raise ArithmeticError
            t1_min = float(self.input_t1min.text())  # default = 80
            t1_max = float(self.input_t1max.text())  # default = 1200
            if not (t1_max >= t1_min > 0):
                msg = 'Неверно заданы пределы параметра t1!'
                raise ArithmeticError
            t2_min = float(self.input_t2min.text())  # default = 3
            t2_max = float(self.input_t2max.text())  # default = 100
            if not (t2_max >= t2_min > 0):
                msg = 'Неверно заданы пределы параметра t2!'
                raise ArithmeticError
            t3_min = float(self.input_t3min.text())  # default = 0.2
            t3_max = float(self.input_t3max.text())  # default = 1
            if not (t3_max >= t3_min > 0):
                msg = 'Неверно заданы пределы параметра t3!'
                raise ArithmeticError
            if not (t1_max >= t2_min + t3_min):
                msg = 'Несоблюдение допущений моделей при выборе параметров!'
                raise ArithmeticError
            a1 = float(self.input_a1.text())  # default = 0.5
            a2 = float(self.input_a2.text())  # default = 0.5
            if not (a1 >= 0 and a2 >= 0 and isclose(a1 + a2, 1)):
                msg = 'Неверно заданы весовые коэффициенты!'
                raise ArithmeticError
            s = int(self.input_interval_count.text())  # default = 10

            self.label_errormessage.setText("")

            std = cal.Standard(m, n_min, n_max, t1_min, t1_max, t2_min, t2_max, t3_min, t3_max, p)
            calc = cal.Calc(std, t, steps=s)

            min_, params, ns = calc.overkill('scalar', a1=a1, a2=a2, background=bck, rounded=rnd,
                                             crits_output=True)
            self.output_scalar.clear()
            self.output_scalar.append(f"Минимум критерия = {np_round(min_, 4)}\n"
                                      f"\n"
                                      f"Ожидаемые параметры:\n"
                                      f"Среднее время сохранения работоспособности = {np_round(1 / params[0], 2)} мин.\n"
                                      f"Среднее время обнаружения и идентификации = {np_round(1 / params[1], 2)} мин.\n"
                                      f"Средняя продолжительность атаки по цели = {np_round(1 / params[2], 2)} мин.\n"
                                      f"Количество БЛА в группе = {np_round(params[3])} ед.\n"
                                      f"Число уничтоженных целей = {np_round(ns[1])} ед.\n"
                                      f"Число потерянных БЛА группы = {np_round(ns[0])} ед.\n")

            min_, params, ns = calc.overkill('target', background=bck, rounded=rnd, crits_output=True)
            self.output_target.clear()
            self.output_target.append(f"Минимум критерия = {np_round(min_, 4)}\n"
                                      f"\n"
                                      f"Ожидаемые параметры:\n"
                                      f"Среднее время сохранения работоспособности: {np_round(1 / params[0], 2)} мин.\n"
                                      f"Среднее время обнаружения и идентификации: {np_round(1 / params[1], 2)} мин.\n"
                                      f"Средняя продолжительность атаки по цели: {np_round(1 / params[2], 2)} мин.\n"
                                      f"Количество БЛА в группе: {np_round(params[3])} ед.\n"
                                      f"Число уничтоженных целей = {np_round(ns[1])} ед.\n"
                                      f"Число потерянных БЛА группы = {np_round(ns[0])} ед.\n")

        except ValueError:
            self.warn_user(message=msg)

        except ArithmeticError:
            self.warn_user(message=msg)

    def show_pareto(self):
        """Метод вывода результатов расчетов множества Парето в GUI
        Ввод: None
        Вывод: None"""

        bck = False
        rnd = True
        msg = 'Неверный формат ввода данных!'

        try:
            t = float(self.input_t.text())  # default = 300
            if not (t > 0):
                msg = 'Неверно задано время эксперимента!'
                raise ArithmeticError
            n_min = int(self.input_nmin.text())  # default = 4
            n_max = int(self.input_nmax.text())  # default = 12
            if not (n_max >= n_min > 0):
                msg = 'Неверно заданы пределы числа БЛА!'
                raise ArithmeticError
            p = float(self.input_p.text())  # default = 0.7
            if not (0 < p < 1):
                msg = 'Неверно задана вероятность поражения цели!'
                raise ArithmeticError
            m = int(self.input_m.text())  # default = 7
            if not (m > 0):
                msg = 'Неверно задано количество целей!'
                raise ArithmeticError
            t1_min = float(self.input_t1min.text())  # default = 80
            t1_max = float(self.input_t1max.text())  # default = 1200
            if not (t1_max >= t1_min > 0):
                msg = 'Неверно заданы пределы параметра t1!'
                raise ArithmeticError
            t2_min = float(self.input_t2min.text())  # default = 3
            t2_max = float(self.input_t2max.text())  # default = 100
            if not (t2_max >= t2_min > 0):
                msg = 'Неверно заданы пределы параметра t2!'
                raise ArithmeticError
            t3_min = float(self.input_t3min.text())  # default = 0.2
            t3_max = float(self.input_t3max.text())  # default = 1
            if not (t3_max >= t3_min > 0):
                msg = 'Неверно заданы пределы параметра t3!'
                raise ArithmeticError
            if not (t1_max >= t2_min + t3_min):
                msg = 'Несоблюдение допущений моделей при выборе параметров!'
                raise ArithmeticError
            a1 = float(self.input_a1.text())  # default = 0.5
            a2 = float(self.input_a2.text())  # default = 0.5
            if not (a1 >= 0 and a2 >= 0 and isclose(a1 + a2, 1)):
                msg = 'Неверно заданы весовые коэффициенты!'
                raise ArithmeticError
            s = int(self.input_interval_count.text())  # default = 10

            self.label_errormessage.setText("")

            std = cal.Standard(m, n_min, n_max, t1_min, t1_max, t2_min, t2_max, t3_min, t3_max, p)
            calc = cal.Calc(std, t, steps=s)

            calc.overkill('pareto', background=bck, rounded=rnd)

        except ValueError:
            self.warn_user(message=msg)

        except ArithmeticError:
            self.warn_user(message=msg)

    def warn_user(self, message: str = None):
        """Метод, изменяющий сообщение-предупреждение для пользователя на желаемое сообщение
        Ввод: message: str -- желаемое сообщение
        Вывод: None"""

        if message is None:
            message = 'Что-то пошло не так.'

        self.label_errormessage.setText(message)


def main():
    """Основная исполняющая функция, по совместительству скрипт запуска приложения"""

    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())


# во избежание лишних запусков при импортировании
if __name__ == "__main__":
    main()
