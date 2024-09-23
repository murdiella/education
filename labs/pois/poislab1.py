from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')


def byhand(x, y):
    xline = [min(x), max(x)]
    # y = kx + b = kx -> w0*y + w1*x = 0 -> w0 = -1, w1 = k
    k = -0.3
    yline = [k * x for x in xline]
    cnt = 0
    for i in range(len(x)):
        if y[i] >= x[i] * k:
            cnt += 1

    w0 = cnt / len(x)
    w1 = 1 - w0
    print(w0, w1)

    plt.scatter(x, y)
    plt.scatter(0, 0, color='red')
    plt.plot(xline, yline, color='red', linestyle='--')
    plt.show()


def neuro(x, y):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    w0 = 2 * np.random.random((5, 5)) - 1
    w1 = 2 * np.random.random((5, 2)) - 1
    n = 0.1
    errors = []

    # сигмоиды
    def sig(x):
        return 1 / (1 + np.exp(-x))

    def sig_dx(x):
        return sig(x) * (1 - sig(x))

    if len(y_train.shape) == 1:
        y_train_one_hot = np.zeros((len(y_train), 2))
        y_train_one_hot[np.arange(len(y_train)), y_train] = 1
    else:
        y_train_one_hot = y_train

    for i in range(10000):
        # прямое распространение
        layer0 = X_train
        layer1 = sig(np.dot(layer0, w0))
        layer2 = sig(np.dot(layer1, w1))

        predicted_classes = np.argmax(layer2, axis=1)
        layer2_error = y_train_one_hot - layer2

        # дельта без обратного распространения ошибки
        layer2_delta1 = sig_dx(np.dot(layer1, w1[:, 0].reshape(-1, 1)))
        layer2_delta2 = sig_dx(np.dot(layer1, w1[:, 1].reshape(-1, 1)))

        # дельта с обратным распространением
        # layer2_delta1 = layer2_error[:, 0].reshape(-1, 1) * sig_dx(np.dot(layer1, w1[:, 0].reshape(-1, 1)))
        # layer2_delta2 = layer2_error[:, 1].reshape(-1, 1) * sig_dx(np.dot(layer1, w1[:, 1].reshape(-1, 1)))

        for j in range(len(w1)):
            w1[j, 0] += layer1.T.dot(layer2_delta1)[j] * n

        for j in range(len(w1)):
            w1[j, 1] += layer1.T.dot(layer2_delta2)[j] * n

        layer1_error = layer2_delta1.dot(w1[:, 0].reshape(-1, 1).T) + layer2_delta2.dot(w1[:, 1].reshape(-1, 1).T)
        layer1_delta = layer1_error * sig_dx(np.dot(layer0, w0))
        w0 += layer0.T.dot(layer1_delta) * n

        error = np.mean(np.abs(layer2_error))
        errors.append(error)
        accuracy = (1 - error) * 100

    a1, b1 = w0[0, 0], w0[1, 0]
    a2, b2 = w0[0, 1], w0[1, 1]
    c1, c2 = w1[0], w1[1]
    x_values = np.linspace(-8, 8, 100)

    a1_values = np.full_like(x_values, a1)
    b1_values = np.full_like(x_values, b1)
    a2_values = np.full_like(x_values, a2)
    b2_values = np.full_like(x_values, b2)
    c1_mean = np.mean(c1)
    c2_mean = np.mean(c2)
    c1_values = np.full_like(x_values, c1_mean)
    c2_values = np.full_like(x_values, c2_mean)

    y_values1 = (-a1_values * x_values - c1_values) / b1_values
    y_values2 = (-a2_values * x_values - c2_values) / b2_values

    print("Точность: " + str(accuracy / 100))
    print(w0, w1)

    plt.scatter(x[:, 3], x[:, 4], c=y, cmap=plt.cm.coolwarm)
    plt.plot(x_values, y_values1, color='red', linestyle='--')
    plt.show()
    plt.plot(errors)
    plt.xlabel('Обучение')
    plt.ylabel('Ошибка')
    plt.show()


def main():
    # var 5
    r = 70
    X, Y = make_classification(n_samples=2000, n_features=5, n_informative=4, n_redundant=1, n_repeated=0, n_classes=2,
                               n_clusters_per_class=3, class_sep=4, flip_y=0, weights=[0.5, 0.5], random_state=r)

    x = np.array(X)[:, 3]
    y = np.array(X)[:, 4]

    # byhand(x, y)
    neuro(X, Y)


if __name__ == '__main__':
    main()
