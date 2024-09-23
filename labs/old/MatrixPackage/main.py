import integrator as intg
import custom as cs


def main():
    # создание объекта интегратора
    integrator = intg.TDormandPrinceIntegrator()
    # установка максимально допустимой ошибки интегрирования на каждом шаге
    integrator.set_precision(1e-16)
    # создание объектов моделей
    model1 = cs.TArenstorfModel1(0, 20, 0.1)
    model2 = cs.TArenstorfModel2(0, 20, 0.1)
    # запуск интегрирования системы ДУ модели 1
    integrator.run(model1)
    # копирование результатов из объекта модели 1 в отдельную матрицу
    result = model1.get_result()
    # запись результатов в файл или построение графика
    print(result)
    # запуск интегрирования системы ДУ модели 2
    integrator.run(model2)
    result = model2.get_result()
    # запись результатов в файл или построение графика
    print(result)


if __name__ == "__main__":
    main()