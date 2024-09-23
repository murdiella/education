import mmlab1 as lab1
from numpy import cos, sqrt, arange
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod


class SObject(metaclass=ABCMeta):
    """Класс абстрактного космического объекта"""

    @abstractmethod
    def __init__(self):
        """Абстрактный конструктор класса"""
        self.pos = None
        self.mass = None


class SAC(SObject):
    """Класс КЛА"""

    def __init__(self, num_ns, type_ns, td, pos=None):
        """Конструктор КЛА"""

        super().__init__()
        # дефолт вэлъю как говорят наши коллеги американсы (с)
        if pos is None:
            self.pos = [0, 0, 10000]
        self.num = num_ns
        self.type = type_ns

        # на чето ж опираться надо да
        analysist = lab1.Analysis()
        analysist.load(self.num, self.type, td, graphs=False)
        self.data = analysist.data
        # вектор состояния [x, y, z, vx, vy, vz]T
        self.state = []
        self.record = []  # для построения графиков

        # по этому массиву будем отслеживать кто на нас влияет.
        # вообще, если так уже раскручиваться, можно было бы запихнуть это дело в SObject вместе с методом Dynamics
        # и сделать взаимное влияние всех на всех, если бы еще у всех были орбиты, динамика и тд
        self.influencers = []

    def dynamics(self, moon_pos=None, sun_pos=None, unknown=False, unknown_pos=None, unknown_mass=None, graphs=True):
        """Метод динамики КЛА"""

        # планеты запихиваем
        moon = Moon(pos=moon_pos)
        self.influencers.append(moon)
        sun = Sun(pos=sun_pos)
        self.influencers.append(sun)
        # короче да, можно поиграться с левыми объектами
        if unknown:
            planet = Unknown(unknown_mass, unknown_pos)
            self.influencers.append(planet)

        # метод для расчета ускорения влияющего объекта
        def inf_acc(obj: SPlanet, axis):
            g = 6.67e-11
            r2 = ((self.state[0] - obj.pos[0]) ** 2 + (self.state[1] - obj.pos[1]) ** 2 +
                  (self.state[2] - obj.pos[2]) ** 2)
            m = obj.mass

            if axis == 'x':
                proj_cos = cos(sqrt(r2) / (self.state[0] - obj.pos[0]))
            elif axis == 'y':
                proj_cos = cos(sqrt(r2) / (self.state[1] - obj.pos[1]))
            elif axis == 'z':
                proj_cos = cos(sqrt(r2) / (self.state[2] - obj.pos[2]))
            else:
                raise ValueError('Incorrect axis input')

            return g * m / r2 * proj_cos

        # формат данных self.data все еще [номер спутника, [время], [x], [y], [z]]
        self.state = [self.data[2][0], self.data[3][0], self.data[4][0], 0, 0, 0]
        self.record.append(self.state)
        for i in range(len(self.data[1]) - 1):
            if self.data[0] == self.num:
                dt = abs(self.data[1][i + 1] - self.data[1][i])
                v_xadd = (self.data[2][i + 1] - self.data[2][i]) / dt
                v_yadd = (self.data[3][i + 1] - self.data[3][i]) / dt
                v_zadd = (self.data[4][i + 1] - self.data[4][i]) / dt
                ax = 0
                ay = 0
                az = 0
                for influencer in self.influencers:
                    ax += inf_acc(influencer, axis='x')
                    ay += inf_acc(influencer, axis='y')
                    az += inf_acc(influencer, axis='z')
                v_xnew = ax * dt + v_xadd
                v_ynew = ay * dt + v_yadd
                v_znew = az * dt + v_zadd
                xnew = self.state[0] + v_xnew * dt
                ynew = self.state[1] + v_ynew * dt
                znew = self.state[2] + v_znew * dt
                self.state = [xnew, ynew, znew, v_xnew, v_ynew, v_znew]
                self.record.append(self.state)

        if graphs:
            x_data = []
            y_data = []
            z_data = []
            vx_data = []
            vy_data = []
            vz_data = []
            for item in self.record:
                x_data.append(item[0])
                y_data.append(item[1])
                z_data.append(item[2])
                vx_data.append(item[3])
                vy_data.append(item[4])
                vz_data.append(item[5])

            x0 = self.record[0][0]
            y0 = self.record[0][1]
            z0 = self.record[0][2]
            ax = plt.figure().add_subplot(projection='3d')

            ax.scatter(0, 0, 0, color='green', s=6400)  # ПЛАНЕТА

            # ax.scatter(0, 0, 0, color='black')
            # ax.text(0, 0, 0, 'earth center', color='black')

            ax.scatter(x0, y0, z0, color='red')
            ax.text(x0, y0, z0, 'start', color='red')
            ax.plot(x_data, y_data, z_data, color='blue', markersize=0.5)

            ax.set_xlabel('x, km')
            ax.set_ylabel('y, km')
            ax.set_zlabel('z, km')
            plt.show()

            fig, ax = plt.subplots(1, 3)
            time = arange(0, 1440, 15)
            ax[0].plot(time, vx_data)
            ax[0].set_title("X speeds")
            ax[1].plot(time, vy_data)
            ax[1].set_title("Y speeds")
            ax[2].plot(time, vz_data)
            ax[2].set_title("Z speeds")
            plt.show()


class SPlanet(SObject):
    """Класс абстрактной планеты (или другой <<неподвижной>> херни в космосе)"""

    @abstractmethod
    def __init__(self):
        """Абстрактный конструктор планеты"""
        super().__init__()
        pass


class Moon(SPlanet):
    """Класс планеты-Луны"""
    # несмотря на то, что Луна -- не планета вовсе...

    def __init__(self, pos=None):
        """Конструктор Луны"""
        # звучит как набор лего

        super().__init__()
        # очень реальные параметры (из гугла разумеется)
        self.mass = 7.36e22
        if pos is None:
            self.pos = [384400, 0, 0]
        else:
            self.pos = pos


class Sun(SPlanet):
    """Класс планеты-Солнца"""
    # а Солнце это вообще звезда...

    def __init__(self, pos=None):
        """Конструктор Солнца"""
        # а это звучит как сай-фай новелла

        super().__init__()
        # вновь очень реальные параметры (все еще из гугла)
        self.mass = 1.99e30
        if pos is None:
            self.pos = [0, 149_597_870, 0]
        else:
            self.pos = pos


class Unknown(SPlanet):
    """Класс неизвестной и очень таинственной планеты"""

    def __init__(self, mass, pos):
        """Конструктор неизвестной и очень таинственной планеты"""

        # короче можно любую планетку впаять
        super().__init__()
        if isinstance(mass, float) and isinstance(pos, list) and len(pos) == 3:
            self.mass = mass
            self.pos = pos
        else:
            raise ValueError('Incorrect planet config input')


def main():
    rinex_file = 'Brdc0880.24n'
    sp3_file = 'Sta23074.sp3.glo'
    satellite = SAC(1, 'GLONASS', sp3_file)
    moon_pos = [384400, 0, 0]
    sun_pos = [0, 0, 149_597_870]
    satellite.dynamics(moon_pos=moon_pos, sun_pos=sun_pos)


if __name__ == "__main__":
    main()
