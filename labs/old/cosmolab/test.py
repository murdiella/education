import unittest as ut
import main as mn


class Test(ut.TestCase):

    def testEuler(self):
        TI = mn.TIntegrator()
        v = 1

        def func(t, x):
            return t * t - 2 * x

        f = TI.integrate(1, v, func, 0, 1, 0.1)
        self.assertEqual(round(f, 4), 0.3082)

    def testKutta(self):
        TI = mn.TIntegrator()
        v = 1

        def func(t, x):
            return t * t - 2 * x

        f = TI.integrate(2, v, func, 0, 1, 0.1)
        self.assertEqual(round(f, 4), 0.3515)

    def testPrikol(self):
        TI = mn.TIntegrator()
        KA = mn.TDynamicModel(100000,
                              100000,
                              100000,
                              200000,
                              0, 0, 0)
        KA.x = TI.integrate(2, KA.x, KA.moveX, 0, 0.1, 0.1)
        self.assertEqual(round(KA.x, 2), 101196.21)
