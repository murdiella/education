import numpy as np
from scipy.stats import t, f
import matplotlib.pyplot as plt


# линейная модель в общем виде
def linearModel(a, f):
    return np.matmul(np.transpose(a), f)


# вектор-функция, заданная заданием варианта 5
def vectorFunc(x):
    return np.array([np.sqrt(x[2]), x[0], np.sqrt(x[0]), x[1] * x[2]])


# реализация МНК
def MNK(x, y):
    # делаем усредненный вектор Уср
    Y_avg = np.array([])
    for i in range(len(y)):
        i_summ = 0
        for j in range(len(y[0])):
            i_summ += y[i][j]
        i_summ = i_summ / len(y[0])
        Y_avg = np.append(Y_avg, np.array(i_summ))
    # print(f'Y_avg = {Y_avg}')  # вывод усредненного вектора Yср  (2)

    # делаем матрицу F
    func_len = len(vectorFunc(x[0]))
    F = np.empty((0, func_len), float)
    for i in range(len(x)):
        new_row = [vectorFunc(x[i])[j] for j in range(func_len)]
        F = np.append(F, np.array([new_row]), axis=0)
    # print(f'F = \n{F}\n')  # вывести матрицу F (3)

    # print(f'Ft = \n{np.transpose(F)}\n')  # вывести матрицу Fт (4)
    # print(f'С: = \n{np.matmul(np.transpose(F), F)}\n')  # вывести матицу С' (5)
    C = np.linalg.inv(np.matmul(np.transpose(F), F))
    # print(f'С = \n{C}\n')  # вывести матрицу С (8)
    CFt = np.matmul(C, np.transpose(F))
    # print(f'CFt = \n{CFt}\n')  # вывести матрицу CFт (9)
    a_est = np.matmul(CFt, Y_avg)
    # print(f'a* = {a_est}')  # вывести вектор оценок параметров модели (10)
    Y_est = np.array([])
    for i in range(len(x)):
        Y_est = np.append(Y_est, np.array(linearModel(a_est, vectorFunc(x[i]))))
    # print(f'Y* = {Y_est}')  # вывести вектор оценок выходных значений модели (11)

    sample_disp = 0
    for i in range(len(y)):
        for j in range(len(y[0])):
            sample_disp += (y[i][j] - Y_est[i]) ** 2
    sample_disp = sample_disp / (len(y) - len(a_est))
    # print(f'D = {sample_disp}')  # вывести значение выборочной дисперсии (12)

    t_quantile = t(df=len(y) - len(a_est)).ppf(0.95)
    # print(f't_quantile = {t_quantile}')  # выввести квантиль Стьюдента для дов. вер-ти 0.95 (12)
    intervals = []
    for i in range(len(a_est)):
        intervals.append([a_est[i] - t_quantile * np.sqrt(sample_disp) * np.sqrt(C[i][i]), a_est[i] + t_quantile * np.sqrt(sample_disp) * np.sqrt(C[i][i])])
    intervals = np.array(intervals)
    # print(f'intervals = \n{intervals}\n')  # вывести границы доверительных интервалов (12)

    S1 = 0
    S2 = 0
    for_graph = []  # дисперсии в каждой точке Уср для графика
    for i in range(len(y)):
        temp = (Y_avg[i] - linearModel(a_est, vectorFunc(x[i]))) ** 2 / (len(y) - len(a_est))
        for_graph.append(temp)
        S1 += temp
    # print(f'S1 = {S1}')  # вывести значение дисперсии ошибок модели (13)

    for i in range(len(y)):
        for j in range(len(y[0])):
            S2 += (y[i][j] - np.mean(y[i])) ** 2
    S2 = S2 / (len(y) * (len(y[0]) - 1))
    # print(f'S2 = {S2}')  # вывести значение дисперсии ошибок измерений (13)

    F_stat = (S1 ** 2) / (S2 ** 2)
    # print(f'F_stat = {F_stat}')  # вывести значение статистики Фишера (13)
    f_quantile = f.ppf(0.95, dfn=len(y) - len(a_est), dfd=len(y) * (len(y[0]) - 1))
    # print(f'f_quantile = {f_quantile}')  # вывести критическое значение F распределения (13)

    plt.scatter(Y_avg, Y_est)  # зависимость y*(y_ср) (14)
    plt.xlabel('Y среднее в эксперименте')
    plt.ylabel('Оценка Y')
    plt.show()
    plt.scatter(Y_avg, for_graph)  # зависимость disp_y(y_ср) (15)
    plt.xlabel('Y среднее в эксперименте')
    plt.ylabel('Дисперсия оценки выходной координаты')
    plt.show()


def main():
    # вариант 5
    #                       X_1  X_2  X_3
    input_data = np.array([[1.5, 0.6, 0.4],   # exp. 1
                           [2.0, 1.3, 0.5],   # exp. 2
                           [2.5, 1.1, 2.1],   # exp. 3
                           [3.0, 4.2, 1.4],   # exp. 4
                           [2.5, 1.4, 3.2],   # exp. 5
                           [2.0, 2.4, 1.6]])  # exp. 6

    #                        Y_i1  Y_i2  Y_i3  Y_i4  Y_i5
    output_data = np.array([[4.40, 6.61, 7.32, 5.57, 6.27],        # exp. 1 ~ Y1
                            [6.47, 7.86, 8.96, 8.96, 8.72],        # exp. 2 ~ Y2
                            [13.26, 15.56, 14.20, 14.18, 13.00],   # exp. 3 ~ Y3
                            [25.35, 25.51, 22.15, 25.44, 23.20],   # exp. 4 ~ Y4
                            [18.41, 18.89, 18.05, 18.28, 19.67],   # exp. 5 ~ Y5
                            [16.11, 15.80, 15.54, 16.81, 15.66]])  # exp. 6 ~ Y6

    MNK(input_data, output_data)


# во избежание лишних вычислений при переиспользовании функций модуля,
# инициируем функцию main() только при запуске модуля
if __name__ == '__main__':
    main()
