import math as m
import random
import numpy as np
import matplotlib.pyplot as plt

U = 3.986*pow(10, 14)
et = 10


class TDynamicModel(object):
    def __init__(self, X0, Y0, Z0, VX, VY, VZ):
        self.x_0 = X0
        self.y_0 = Y0
        self.z_0 = Z0
        self.x = X0
        self.y = Y0
        self.z = Z0
        self.v_x = VX
        self.v_y = VY
        self.v_z = VZ
        self.r = m.sqrt(X0*X0+Y0*Y0+Z0*Z0)
        self.a_x = (-U*X0) / pow(self.r, 3)
        self.a_y = (-U * Y0) / pow(self.r, 3)
        self.a_z = (-U * Z0) / pow(self.r, 3)

    def SetX(self, x):
        self.x = x

    def GetX(self):
        return self.x

    def SetY(self, x):
        self.y = x

    def GetY(self):
        return self.y

    def SetZ(self, x):
        self.z = x

    def GetZ(self):
        return self.z

    def SetVX(self, x):
        self.v_x = x

    def GetVX(self):
        return self.v_x

    def SetVY(self, x):
        self.v_y = x

    def GetVY(self):
        return self.v_y

    def SetVZ(self, x):
        self.v_z = x

    def GetVZ(self):
        return self.v_z

    def MoveX(self, xi):
        self.x += xi*et
        self.r = m.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        x = self.ChangeVX(xi)
        return x

    def MoveY(self, yi):
        self.y += yi*et
        self.r = m.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        y = self.ChangeVY(yi)
        return y

    def MoveZ(self, zi):
        self.z += zi*et
        self.r = m.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        z = self.ChangeVZ(zi)
        return z

    def ChangeVX(self, xi):
        self.v_x += self.ChangeA(xi)*et
        vx = self.ChangeA(xi)
        return vx

    def ChangeVY(self, yi):
        self.v_y += self.ChangeA(yi)*et
        vy = self.ChangeA(yi)
        return vy

    def ChangeVZ(self, zi):
        self.v_z += self.ChangeA(zi)*et
        vz = self.ChangeA(zi)
        return vz

    def ChangeA(self, xi):
        return (-U*xi) / pow(self.ChangeR(), 3)

    def ChangeR(self):
        return m.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    TMove = [MoveX, MoveY, MoveZ, ChangeVX, ChangeVY, ChangeVZ]
    TGet = [GetX, GetY, GetZ, GetVX, GetVY, GetVZ]


class TSpaceCraft(TDynamicModel):
    def __init__(self, X, Y, Z, VX, VY, VZ):
        super(TSpaceCraft, self).__init__(X, Y, Z, VX, VY, VZ)


class TAbstractIntegrator(object):
    def __init__(self, T0, TK, H):
        self.name = "AbstractIntegrator"
        self.t_0 = T0
        self.t_k = TK
        self.dt = H

    def OneStep(self, TSC, prevs, dt):
        lefts = []

        for i in range(len(TSC.TMove)):
            lefts.append(TSC.TMove[i](TSC, prevs[i]))

        print(lefts)
        return lefts

    def MoveTo(self, TSC):
        t = np.arange(self.t_0, self.t_k, self.dt)

        vars = []
        prev = []
        prevx = []
        for i in range(len(TSC.TMove)):
            x = []
            x.append(TSC.TGet[i](TSC))
            prevx.append(TSC.TGet[i](TSC))
            vars.append(x)
        prev.append(prevx)

        for i in range(len(t)):
            prevx = []
            leftss = self.OneStep(TSC, prev[-1], self.dt)
            for j in range(len(TSC.TMove)):
                xj = vars[j][-1] + leftss[j]*self.dt
                # print(xj)
                prevx.append(xj)
                vars[j].append(xj)
            prev.append(prevx)
            # print(prev)
        return vars


class Runge(TAbstractIntegrator):
    def __init__(self, T0, TK, H):
        self.name = "Runge-Kutta"
        super(Runge, self).__init__(T0, TK, H)

    def OneStep(self, TSC, prevs, dt):
        lefts = []
        for i in range(len(TSC.TMove)):
            k1 = TSC.TMove[i](TSC, prevs[i])
            k2 = TSC.TMove[i](TSC, (prevs[i] + k1*(dt/2)))
            k3 = TSC.TMove[i](TSC, (prevs[i] + k2*(dt/2)))
            k4 = TSC.TMove[i](TSC, (prevs[i] + k3*dt))
            summ = (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
            lefts.append(summ)

        # print(lefts)
        return lefts


class Euler(TAbstractIntegrator):
    def __init__(self, T0, TK, H):
        self.name = "Euler"
        super(Euler, self).__init__(T0, TK, H)


def main():
    t_0 = 0
    t_k = 80000
    dt = 10
    # md = TSpaceCraft(random.uniform(0, 100000), random.uniform(0, 100000), random.uniform(0, 100000), random.uniform(0, 100000), random.uniform(0, 1000000), random.uniform(0, 1000))
    md = TSpaceCraft(-2000000, 100000, 19000000, 100000, -360000, 3600)
    intr = Runge(t_0, t_k, dt)
    # t = np.linspace(0, t_k, int((t_k - t_0) / dt) + 1)
    mas = intr.MoveTo(md)
    # print(mas)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot(mas[0], mas[1], mas[2])
    plt.show()


if __name__ == "__main__":
    main()
