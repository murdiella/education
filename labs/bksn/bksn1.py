import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def draw_everything(curve_yx1: list, curve_yx2: list, borderline: float, add_borderline=None):
    """Метод для отрисовки двух нормально распределенных кривых и критериальной границы"""

    if not (len(curve_yx1) == len(curve_yx2) == 2):
        raise ValueError('Неверный формат ввода')

    # задаем разметку для значений по оси абсцисс
    xs_p_y_x1 = np.linspace(curve_yx1[0] - 3 * curve_yx1[1], curve_yx1[0] + 3 * curve_yx1[1], 100)
    xs_p_y_x2 = np.linspace(curve_yx2[0] - 3 * curve_yx2[1], curve_yx2[0] + 3 * curve_yx2[1], 100)

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
    plt.plot(borderline_x, borderline_y, color='red', linestyle='--')
    plt.ylabel('p(Y/x)')
    plt.xlabel('x')
    plt.show()


def bayes(r12: float, r21: float, p1: float):
    """Метод для расчета границы с помощью критерия минимального байесовского риска"""

    if abs(p1) > 1 or p1 == 0:
        raise ValueError('Неверный формат ввода')

    return (r21 * p1) / (r12 * (1 - p1))


def zig_kotel(p1: float):
    """Метод для расчета границы с помощью критерия идеального наблюдения Зигерта-Котельникова"""

    if abs(p1) > 1 or p1 == 0:
        raise ValueError('Неверный формат ввода')

    return p1 / (1 - p1)


def fisher():
    """Метод для расчета границы с помощью критерия максимального правдоподобия Фишера"""

    return 1


def minmax(p1: float, r12: float, r21: float):
    """Метод для расчета границы с помощью минимаксного критерия"""

    if abs(p1) > 1 or p1 == 0:
        raise ValueError('Неверный формат ввода')

    return min((r12 * p1) / (r21 * (1 - p1)), (r12 * (1 - p1)) / (r21 * p1))


def neyman_piercon(curve1: list, curve2: list, param: float, param_type='beta'):
    """Метод для расчета границы с помощью критерия Неймана-Пирсона"""

    if not (len(curve1) == len(curve2) == 2):
        raise ValueError('Неверный формат ввода')

    if param_type == 'beta':
        return norm.cdf(norm.ppf((param + norm.cdf(-np.inf, curve2[0], np.sqrt(curve2[1]))), curve2[0],
                                 np.sqrt(curve2[1])), param, np.sqrt(curve2[1]))
    elif param_type == 'alpha':
        return norm.cdf(norm.ppf((param + norm.cdf(-np.inf, curve1[0], np.sqrt(curve1[1]))), curve1[0],
                                 np.sqrt(curve1[1])), param, np.sqrt(curve1[1]))

    else:
        raise ValueError('Неверный формат ввода')


def vald(alpha, beta):
    """Метод для расчета границы с помощью критерия Вальда"""

    return (beta / (1 - alpha)), ((1 - beta) / alpha)


def main():
    """Основная исполняющая функция"""

    # [МО, СКО]
    curve_yx1 = [-2, 4]  # P(Y/X1)
    curve_yx2 = [10, 5]  # P(Y/X2)
    p1 = 0.4  # P(X1)
    r12 = 0.2
    r21 = 0.6
    alpha = 0.1
    beta = 0.7
    
    # border = bayes(r12, r21, p1)  # Байес
    # border = zig_kotel(p1)  # Зигерт-Котельников
    # border = fisher()  # Фишер
    # border = minmax(p1, r12, r21)  # Минимаксный
    # border = neyman_piercon(curve_yx1, curve_yx2, beta)
    border1, border2 = vald(alpha, beta)  # Вальд

    # draw_everything(curve_yx1, curve_yx2, border)
    draw_everything(curve_yx1, curve_yx2, border1, border2)  # для критерия Вальда


if __name__ == "__main__":
    main()
