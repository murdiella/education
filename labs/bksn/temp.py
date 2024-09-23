import numpy as np
import matplotlib.pyplot as plt


def func(ts, theta):
    fs = []
    for t in ts:
        fs.append(theta * np.exp(-theta * t))
    return fs


def main():
    x = np.linspace(0, 5, 100)
    th1 = 0.5
    p1 = func(x, th1)
    th2 = 1
    p2 = func(x, th2)
    th3 = 1.8
    p3 = func(x, th3)
    plt.xlabel('t1')
    plt.ylabel('p(t1)')
    plt.plot(x, p1, linestyle='--')
    plt.plot(x, p2, linestyle='--')
    plt.plot(x, p3, linestyle='--')
    plt.show()
    

if __name__ == "__main__":
    main()