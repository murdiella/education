from calculations import *


def graphs():
    t_min = 60  # время операции В МИНУТАХ, def = 300
    t_max = 300
    m = 7  # число целей, def = 7
    n_min = 6  # число БЛА, def = 4
    n_max = 40  # def = 12
    t1_min = 20  # позже theta, def = 80
    t1_max = 200  # def = 1200
    t2_min = 2  # позже lambda, def = 3
    t2_max = 50  # def = 100
    t3_min = 0.1  # позже mu, def = 0.2
    t3_max = 1.5  # def = 1
    p = 0.7  # вероятность поражения
    s = 100
    std = Standard(m, n_min, n_max, t1_min, t1_max, t2_min, t2_max, t3_min, t3_max, p)

    nums = np.linspace(n_min, n_max, n_max - n_min + 1)
    ts = np.linspace(t_min, t_max, s)
    t1s = np.linspace(t1_min, t1_max, s)
    t2s = np.linspace(t2_min, t2_max, s)
    t3s = np.linspace(t3_min, t3_max, s)
    ps = np.linspace(0.05, 0.95, s)
    ms = np.linspace(4, 12, 9)

    skipcount = 0
    count = 0
    c1s = []  # x -- МО упавших БЛА
    c2s = []  # y -- МО количества пораженных целей

    # собственно, перебор значений
    params = ms
    for param in params:
        try:
            c1s.append(std.crit1(t_min, 1 / t1_min, 1 / t2_min, 1 / t3_min, n_min))
            c2s.append(std.crit2(t_min, 1 / t1_min, 1 / t2_min, 1 / t3_min, p, n_min, param))
        except ValueError:
            print(param)
            pass

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))
    title = fig.suptitle(f't = {t_min}, t1 = {t1_min}, t2 = {t2_min}, t3 = {t3_min}, p = {p}, n = {n_min}')

    ax[0].plot(params, c1s)
    ax[0].set_title('МО числа БЛА, которые будут потеряны к моменту времени t')
    ax[0].set_xlabel('m, ед')
    ax[0].set_ylabel('Число потерянных БЛА, ед.')

    ax[1].plot(params, c2s, color='red')
    ax[1].set_title('МО числа целей, которые будут поражены к моменту времени t')
    ax[1].set_xlabel('m, ед')
    ax[1].set_ylabel('Число пораженных целей, ед.')
    plt.show()


if __name__ == '__main__':
    graphs()
