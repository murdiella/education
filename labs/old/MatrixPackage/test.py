import unittest as ut
from math import sqrt
import my_matrix_package as mp


# класс для всех тестов нашего модуля
class Test(ut.TestCase):

    def testVector(self):
        A = mp.TVector([3, 2, 1])
        B = mp.TVector([3, 4, 5])
        C = mp.TMatrix([[1, 2, 3],
                        [2, 4, 5],
                        [3, 5, 7]])

        self.assertEqual(A.data, [3, 2, 1])                            # проверяем конструктор
        self.assertEqual(A.get_length(), 3)                             # проверяем длину вектора (кол-во элементов в нем)
        self.assertEqual(A.get_magnitude(), sqrt(14))                   # проверяем модуль длины вектора
        self.assertEqual(A[2], 1)                                      # проверяем элемент
        self.assertEqual(A.add(B).data, [6, 6, 6])                     # проверяем сложение векторов
        self.assertEqual(A.mult(B), 22)                                # проверяем скалярное произведение векторов
        self.assertEqual(A.cross_product(B).data, [6, -12, 6])          # проверяем векторное произведение векторов
        self.assertEqual(A.mult(1.5).data, [4.5, 3, 1.5])              # проверяем произведение вектора на число
        self.assertEqual(A.mult(C).data, [10, 19, 26])                 # проверяем умножение вектор-строки на матрицу

        A[0] = 5
        self.assertEqual(A.data, [5, 2, 1])                            # проверяем замену элемента
        A.set_length(5)
        self.assertEqual(A.data, [5, 2, 1, 0, 0])                      # проверяем удлинение вектора
        A.set_length(2)
        self.assertEqual(A.data, [5, 2])                               # проверяем укорочение вектора

    def testMatrix(self):
        A = mp.TMatrix([[1, 2, 3],
                        [2, 4, 5],
                        [3, 5, 7]])

        B = mp.TMatrix([[1, 2, 3],
                        [1, 3, 2],
                        [2, 1, 3]])

        C = mp.TMatrix([[1, 2],
                        [3, 4],
                        [5, 6]])

        D = mp.TVector([1, 2])

        E = mp.TMatrix([[1, 2, 3],
                        [4, 5, 6]])

        F = mp.TMatrix([[1, 2],
                        [3, 4]])

        self.assertEqual(A.data, [[1, 2, 3],
                                  [2, 4, 5],
                                  [3, 5, 7]])                          # проверяем конструктор
        self.assertEqual(C.get_col_count(), 2)                           # проверяем счет столбцов
        self.assertEqual(C.get_row_count(), 3)                           # проверяем счет строк
        self.assertEqual(A[2][1], 5)                                   # проверяем получение элемента
        self.assertEqual(A.check_symmetric(), True)                     # проверяем определение матрицы как симметричной
        self.assertEqual(B.check_symmetric(), False)                    # проверяем определение матрицы как несимметричной
        self.assertEqual(A.add(B).data, [[2, 4, 6],                    # проверяем сложение
                                         [3, 7, 7],
                                         [5, 6, 10]])
        self.assertEqual(C.flip().data, [[1, 3, 5],                    # проверяем транспонирование
                                         [2, 4, 6]])
        self.assertEqual(C.mult(1.5).data, [[1.5, 3.0],                # проверяем умножение на число
                                            [4.5, 6.0],
                                            [7.5, 9.0]])
        self.assertEqual(C.mult(D).data, [5, 11, 17])                  # проверяем умножение на вектор
        self.assertEqual(C.mult(E).data, [[9, 12, 15],                 # проверяем умножение на матрицу
                                          [19, 26, 33],
                                          [29, 40, 51]])
        self.assertEqual(F.inverse().data, [[-2.0, 1.0],               # проверяем вычисление обратной матрицы
                                            [1.5, -0.5]])

        B[0][1] = 3
        self.assertEqual(B.data, [[1, 3, 3],                           # проверяем изменение элемента
                                  [1, 3, 2],
                                  [2, 1, 3]])
        B.set_size(2, 2)
        self.assertEqual(B.data, [[1, 3],                              # проверяем уменьшение матрицы
                                  [1, 3]])
        B.set_size(2, 3)
        self.assertEqual(B.data, [[1, 3, 0],                           # проверяем увеличение матрицы
                                  [1, 3, 0]])


if __name__ == '__main__':
    ut.main()
