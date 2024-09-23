import unittest as ut
import main as mn
import numpy as np


class Test(ut.TestCase):

    def testFuncs(self):
        X = [1, 2, 5, 6]
        Y = [3, 4, 5, 7]
        matr = np.array([[1, 2],
                         [3, 4]])
        vect = np.array([1, 2])

        self.assertEqual(mn.avg(X), 3.5)
        self.assertEqual(mn.avg(Y), 4.75)
        self.assertEqual(round(mn.corr(X, Y), 3), 0.943)
        # округлить(обратная матрица, 1 после запятой).в список()
        self.assertEqual(np.around(np.linalg.inv(matr), 1).tolist(), [[-2, 1],
                                                                      [1.5, -0.5]])
        self.assertEqual(np.matmul(matr, matr).tolist(), [[7, 10],
                                                          [15, 22]])
        self.assertEqual(np.matmul(matr, vect).tolist(), [5, 11])

    def testLin(self):
        X = [0, 1, -1]
        Y = [1, 0, 1]

        self.assertEqual(np.around(mn.linModel(X, Y), 2).tolist(), [-0.5, 0.67])


if __name__ == '__main__':
    ut.main()
