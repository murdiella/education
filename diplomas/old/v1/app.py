"""Модуль для визуализации и создания приложения"""

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import calculations as cal
import sys
import warnings


class App(QMainWindow):
    """"""

    def __init__(self):
        """"""
        super().__init__()
        uic.loadUi('diplomas.ui', self)
        self.pareto_button.clicked.connect(self.show_pareto)
        self.calc_button.clicked.connect(self.show_crit)


    def show_crit(self):
        """"""
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
        std = cal.Standard(m, n_min, n_max, t1_min, t1_max, t2_min, t2_max, t3_min, t3_max, p)
        calc = cal.Calc(std, t, steps=s)

        bck = False
        rnd = True

        min_, params = calc.overkill('scalar', background=bck, rounded=rnd)
        self.output_scalar.clear()
        self.output_scalar.append(f"Минимум критерия = {min_}\n"
                                  f"theta = {params[0]}, lambda = {params[1]}, mu = {params[2]}, n = {params[3]}\n")

        min_, params = calc.overkill('target', background=bck, rounded=rnd)
        self.output_target.clear()
        self.output_target.append(f"Минимум критерия = {min_}\n"
                                  f"theta = {params[0]}, lambda = {params[1]}, mu = {params[2]}, n = {params[3]}\n")

    def show_pareto(self):
        """"""
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
        std = cal.Standard(m, n_min, n_max, t1_min, t1_max, t2_min, t2_max, t3_min, t3_max, p)
        calc = cal.Calc(std, t, steps=s)

        bck = False
        rnd = True

        calc.overkill('pareto', background=bck, rounded=rnd)


def main():
    """"""
    # warnings.filterwarnings("ignore")  # игнор варнингов

    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())


# во избежание лишних запусков при импортировании
if __name__ == "__main__":
    main()
