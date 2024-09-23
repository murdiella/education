import math as m


# функция по заданию
def fx(x):
    s1 = 0
    for i in range(len(x)):
        s1 += x[i] * x[i]
    return m.sin(s1) * m.cos(2 * s1)


# функция сложения двух массивов-векторов
def add(x, y):
    res = []
    for i in range(len(x)):
        res.append(x[i] + y[i])
    return res


# фукнция вычитания двух массивов-векторов
def sub(x, y):
    res = []
    for i in range(len(x)):
        res.append(x[i] - y[i])
    return res


# фукнция градиента
def gradient(f, x0):
    res = []  # здесь будет наш результат
    dx = 0.001  # шаг интегрирования
    print(f"dx: {dx}")
    dxss = []  # масив из dx

    # заполнение массива dxss
    for i in range(len(x0)):
        dxs = [0] * len(x0)  # dxs -- временная переменная для заполнения dxss
        dxs[i] = dx
        dxss.append(dxs)

    # реализация самой формулы градиента
    for i in range(len(x0)):
        xi = (f(add(x0, dxss[i])) - f(sub(x0, dxss[i]))) / (2 * dx)
        res.append(xi)

    return res


def main():

    grad = gradient(fx, [1, -0.5, 2, -1, 0.5])
    print(f"полученное значение градиента в точке xT: {grad}")

    tru = [1.410857, -0.705429, 2.821715, -1.410857, 0.705429]  # действительные значения (получены аналитически)
    print(f"действительное значение градиента в точке (полученное аналитически): {tru}")

    # объявим переменные для всех необходимых ошибок
    error = []
    relative_error = []
    squared_absolute_error = 0
    # блок вычисления ошибок в цикле
    for i in range(len(grad)):
        error.append(tru[i] - grad[i])
        relative_error.append((tru[i] - grad[i]) / tru[i] * 100)
        squared_absolute_error += error[i] * error[i]

    print(f"ошибка: {error}")
    print(f"относительная ошибка: {relative_error}")
    print(f"абсолютная ошибка: {m.sqrt(squared_absolute_error)}")


if __name__ == "__main__":
    main()
