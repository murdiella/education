import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def draw_everything(curve_yx1: list, curve_yx2: list, curve_yx3: list, borderline: float, add_borderline=None):
    """Метод для отрисовки двух нормально распределенных кривых и критериальной границы"""

    if not (len(curve_yx1) == len(curve_yx2) == 2):
        raise ValueError('Неверный формат ввода')

    # задаем разметку для значений по оси абсцисс
    xs_p_y_x1 = np.linspace(curve_yx1[0] - 3 * curve_yx1[1], curve_yx1[0] + 3 * curve_yx1[1], 100)
    xs_p_y_x2 = np.linspace(curve_yx2[0] - 3 * curve_yx2[1], curve_yx2[0] + 3 * curve_yx2[1], 100)
    xs_p_y_x3 = np.linspace(curve_yx3[0] - 3 * curve_yx3[1], curve_yx3[0] + 3 * curve_yx3[1], 100)

    # задаем прямую по указанному x = borderline
    borderline_x = [borderline] * 2
    borderline_y = [norm.pdf(curve_yx1[0], curve_yx1[0], curve_yx1[1]) + norm.pdf(curve_yx2[0], curve_yx2[0], curve_yx2[1]),
                    - (norm.pdf(curve_yx1[0], curve_yx1[0], curve_yx1[1]) + norm.pdf(curve_yx2[0], curve_yx2[0], curve_yx2[1])) / 8]
    if add_borderline is not None:
        add_borderline_x = [add_borderline] * 2
        add_borderline_y = [
            norm.pdf(curve_yx1[0], curve_yx1[0], curve_yx1[1]) + norm.pdf(curve_yx2[0], curve_yx2[0], curve_yx2[1]),
            - (norm.pdf(curve_yx1[0], curve_yx1[0], curve_yx1[1]) + norm.pdf(curve_yx2[0], curve_yx2[0],
                                                                             curve_yx2[1])) / 8]
        plt.plot(add_borderline_x, add_borderline_y, color='red', linestyle='--')

    # рисуем кривые и выводим
    plt.plot(xs_p_y_x1, norm.pdf(xs_p_y_x1, curve_yx1[0], curve_yx1[1]), color='blue')
    plt.plot(xs_p_y_x2, norm.pdf(xs_p_y_x2, curve_yx2[0], curve_yx2[1]), color='green')
    plt.plot(xs_p_y_x3, norm.pdf(xs_p_y_x3, curve_yx3[0], curve_yx3[1]), color='red')
    plt.plot(borderline_x, borderline_y, color='green', linestyle='--')
    plt.ylabel('p(Y/x)')
    plt.xlabel('x')
    plt.show()


def min_risk(rs, p_xs, p_y_xs):
    """Метод для расчета критерия минимального риска"""

    border1 = (rs[0] - rs[1]) * (p_xs[1] * p_y_xs[1]) / (p_xs[0] * p_y_xs[0])
    border2 = (rs[2] - rs[3]) * (p_xs[2] * p_y_xs[2]) / (p_xs[0] * p_y_xs[0])
    return border1, border2


def ideal(p_xs, p_y_xs):
    """Метод для расчета значения и построения графика к критерию идеального наблюдения"""

    value21 = p_xs[1] * p_y_xs[1] / p_xs[0] * p_y_xs[0]
    value31 = p_xs[2] * p_y_xs[2] / p_xs[0] * p_y_xs[0]
    value32 = p_xs[2] * p_y_xs[2] / p_xs[1] * p_y_xs[1]
    max_value = max([value21, value31, value32])
    plt.bar([1, 2, 3], [value21, value31, value32])
    plt.plot([0, 4], [max_value] * 2, color='red', linestyle='--')
    plt.ylabel('P(Y/x)')
    plt.xlabel('Object number')
    plt.show()

    return max_value


def main():
    # [МО, СКО]
    # все значения для x1 принимаем за фон

    # кривульки
    curve_yx1 = [0, 1]  # P(Y/X1)
    curve_yx2 = [0.5, 0.5]  # P(Y/X2)
    curve_yx3 = [-1, 0.7]  # P(Y/X3)

    # вероятности присутствия признаков на изображении
    p_x1 = 0.8
    p_x2 = 0.6
    p_x3 = 0.5

    # условные плотности присутствия признака (задаем вот так, нуаче)
    p_y_x1 = 0.7
    p_y_x2 = 0.4
    p_y_x3 = 0.5

    # риски для объектов с фоном
    r21 = 0.1
    r12 = 0.5
    r31 = 0.2
    r13 = 0.7

    rs = [r12, r21, r31, r13]
    p_xs = [p_x1, p_x2, p_x3]
    p_y_xs = [p_y_x1, p_y_x2, p_y_x3]

    # получаем две границы для 2 и 3 кривых относительно фона соответственно
    border21, border31 = min_risk(rs, p_xs, p_y_xs)

    # для критерия мин. риска
    draw_everything(curve_yx1, curve_yx2, curve_yx3, border21, add_borderline=border31)

    # для критерия идеального наблюдения
    res = ideal(p_xs, p_y_xs)
    print(f'Crit value = {res}')


if __name__ == '__main__':
    main()
