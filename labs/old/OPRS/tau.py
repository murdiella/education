import matplotlib.pylab as plt
import math as m

# Михайлов
# u = []
# v = []
# a3 = 0.0144
# a2 = 2.8793
# a1 = 1
# a0 = 0.0291
# for i in range(50):
#     w = i * 0.2
#     u.append(-a2 * w**2 + a0)
#     v.append(-a3 * w**3 + a1 * w)
#     print(round(w, 3), ' ', round(u[-1], 4), ' ', round(v[-1], 4))
#
# plt.plot(u, v, '-o')
# plt.show()

# Найквист
uw = []
vw = []
K = 0.0291
T1 = 2.8802
T2 = 0.005
for i in range(50):
    w = (i + 1) * 0.02
    uw.append(-(K * (T1 + T2) * w**2) / (T1 ** 2 * T2 ** 2 * w ** 6 + ((T1 + T2)**2 - 2 * T1 * T2) * w**4 + w**2))
    vw.append((K * (T1 * T2 * w**3 - w)) / (T1 ** 2 * T2 ** 2 * w ** 6 + ((T1 + T2) ** 2 - 2 * T1 * T2) * w ** 4 + w ** 2))
    print(round(w, 3), ' ', round(uw[-1], 5), ' ', round(vw[-1], 5))
# plt.plot(-1, 0, '-o', color='r')
plt.plot(uw, vw, '-o')
plt.show()

# ЛФЧХ
# T1 = 2.8802
# T2 = 0.005
# K = 0.0291
# lst = [0.01, 0.1, 1/T1, 1, 10, 100, 1/T2, 1000]
# def phi(w):
#     return (-m.pi/2 - m.atan(T1 * w) - m.atan(T2 * w)) * 180 / m.pi
# for item in lst:
#     print(f'{round(item, 3)} {round(phi(item), 4)}')

# ЛАЧХ
# def lm(w):
#     lm0 = 20*m.log10(K)
#     return lm0 - 20 * m.log10(w) + 20 * m.log10(1 / m.sqrt(T1**2 * w**2 + 1)) + 20 * m.log10(1 / m.sqrt(T2**2 * w**2 + 1))
# for item in lst:
#     print(f'{round(item, 3)} | {round(lm(item), 4)}')
