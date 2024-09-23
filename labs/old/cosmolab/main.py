import numpy as np
import math as m
import matplotlib.pyplot as plt
import random as r
import sys

mu = 3.986 * 10 ** 14


class TIntegrator:
    coords = []

    def integrate(self, mode, vect, func, t0, tk, dt):
        self.coords = []
        time = np.arange(t0, tk, dt)
        self.coords.append(vect)
        if mode == 1:
            for t in time:
                vect = self.Euler(vect, func, t, dt)
                self.coords.append(vect)
            return vect
        elif mode == 2:
            for t in time:
                vect = self.Kutta(vect, func, t, dt)
                self.coords.append(vect)
            return vect
        else:
            print('wrong number, buddy')
            sys.exit()

    def Euler(self, vec, fun, t, dt):
        vec += fun(t, vec) * dt
        return vec

    def Kutta(self, vec, fun, t, dt):
        k1 = fun(t, vec)
        k2 = fun(t + dt / 2, vec + dt * k1 / 2)
        k3 = fun(t + dt / 2, vec + dt * k2 / 2)
        k4 = fun(t + dt, vec + dt * k3)
        vec += dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return vec


class TDynamicModel:

    def __init__(self, fx, fy, fz, fv, alpha, beta, theta):
        self.x = fx
        self.y = fy
        self.z = fz
        self.vx = fv * m.cos(alpha)
        self.vy = fv * m.cos(beta)
        self.vz = fv * m.cos(theta)
        self.r = m.sqrt(fx ** 2 + fy ** 2 + fz ** 2)

    def geta(self, x):
        return - mu * x / self.r ** 3

    def getr(self):
        self.r = m.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return m.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def getvx(self, t):
        return self.vx * 0.2 + self.vx * m.cos(t)

    def getvy(self, t):
        return self.vy * 0.3 + self.vy * m.sin(t)

    def getvz(self, t):
        return self.vz * 0.5 + self.vz * m.cos(2 * t)

    def moveX(self, t, x):
        return self.getvx(t) * t + self.geta(x) * t ** 2 / 2

    def moveY(self, t, y):
        return self.getvy(t) * t + self.geta(y) * t ** 2 / 2

    def moveZ(self, t, z):
        return self.getvz(t) * t + self.geta(z) * t ** 2 / 2

    def __del__(self):
        print('Prikol removed')


class TSpaceCraft(TDynamicModel):  # why do we even have this?

    def __init__(self, fx, fy, fz, fv, alpha, beta, theta):
        super().__init__(fx, fy, fz, fv, alpha, beta, theta)


def main():
    TI = TIntegrator()

    mode = int(input('Enter 1 for Eulers method, 2 for Kuttas method\n'))

    if mode == 1 or mode == 2:
        t = float(input('Enter your prefered period of time\n'))
        dt = float(input('Enter your prefered dt\n'))

        wish = str(input('Do you REALLY want to write all that coordinates and stuff? Y/n\n'))
        if wish.lower() == 'y':
            print('Man youre boring\n')
            x = float(input('Enter your X\n'))
            y = float(input('Enter your Y\n'))
            z = float(input('Enter your Z\n'))
            v = float(input('Enter your speed V\n'))
            alpha = float(input('Enter your alpha angle between OX and V\n'))
            beta = float(input('Enter your beta angle between OY and V\n'))
            theta = float(input('Enter your theta angle between OZ and V\n'))
            KA = TDynamicModel(x, y, z, v, alpha, beta, theta)

        elif wish.lower() == 'n':
            KA = TDynamicModel(r.random() * 1000000 + 100000,
                               r.random() * 1000000 + 100000,
                               r.random() * 1000000 + 100000,
                               r.random() * 500000 + 50000,
                               r.random() * 2 * m.pi,
                               r.random() * 2 * m.pi,
                               r.random() * 2 * m.pi)

        else:
            print('What? I dont understand you')
            sys.exit()

        KA.x = TI.integrate(mode, KA.x, KA.moveX, 0, t, dt)
        xline = TI.coords
        KA.y = TI.integrate(mode, KA.y, KA.moveY, 0, t, dt)
        yline = TI.coords
        KA.z = TI.integrate(mode, KA.z, KA.moveZ, 0, t, dt)
        zline = TI.coords

        ax = plt.axes(projection='3d')
        ax.scatter3D(0, 0, 0, color='green')
        ax.plot3D(xline, yline, zline, 'gray')
        ax.set_xlabel('x, 10^6m')
        ax.set_ylabel('y, 10^6m')
        ax.set_zlabel('z, 10^6m')
        plt.show()

    else:
        print('wrong mode buddy')
        sys.exit()


if __name__ == "__main__":
    main()
