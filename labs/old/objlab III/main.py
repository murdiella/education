import random as r
import math as m
import numpy as np
import matplotlib.pyplot as plt
import threading
import time
import psycopg2 as pscg

# здесь введены константы и функции для открытия файлов для всего кода
g = 9.81
exp_id = 0  # айди эксперимента, будет сохраняться в файле exp_id.db
global_id = 1  # айди ЛА, в последствии будем этот параметр менять
po = 1.007  # плотность атмосферы на высоте 2км
fw = open('log.txt', 'w')
fa = open('log.txt', 'a')
cred = open("credentials.txt", 'r')


# родительский класс
class TTarget:
    x = y = v = k = dfuel = fP = Xdrag = fm = float
    id = int

    def __init__(self, fx, fy, fv, fk, fmfuel):
        self.x = fx
        self.y = fy
        self.v = fv
        self.k = fk
        self.mfuel = fmfuel
        # присваеваем id для ЛА и увеличиваем для следующих ЛА
        global global_id
        self.id = global_id
        global_id += 1

    # удалятор
    def __del__(self):
        if isinstance(self, TMissle):
            print("Missle removed")
        if isinstance(self, TAircraft):
            print("Aircraft removed")


# класс самолетов
# у нас отечественные Ту-204
class TAircraft(TTarget):
    S = 12.325
    Cx = 0.3
    m = 60000
    mcrit = 32800
    dfuel = 53

    def __init__(self, fx, fy, fv, fk, fmfuel):
        super().__init__(fx, fy, fv, fk, fmfuel)
        self.P0 = self.v * 113500

    # система уравнений в задании для лабы 3 (с монитором, блекджеком и топливом впридачу)
    def SetXdrag(self):
        return self.Cx * po * self.v * self.v * self.S / 2

    def FuelMass(self, t):
        return self.mfuel - self.dfuel * t

    def Mass(self, t):
        return self.m + self.FuelMass(t)

    def SetP(self, t):
        fuel = self.FuelMass(t)
        if fuel > self.mcrit:
            return self.P0
        elif fuel < 0:
            return 0
        else:
            return self.P0 * fuel / self.mcrit

    def SetV(self, t):
        self.v = (self.SetP(t) - self.SetXdrag()) / self.Mass(t)
        return self.v

    # функции движения самолета
    def MoveX(self, t):
        return self.SetV(t) * m.cos(self.k)

    def MoveY(self, t):
        return self.SetV(t) * m.sin(self.k)


# класс ракет
# у нас американские АТМ-120
class TMissle(TTarget):
    S = 0.025
    Cx = 0.2
    m = 157
    mcrit = 30
    dfuel = 0.8

    def __init__(self, fx, fy, fv, fk, fmfuel):
        super().__init__(fx, fy, fv, fk, fmfuel)
        self.P0 = self.v * 227

    # все еще топливо и его система уравнений
    def SetXdrag(self):
        return self.Cx * po * self.v * self.v * self.S / 2

    def FuelMass(self, t):
        return self.mfuel - self.dfuel * t

    def Mass(self, t):
        return self.m + self.FuelMass(t)

    def SetP(self, t):
        fuel = self.FuelMass(t)
        if fuel > self.mcrit:
            return self.P0
        elif fuel < 0:
            return 0
        else:
            return self.P0 * fuel / self.mcrit

    def SetV(self, t):
        self.v = (self.SetP(t) - self.SetXdrag()) / self.Mass(t)
        return self.v

    # функции движения ракеты
    def MoveX(self, t):
        return self.SetV(t) * m.cos(self.k)

    def MoveY(self, t):
        return self.SetV(t) * m.sin(self.k)


# эта фигня отслеживает ЛА
class RLS:
    x = y = R0 = float
    Targets = []

    def __init__(self, fx, fy, fR0):
        self.x = fx
        self.y = fy
        self.R0 = fR0
        self.Targets = []

    def __del__(self):
        print("RLS removed")

    def Peleng(self, ft0, ftk, fdt):
        Te = TEuler()
        tk = ftk
        t = ft0
        dt = fdt

        # блок кода в котором мы:
        # 1 -- создаем соединение
        conn = pscg.connect(f"{cred.read()}")
        cur = conn.cursor()
        # 2 -- достаем id последнего эксперимента и инкрементируем его
        global exp_id
        cur.execute("SELECT exp_id FROM experiment")
        exp_id = cur.fetchall()[-1]
        exp_id = exp_id[0]
        exp_id += 1
        # 3 -- заносим в БД инфу по эксперименту
        cur.execute('INSERT INTO experiment (exp_id, exp_data, exp_t, exp_t0, exp_dt) VALUES (%s, %s, %s, %s, %s)',
                    (exp_id, ' ', tk, t, dt))
        cur.execute('INSERT INTO rls (exp_id, rls_x, rls_y, rls_radius) VALUES (%s, %s, %s, %s)',
                    (exp_id, self.x, self.y, self.R0))

        # а вот тут мы уже вносим в БД инфу про ЛА, которые мы нагенерировали
        for Ar in self.Targets:
            if isinstance(Ar, TAircraft):
                cur.execute(
                    'INSERT INTO aircrafts (exp_id, ac_id, ac_x0, ac_y0, ac_v0, ac_k, ac_type) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (exp_id, Ar.id, Ar.x, Ar.y, Ar.v, Ar.k, 'Aircraft'))
            if isinstance(Ar, TMissle):
                cur.execute(
                    'INSERT INTO aircrafts (exp_id, ac_id, ac_x0, ac_y0, ac_v0, ac_k, ac_type) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (exp_id, Ar.id, Ar.x, Ar.y, Ar.v, Ar.k, 'Missle'))

        # этот массив позже пригодится чтоб строить графики и заполнять таблицу с координатами в БД
        objects = []
        for _ in range(len(np.arange(t, tk, dt))):
            objects.append([None])

        # (б)логгер. у него нет канала в телеграмм НО ВСЕ РАВНО ПОДПИСЫВАЙТЕСЬ!!!
        # (на самом деле он лог заполняет. и БД)
        def logger():
            for Target in self.Targets:
                # интегрируем функции движения
                Target.x = Te.integrate(Target.x, Target.MoveX, t, tk, dt)
                coordsX = Te.coords
                Target.y = Te.integrate(Target.y, Target.MoveY, t, tk, dt)
                coordsY = Te.coords
                temppos = []
                for i in range(len(coordsX)):
                    # сразу внесем в БД все координаты во все участки времени
                    cur.execute('INSERT INTO ac_coords (exp_id, ac_id, curr_time, curr_x, curr_y) VALUES (%s, %s, %s, %s, %s)', (exp_id, Target.id, (i + 1) * dt, coordsX[i], coordsY[i]))
                    # вычислим дистанцию и азимут от РЛС до ЛА
                    Az = m.atan((coordsY[i] - self.y) / (coordsX[i] - self.y))
                    D = m.sqrt((coordsX[i] - self.x) * (coordsX[i] - self.x) + (coordsY[i] - self.y) * (coordsY[i] - self.y))
                    # если РЛС засекло, то заполняем лог и заносим в БД
                    if self.R0 >= D:
                        temppos.append(D)
                        cur.execute('INSERT INTO rls_log (exp_id, ac_id, curr_time, ac_distance, ac_azimuth) VALUES (%s, %s, %s, %s, %s)', (exp_id, Target.id, (i + 1) * dt, D, Az))
                        if isinstance(Target, TMissle):
                            fa.write(f"{(i + 1) * dt}; Missle #{Target.id}; D = {round(D, 2)}; Az = {round(Az, 2)}\n")
                        if isinstance(Target, TAircraft):
                            fa.write(f"{(i + 1) * dt}; Aircraft #{Target.id}; D = {round(D, 2)}; Az = {round(Az, 2)}\n")
                    else:
                        # если добавим None, на графике будет промежуток в случае если ЛА снова попадет в радиус обнаружения
                        temppos.append(None)

                # немного странная конструкция, но именно в таком виде графики по objects строятся адекватно
                j = 0
                for item in objects:
                    item.append(temppos[j])
                    j += 1

        # запускаем первый поток с блоггером
        my_logger = threading.Thread(target=logger)
        my_logger.start()

        # функция для плотника :)
        # будет строить графики
        def plotter():
            plt.plot(objects)
            plt.xlabel("Time")
            plt.ylabel("Distance between RLS and an object")
            plt.show()
            plt.pause(0.1)

        # опа бесконечные циклы подъехали (спойлер: их двое)
        n = 1
        while n > 0:
            n = 1
            # короче, пока блоггер не закончит, плотник не начнет строить в связи с тем что до конца работы
            # блоггера не создается файл, нужный для плотника, и он ниче не строит
            if not my_logger.is_alive():
                my_plotter = threading.Thread(target=plotter)
                my_plotter.start()
                break

        # еще один бесконечный цикл. нужен что бы соединение не закрылось до того, как БД не будет заполнена, и автор
        # данного кода (я) не просрал информацию
        while n > 0:
            n = 1
            if not my_logger.is_alive() and not my_plotter.is_alive():
                conn.commit()
                cur.close()
                fa.close()
                break


# мистор интегратор векторов
class TEuler:
    # тут будут жить промежуточные значения координат для их последующей обработки
    coords = []

    def integrate(self, vect, func, t0, tk, dt):
        self.coords = []
        time = np.arange(t0, tk, dt)
        self.coords.append(vect)
        for t in time:
            vect += func(t)*dt
            self.coords.append(vect)
        return vect


def main():
    # засекаем время
    start_time = time.time()

    # вводим время эксперимента
    print("Enter your t0:")
    t0 = float(input())
    print("Enter your tk:")
    t = float(input())
    print("Enter your dt:")
    dt = float(input())

    # обнуляем файл
    fw.write('Log File\n')
    fw.close()

    # вводим параметры РЛС
    print("Enter your RLS x and y:")
    rlsx = float(input())
    rlsy = float(input())
    print("Enter your RLS R:")
    rlsr = float(input())
    Rls = RLS(rlsx, rlsy, rlsr)

    # создаем ЛА
    print("How many Aircrafts do you need?")
    A = int(input())
    print("How many Missles do you need?")
    M = int(input())
    for i in range(A):
        Ar = TAircraft(r.random() * 20000, r.random() * 20000, r.random() * 600 + 300, r.random() * 2 * m.pi, r.random() * 25000 + 10000)
        Rls.Targets.append(Ar)
    for i in range(M):
        Ms = TMissle(r.random() * 20000, r.random() * 20000, r.random() * 600 + 600, r.random() * 2 * m.pi, r.random() * 25 + 10)
        Rls.Targets.append(Ms)

    print('\n')
    # запускаем!
    Rls.Peleng(t0, t, dt)
    # а тута смотрим сколько времени прошло за выполнение кода
    print("--- %s seconds ---" % (time.time() - start_time))


# чтоб скрипт не офигевал и не выполнялся когда его подключаем куда-нибудь
if __name__ == "__main__":
    main()
