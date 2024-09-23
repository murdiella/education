import unittest as ut
import math as m
import main as mn


class Test(ut.TestCase):

    def testAircraftMove(self):
        Ar = mn.TAircraft(10000, 5000, 400, m.pi / 3, 25000)
        Ar.x += Ar.MoveX(1) * 1
        Ar.y += Ar.MoveY(1) * 1
        self.assertEqual(round(Ar.x, 2), 10201.49)
        self.assertEqual(round(Ar.y, 2), 5348.95)

    def testMissleMove(self):
        Mi = mn.TMissle(4000, 8000, 1000, m.pi / 3, 25)
        Mi.x += Mi.MoveX(1) * 1
        Mi.y += Mi.MoveY(1) * 1
        self.assertEqual(round(Mi.x, 2), 4498.33)
        self.assertEqual(round(Mi.y, 2), 8863.22)

    def testIntegrator(self):
        def func(t):
            return t * t * t + 2 * t * t + t + 3

        x = 0
        TE = mn.TEuler()
        x = TE.integrate(x, func, 1, 3, 0.001)
        self.assertEqual(round(x, 1), 47.3)

    def testRlsPeleng(self):
        Ar = mn.TAircraft(4000, 4000, 700, 0, 18000)
        Ms = mn.TMissle(4000, 4000, 1000, m.pi, 20)
        Rls = mn.RLS(0, 0, 5000)
        Rls.Targets.append(Ar)
        Rls.Targets.append(Ms)
        Rls.Peleng(1, 5, 1)

        f = open('log.txt', 'r')
        lines = []
        for line in f:
            lines.append(line)
        truelines = ['3; Missle #1; D = 4667.56; Az = 1.03\n',
                     '4; Missle #1; D = 4327.55; Az = 1.18\n',
                     '5; Missle #1; D = 4106.32; Az = 1.34\n']
        self.assertEqual(lines, truelines)
        f.close()


if __name__ == '__main__':
    ut.main()
