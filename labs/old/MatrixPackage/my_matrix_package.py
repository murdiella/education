from math import sqrt
from copy import deepcopy


# класс матриц
# в коде местами не соблюдался pep8 т.к. я только в процессе его изучения
class TMatrix:
    data = []

    # клонирование матриц
    def clone(self):
        return deepcopy(self)

    # конструктор матриц
    def __init__(self, lists):
        if not isinstance(lists, list):
            raise Exception("Матрицу нужно задать списком списков")
        temp = []
        rowLength = 0  # будем проверять этой переменной длины строк (что бы их размер был одинаков в матрице)
        for arg in lists:
            if isinstance(arg, list):
                if rowLength == 0:
                    rowLength = len(arg)
                elif len(arg) != rowLength:
                    raise Exception("Строки матрицы должны быть одной длины")
                for item in arg:
                    if not (isinstance(item, int) or isinstance(item, float)):
                        raise Exception("Можно вводить только числа")
                temp.append(arg)
            else:
                raise Exception("Строка матрицы должна быть списком")
        if rowLength == 0:
            raise Exception("Строки матрицы не должны быть пустыми")
        self.data = temp

    # сложение матриц
    def add(self, matr):
        result = []
        temp = []
        if isinstance(matr, TMatrix):
            if matr.get_col_count() == self.get_col_count() and matr.get_row_count() == self.get_row_count():
                for i in range(self.get_row_count()):
                    for j in range(self.get_col_count()):
                        temp.append(self.data[i][j] + matr.data[i][j])
                    result.append(temp)
                    temp = []
                return TMatrix(result)
            else:
                raise Exception("Матрицы не одного размера")
        else:
            raise Exception("С матрицей можно сложить только матрицу")

    # сложение матриц
    def sub(self, matr):
        result = []
        temp = []
        if isinstance(matr, TMatrix):
            if matr.get_col_count() == self.get_col_count() and matr.get_row_count() == self.get_row_count():
                for i in range(self.get_row_count()):
                    for j in range(self.get_col_count()):
                        temp.append(self.data[i][j] - matr.data[i][j])
                    result.append(temp)
                    temp = []
                return TMatrix(result)
            else:
                raise Exception("Матрицы не одного размера")
        else:
            raise Exception("Из матрицы можно вычесть только матрицу")

    # проверить на симметричность
    def check_symmetric(self):
        if self.get_col_count() != self.get_col_count():
            raise Exception("Матрица не квадратрная")
        for i in range(self.get_row_count()):
            for j in range(self.get_col_count()):
                if self.data[i][j] != self.data[j][i]:
                    return False
        return True

    # транспонировать матрицу
    def flip(self):
        result = []
        temp = []
        for i in range(self.get_col_count()):
            for j in range(self.get_row_count()):
                temp.append(self.data[j][i])
            result.append(temp)
            temp = []
        return TMatrix(result)

    # получить значение элемента i-той строки j-того столбца
    # j здесь вообще не требуется в описании т.к. при вызове TMatrix[i][j] вызов
    # дважды входит в __getitem__
    def __getitem__(self, i):
        if i + 1 > self.get_row_count() or i < 0:
            raise Exception("Неверно указаны индексы требуемого элемента")
        return self.data[i]

    # получить количество столбцов
    def get_col_count(self):
        return len(self.data[0])

    # получить количество строк
    def get_row_count(self):
        RowCount = 0
        for _ in self.data:
            RowCount += 1
        return RowCount

    # вычислитель обратной матрицы
    # если я правильно помню, разложение холецкого делать не нужно было
    def inverse(self):
        if self.get_row_count() != self.get_col_count():
            raise Exception("Матрица не квадратная")

        # делаем единичную матрицу размерности исходной
        result = self.clone().data
        identityMatrixData = []
        temp = []
        for i in range(self.get_row_count()):
            for j in range(self.get_row_count()):
                temp.append(0)
            temp[i] = 1
            identityMatrixData.append(temp)  # единичная матрица нужной нам размерности
            temp = []

        # склеиваем единичную матрицу с изначальной
        for i in range(self.get_row_count()):
            for j in range(len(identityMatrixData)):
                result[i].append(identityMatrixData[i][j])

        # делаем треугольную матрицу (прямой ход метода Гаусса)
        for i in range(self.get_row_count()):
            for j in range(len(result[i])):
                if result[i][i] == 0:
                    for k in range(i + 1, self.get_row_count()):
                        if result[k][k] != 0:
                            result[i], result[k] = result[k], result[i]
                            break
                if result[i][i] == 0:
                    raise Exception("Невозможно найти обратную матрицу")
            for k in range(i + 1, self.get_row_count()):
                ratio = result[k][i]
                for j in range(i, len(result[i])):
                    result[k][j] = result[k][j] - ratio * result[i][j]

        # проверка на нули главной диагонали
        for i in range(self.get_row_count()):
            if result[i][i] == 0:
                raise Exception("Невозможно найти обратную матрицу")

        # делаем главную диагональ основной матрицы единичной
        for i in range(self.get_row_count()):
            div = result[i][i]
            for j in range(len(result[i])):
                result[i][j] = result[i][j] / div

        # обратный ход метода Гаусса
        for i in range(self.get_row_count() - 1, 0, -1):
            for k in range(i - 1, -1, -1):
                ratio = result[k][i]
                for j in range(i, len(result[i])):
                    result[k][j] = result[k][j] - ratio * result[i][j]

        # удаляем ненужную полученную единичную матрицу
        for i in range(self.get_row_count()):
            for j in range(self.get_row_count()):
                result[i].pop(0)

        return TMatrix(result)

    # произведение матрицы на число, вектор или матрицу
    def mult(self, x):
        result = []

        if isinstance(x, int) or isinstance(x, float):
            temp = []
            for i in range(self.get_row_count()):
                for j in range(self.get_col_count()):
                    temp.append(self.data[i][j] * x)
                result.append(temp)
                temp = []
            return TMatrix(result)

        if isinstance(x, TVector):
            temp = 0
            if self.get_col_count() == x.get_length():
                for i in range(self.get_row_count()):
                    for j in range(self.get_col_count()):
                        temp += self.data[i][j] * x.data[j]
                    result.append(temp)
                    temp = 0
                return TVector(result)
            else:
                raise Exception("Количество столбцов матрицы не совпадает с длиной вектора")

        if isinstance(x, TMatrix):
            temp1 = []
            temp2 = 0
            if self.get_col_count() == x.get_row_count():
                for i in range(self.get_row_count()):
                    for j in range(x.get_col_count()):
                        for k in range(self.get_col_count()):
                            temp2 += self.data[i][k] * x.data[k][j]
                        temp1.append(temp2)
                        temp2 = 0
                    result.append(temp1)
                    temp1 = []
                return TMatrix(result)
            else:
                raise Exception("Количество столбцов первой матрицы не совпадает с количеством строк второй матрицы")

        else:
            raise Exception("Неверный тип множителя в произведении")

    # установить выбранный элемент
    # если матрица симметрична, меняется и симметричный ей элемент (в задании была
    # функция для симметричных матриц с заменой, я так понимаю как раз для этой фишки).
    def __setitem__(self, i, j, x):
        if i + 1 > self.get_row_count() or i < 0 or j + 1 > self.get_col_count() or j < 0:
            raise Exception("Неверно указаны индексы требуемого элемента")
        if not (isinstance(x, int) or isinstance(x, float)):
            raise Exception("Вставляемый элемент должен быть числом")
        self.data[i][j] = x

    # установить размер матрицы
    # если увеличиваем, новые ячейки матрицы заполняем нулями
    # если уменьшаем, то удаляются ячейки со старшими индексами
    def set_size(self, i, j):
        if i < 0 or j < 0:
            raise Exception("Матрица не может быть отрицательной размерности")
        else:
            if i > self.get_row_count():
                temp = []
                for _ in range(i - self.get_row_count()):
                    for k in range(self.get_col_count()):
                        temp.append(0)
                    self.data.append(temp)
            else:
                for _ in range(self.get_row_count() - i):
                    self.data.pop(-1)
            if j > self.get_col_count():
                for _ in range(j - self.get_col_count()):
                    for k in range(self.get_row_count()):
                        self.data[k].append(0)
            else:
                for _ in range(self.get_col_count() - j):
                    for k in range(self.get_row_count()):
                        self.data[k].pop(-1)

    # функция для вывода матриц, изначально не было в структуре классов
    # я подзабил на форматирование строки, потому если числа в строке разной длины то может съехать
    # могу как то это поправить, напишите об этом в ответном письме
    # (не уверен, что оно нужно, ведь элементы отлично читаются через запятые)
    def print(self):
        for row in self.data:
            print(f"{row}")

    # перегрузка оператора для сложения
    def __add__(self, other):
        return self.add(other)

    # перегрузка оператора для вычитания
    def __sub__(self, other):
        return self.sub(other)

    # перегрузка операторов для умножения
    def __mul__(self, other):
        return self.mult(other)

    def __rmul__(self, other):
        return self * other

    # перегрузка оператора для транспонирования
    def __invert__(self):
        return self.flip()

    # перегрузка оператора для обратной матрицы
    def __neg__(self):
        return self.inverse()


class TVector:
    data = []

    # клонирование векторов
    def clone(self):
        return deepcopy(self)

    # конструктор вектора
    def __init__(self, array):
        if isinstance(array, list):
            if len(array) == 0:
                raise Exception("Вектор не должен быть пустой")
            for arg in array:
                if not (isinstance(arg, int) or isinstance(arg, float)):
                    raise Exception("Можно вводить только числа")
            self.data = array
        else:
            raise Exception("Ввод вектора должен осуществляться списком")

    # сложение векторов
    def add(self, vect):
        result = []
        if isinstance(vect, TVector):
            if self.get_length() == vect.get_length():
                for _ in range(self.get_length()):
                    result.append(None)
                for i in range(self.get_length()):
                    result[i] = self.data[i] + vect.data[i]
                return TVector(result)
            else:
                raise Exception("Векторы не одной длины")
        else:
            raise Exception("Вектор можно складывать только с другим вектором")

    # вычитание векторов
    def sub(self, vect):
        result = []
        if isinstance(vect, TVector):
            if self.get_length() == vect.get_length():
                for _ in range(self.get_length()):
                    result.append(None)
                for i in range(self.get_length()):
                    result[i] = self.data[i] - vect.data[i]
                return TVector(result)
            else:
                raise Exception("Векторы не одной длины")
        else:
            raise Exception("Вектор можно складывать только с другим вектором")

    # векторное умножение
    def cross_product(self, vect):
        result = []
        if isinstance(vect, TVector):
            if self.get_length() == vect.get_length():
                if self.get_length() == 3:
                    result.append(self.data[1] * vect.data[2] - self.data[2] * vect.data[1])
                    result.append(self.data[2] * vect.data[0] - self.data[0] * vect.data[2])
                    result.append(self.data[0] * vect.data[1] - self.data[1] * vect.data[0])
                    return TVector(result)
                else:
                    raise Exception("Векторное произведение применимо только для трехмерных векторов")
            else:
                raise Exception("Векторы не одной длины")
        else:
            raise Exception("Векторное произведение вектора применимо только на другой вектор")

    # получить значение элемента вектора
    def __getitem__(self, i):
        try:
            return self.data[i]
        except IndexError:
            print("Такого элемента не существует")

    # получаем длину вектора (т.е. кол-во элементов в нем)
    def get_length(self):
        return len(self.data)

    # получаем длину вектора (т.е. корень суммы квадратов элементов)
    def get_magnitude(self):
        result = 0
        for i in range(self.get_length()):
            result += self[i] * self[i]
        return sqrt(result)

    # произведение вектора на число, вектор или матрицу
    def mult(self, x):
        result = []

        if isinstance(x, int) or isinstance(x, float):
            for i in range(self.get_length()):
                result.append(self.data[i] * x)
            return TVector(result)

        if isinstance(x, TVector):  # я так понимаю, это ТО САМОЕ МЕСТО для скалярного произведения
            result = 0
            if isinstance(x, TVector):
                if self.get_length() == x.get_length():
                    for i in range(self.get_length()):
                        result += self.data[i] * x.data[i]
                    return result
                else:
                    raise Exception("Векторы не одной длины")
            else:
                raise Exception("Скалярное произведение вектора применимо только на другой вектор")

        if isinstance(x, TMatrix):   # тут мы умножаем вектор-строку на матрицу исходя из соображений, что умножается вектор-строка
            result = []
            temp = 0
            if self.get_length() == x.get_row_count():
                for i in range(x.get_col_count()):
                    for j in range(x.get_row_count()):
                        temp += self.data[j] * x.data[j][i]
                    result.append(temp)
                    temp = 0
                return TVector(result)
            else:
                raise Exception("Количество строк в матрице не совпадает с количеством элементов вектор-строки")

        else:
            raise Exception("Неверный тип множителя в произведении")

    # устанавливаем элемент
    def __setitem__(self, i, x):
        try:
            self.data[i] = x
        except IndexError:
            print("Такого номера элемента в векторе нет")

    # меняем длину вектора
    def set_length(self, n):
        if n < 0:
            raise Exception("Вектор не может быть отрицательной длины")
        else:
            if n > self.get_length():
                for i in range(n - self.get_length()):
                    self.data.append(0)  # заполняем нулями все новые элементы
            else:
                for i in range(self.get_length() - n):
                    self.data.pop(-1)  # удаляем последние лишние элементы

    # функция для вывода вектора, изначально не было в структуре классов
    def print(self):
        print(self.data)

    # перегрузка оператора для сложения
    def __add__(self, other):
        return self.add(other)

    # перегрузка оператора для вычитания
    def __sub__(self, other):
        return self.sub(other)

    # перегрузка операторов для умножения
    def __mul__(self, other):
        return self.mult(other)

    def __rmul__(self, other):
        return self * other

    # перегрузка оператора для векторного умножения (на крестик, кроме знака %, более похожего не нашлось)
    def __mod__(self, other):
        return self.cross_product(other)


# пользовательский интерфейс
# здесь можно вписать свой код для проверки библиотеки
def main():

    # В данной функции можно прописать свои примеры для
    # тестов. Ниже приведен пример вызова функций (с учетом
    # перегрузки переменных), а так же прописаны несколько
    # матриц и векторов как пример создания собственного.
    #
    # Я не совсем уверен, как я должен написать пользовательский
    # интерфейс, потому решил написать данный мануал для
    # последующей работы с модулем других пользователей.
    #
    # Названия функций взяты напрямую из задания, к каждой функции
    # добавлен комментарий по поводу ее содержания
    #
    # Была добавлена функция .print() для облегченного вывода матриц
    # и векторов (пример: A.print())
    #
    # Перегружены следующие операнды:
    # + -- сложение для векторов и матриц (пример: А + В)
    # * -- умножение для векторов и скалярное для матриц (пример: А * В)
    # -Х -- обратная матрица (в данном случае, обратная матрице Х)
    # ~ -- транспонирование матриц (пример: ~А)
    # % -- векторное произведение для векторов
    #
    # Так же поддерживаются комбинированные формулы (см. ниже).
    # Мною были написаны тесты для проверки работоспобности модуля
    # в случае изменения его содержания. С ними можно ознакомиться в test.py

    A = TMatrix([[1, 2, 3], [4, 8, 10], [7, 8, 9]])
    (A - -A).print()

    # (-C + C * -1.2).print()
    # print("")
    # (A % B).print()


# main() запустится только в случае, если мы напрямую запускаем библиотеку
# команды в main() не будут выполняться при подключении библиотеки к стороннему проекту
if __name__ == '__main__':
    main()
