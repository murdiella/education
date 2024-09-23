import numpy as np
import math as m
import matplotlib.pyplot as plt
import sys
import random as r
from abc import ABCMeta, abstractmethod

r.seed()
mu = 3.986 * 10 ** 14
mode = 1


class TIntegrator:
    __metaclass__ = ABCMeta
    coordsx = []
    coordsy = []
    coordsz = []

    def integrate(self, KA, vect, func, t0, tk, dt):
        self.coordsx = []
        self.coordsy = []
        self.coordsz = []
        time = np.arange(t0, tk, dt)
        self.coordsx.append(vect[0])
        self.coordsy.append(vect[1])
        self.coordsz.append(vect[2])
        for t in time:
            for i in range(len(vect)):
                vect[i] = self.onestep(vect[i], func[i], t, dt)
                if i == 0:
                    self.coordsx.append(vect[i])
                elif i == 1:
                    self.coordsy.append(vect[i])
                elif i == 2:
                    self.coordsz.append(vect[i])
            func = KA.RP()
        return vect

    @abstractmethod
    def onestep(self, vect, func, t, dt):
        pass


class TEuler(TIntegrator):

    def onestep(self, vect, func, t, dt):
        vect += func * dt
        return vect


class TKutta(TIntegrator):

    def onestep(self, vect, func, t, dt):
        k1 = func(t, vect)
        k2 = func(t + dt / 2, vect + dt * k1 / 2)
        k3 = func(t + dt / 2, vect + dt * k2 / 2)
        k4 = func(t + dt, vect + dt * k3)
        vect += dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return vect


class TDynamicModel:

    def __init__(self, fx, fy, fz, fvx, fvy, fvz):
        self.x = fx
        self.y = fy
        self.z = fz
        self.vx = fvx
        self.vy = fvy
        self.vz = fvz
        self.r = m.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        self.vect = [fx, fy, fz, fvx, fvy, fvz]

    def getr(self):
        self.r = m.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return m.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def RP(self):
        F = [None] * 6
        F[0] = self.vect[3]
        F[1] = self.vect[4]
        F[2] = self.vect[5]
        F[3] = - mu * self.vect[0] / m.sqrt(self.vect[0] ** 2 + self.vect[1] ** 2 + self.vect[2] ** 2) ** 3
        F[4] = - mu * self.vect[1] / m.sqrt(self.vect[0] ** 2 + self.vect[1] ** 2 + self.vect[2] ** 2) ** 3
        F[5] = - mu * self.vect[2] / m.sqrt(self.vect[0] ** 2 + self.vect[1] ** 2 + self.vect[2] ** 2) ** 3
        return F

    def __del__(self):
        print('CA removed')


def main():
    mode = int(input('Enter 1 for Eulers method, 2 for Kuttas method\n'))

    if mode == 1 or mode == 2:
        t = float(input('Enter your prefered period of time\n'))
        dt = float(input('Enter your prefered dt\n'))

        wish = str(input('Do you REALLY want to write all that coordinates and stuff? Y/n\n'))
        if wish.lower() == 'y':
            x = float(input('Enter your X\n'))
            y = float(input('Enter your Y\n'))
            z = float(input('Enter your Z\n'))
            vx = float(input('Enter your speed Vx\n'))
            vy = float(input('Enter your speed Vy\n'))
            vz = float(input('Enter your speed Vz\n'))
            KA = TDynamicModel(x, y, z, vx, vy, vz)

        elif wish.lower() == 'n':
            # KA = TDynamicModel(r.uniform(0, 100000), r.uniform(0, 100000), r.uniform(0, 100000), r.uniform(0, 100000), r.uniform(0, 1000000), r.uniform(0, 1000))
            KA = TDynamicModel(0, 0, 19000000, 3600, 0, 0)

        else:
            print('Incorrect mode input')
            sys.exit()

        xs = ys = zs = []
        if mode == 1:
            TE = TEuler()
            F = KA.RP()
            KA.vect = TE.integrate(KA, KA.vect, F, 0, t, dt)
            xs = TE.coordsx
            ys = TE.coordsy
            zs = TE.coordsz
        else:
            pass
            # TK = TKutta()
            # F = TK.RP(KA.vect)
            # for i in range(6):
            #     KA.vect[i] = TK.integrate(KA.vect[i], F[i], 0, t, dt)
            #     if i == 0:
            #         xs = TK.coords
            #     elif i == 1:
            #         ys = TK.coords
            #     elif i == 2:
            #         zs = TK.coords

        # fig = plt.figure()
        # ax = plt.axes()
        #
        # plot1 = plt.figure(1)
        # ax.plot(xs, ys)
        # plot2 = plt.figure(2)
        # plt.plot(xs, zs)
        # plot3 = plt.figure(3)
        # plt.plot(ys, zs)
        #
        # plt.show()

        ax = plt.axes(projection='3d')
        ax.scatter3D(0, 0, 0, color='green')
        ax.plot3D(xs, ys, zs, 'gray')
        ax.set_xlabel('x, 10^6m')
        ax.set_ylabel('y, 10^6m')
        ax.set_zlabel('z, 10^6m')
        plt.show()


if __name__ == '__main__':
    main()
