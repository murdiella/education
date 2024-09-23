import math as m
dX = []


def main():
    X = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    global dX
    dX = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    n = len(X)

    grad = gradient(f, X)
    actual = [-0.036928, -0.073836, -0.110702, -0.147504, -0.184224, -0.220842, -0.257340, -0.293701, -0.329909, -0.365951]
    error = [None] * n
    rel_error = [None] * n
    abs_error = 0
    for i in range(n):
        error[i] = actual[i] - grad[i]
        rel_error[i] = (actual[i] - grad[i]) / actual[i] * 100
        abs_error += error[i] ** 2
    abs_error = m.sqrt(abs_error)

    print(f'X = {X}\n')
    print(f'dX = {dX}\n')
    print(f'n = {n}\n')
    print(f'Gradient = {grad}')
    print(f'Error = {grad}')
    print(f'Relative Error = {rel_error}')
    print(f'Absolute Error = {abs_error}')


def gradient(F, X):
    newX = []
    n = len(X)
    X1 = [None] * n
    X2 = [None] * n
    for i in range(n):
        e = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        e[i] = dX[i]
        for j in range(n):
            X1[j] = X[j] + e[j]
            X2[j] = X[j] - e[j]
        grad = (F(X1) - F(X2)) / (2 * dX[i])
        newX.append(grad)
    return newX


def f(X):
    sum1 = sum2 = 0
    n = len(X)
    for i in range(n):
        sum1 += X[i] * X[i]
        sum2 += m.cos(X[i])
    return m.exp(-sum1) * sum2


if __name__ == "__main__":
    main()
