import math as m


def func(x):
    return m.cos(x)

def true_func(x):
    return m.sin(x)


def rect(fun, A, B):
    return (B - A) * fun((A + B) / 2)


def trapeze(fun, A, B):
    return (B - A) * (fun(A) + fun(B)) / 2


def simp(fun, A, B):
    dx = (B - A) / 2
    f0 = fun(A)
    f1 = fun((A + B) / 2)
    f2 = fun(B)
    return dx * (f0 + 4 * f1 + f2) / 3


def gen_rect(fun, A, B, N):
    dx = (B - A) / N
    result = 0
    for i in range(N):
        result += fun((A + dx * i + A + dx * (i + 1)) / 2)
    return result * dx


def gen_simp(fun, A, B, N):
    dx = (B - A) / N
    result = 0
    for i in range(N):
        result += fun(A + i * dx)
    return result


def main():
    A = -2
    B = +1
    N = 4

    true_value = true_func(B) - true_func(A)
    rect_value = rect(func, A, B)
    gen_rect_value = gen_rect(func, A, B, N)
    trapeze_value = trapeze(func, A, B)
    simpson_value = simp(func, A, B)
    gen_simpson_value = gen_simp(func, A, B, N)

    print(f'Действительное значение = {true_value}')
    print(f'Метод прямоугольников = {rect_value}')
    print(f'Погрешность метода прямоугольников = {true_value - rect_value}')
    print(f'Обобщенный метод прямоугольников = {gen_rect_value}')
    print(f'Погрешность обобщенного метода прямоугольников = {true_value - gen_rect_value}')
    print(f'Метод трапеций = {trapeze_value}')
    print(f'Погрешность метода трапеций = {true_value - trapeze_value}')
    print(f'Метод Симпсона = {simpson_value}')
    print(f'Погрешность метода Симпсона = {true_value - simpson_value}')
    print(f'Обобщенный метод Симпсона = {gen_simpson_value}')
    print(f'Погрешность обобщенного метода Симпсона = {true_value - gen_simpson_value}')


if __name__ == "__main__":
    main()
