import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from skimage.util import random_noise


def methodical_search(noise_img: np.ndarray, template: np.ndarray):
    """Метод поиска эталона на изображении, представленный в методичке"""

    correlation_func = cv.matchTemplate(noise_img, method=cv.TM_CCORR_NORMED, templ=template)
    # correlation_func = cv.matchTemplate(noise_img, method=cv.TM_SQDIFF, templ=template)
    # correlation_func = cv.matchTemplate(noise_img, method=cv.TM_SQDIFF_NORMED, templ=template)

    # максимум корреляционной функции
    max_index = correlation_func.argmax()

    # индексы соответствующие максимуму функции
    i_max = int(max_index % correlation_func.shape[1])  # % это остаток от деления
    j_max = int(max_index / correlation_func.shape[1])

    # копирование изображения, переход к пространству BGR
    image_copy = noise_img
    image_copy = cv.cvtColor(image_copy, cv.COLOR_GRAY2BGR)

    # построение прямоугольника на изображении, соответствующий области нахождения эталона
    # i_max, j_max - вершина прямоугольника
    # (i_max + I, j_max + J) - вершина напротив первой точки
    I, J = np.shape(template)
    image_copy = cv.rectangle(image_copy, (i_max, j_max), (i_max + I, j_max + J), (255, 134, 0), 2)
    plt.imshow(np.array(image_copy))
    plt.show()

    return correlation_func


def my_search(image: np.ndarray, template: np.ndarray, method='norm'):
    """Метод, реализующий поиск на изображении эталона вручную"""

    templ_h, templ_w = np.shape(template)
    img_h, img_w = np.shape(image)

    templ_mean = np.mean(template)
    templ_std = np.std(template)

    corr_func = np.zeros((img_h - templ_h + 1, img_w - templ_w + 1))

    for i in range(img_h - templ_h + 1):
        for j in range(img_w - templ_w + 1):
            # слайсы от i до i + templ_h и второго соотв.
            box = image[i:i + templ_h, j:j + templ_w]
            box_mean = np.mean(box)

            match method.upper():
                case 'NORM':
                    # нормированная корреляционная функция
                    corr_func[i, j] = ((1 / (templ_h * templ_w)) * np.sum((template - templ_mean) * (box - box_mean))
                                       / (np.std(box) * templ_std))

                case 'SQR':
                    # квадрат разности
                    corr_func[i, j] = (1 / (templ_h * templ_w)) * np.sum((template - box) ** 2)

                case 'ABS':
                    # средний модуль разности (MAD)
                    corr_func[i, j] = (1 / (templ_h * templ_w)) * np.sum(abs(template - box))

                case _:
                    raise ValueError('Такой корреляционной функции в скрипте нет')

    # копия кода с методы
    match method.upper():
        case 'NORM':
            max_index = corr_func.argmax()  # копия фрагмента с методы
            i_corner = int(max_index % corr_func.shape[1])
            j_corner = int(max_index / corr_func.shape[1])

        case 'SQR':
            min_index = corr_func.argmin()
            i_corner = int(min_index % corr_func.shape[1])
            j_corner = int(min_index / corr_func.shape[1])

        case 'ABS':
            min_index = corr_func.argmin()
            i_corner = int(min_index % corr_func.shape[1])
            j_corner = int(min_index / corr_func.shape[1])

        case _:
            raise ValueError('Такой корреляционной функции в скрипте нет')

    image_copy = image
    image_copy = cv.cvtColor(image_copy, cv.COLOR_GRAY2BGR)
    I, J = np.shape(template)
    image_copy = cv.rectangle(image_copy, (i_corner, j_corner), (i_corner + I, j_corner + J), (255, 134, 0), 2)
    plt.imshow(np.array(image_copy))
    plt.show()

    return corr_func


def main():
    """Основная исполняющая функция"""
    filename = 'orig.png'
    image = cv.imread(filename)
    gray_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    noise_image = random_noise(gray_image, mode='gaussian', rng=42, clip=True, mean=0, var=0.01)
    noise_image = np.array(255 * noise_image, dtype='uint8')

    template_name = 'template.png'
    template = cv.cvtColor(cv.imread(template_name), cv.COLOR_RGB2GRAY)

    # поменять и сравнить потом
    # res = methodical_search(noise_image, template)
    res = my_search(noise_image, template, method='abs') 
    # res = my_search(gray_image, template, method='abs')

    fig, ax = plt.subplots(1, 1, figsize=(16, 9))
    surf = fig.add_subplot(projection='3d')
    xs, ys = np.meshgrid(range(len(res[0])), range(len(res)))
    surf.plot_surface(xs, ys, res)
    plt.show()


if __name__ == "__main__":
    main()
