import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import warnings


def quant(image: np.ndarray, n: int):
    """Метод для квантования изображения"""

    lvl_list = 256 / n
    new = np.empty_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            new[i][j] = image[i][j] - (image[i][j] % lvl_list)

    return new


def gamma_corr(image: np.ndarray, gamma: float = 1):
    """Метод для выполнения гамма-коррекции"""

    new = np.empty_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            new[i][j] = (image[i][j] / 255) ** gamma * 255

    return new


def get_hists(image: np.ndarray):
    """Метод для получения гистограммы изображения"""

    hist_array = image.ravel()
    equalized = cv.equalizeHist(image)
    eq_hist_array = equalized.ravel()
    clahe = cv.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    clahed = clahe.apply(image)
    cl_hist_array = clahed.ravel()

    fig, ax = plt.subplots(2, 3, figsize=(16, 9))
    ax[1][0].hist(hist_array, color='blue', edgecolor='black')
    ax[1][1].hist(eq_hist_array, color='blue', edgecolor='black')
    ax[1][2].hist(cl_hist_array, color='blue', edgecolor='black')

    ax[0][0].imshow(cv.cvtColor(image, cv.COLOR_GRAY2BGRA))
    ax[0][1].imshow(cv.cvtColor(equalized, cv.COLOR_GRAY2BGRA))
    ax[0][2].imshow(cv.cvtColor(clahed, cv.COLOR_GRAY2BGRA))

    ax[0][0].set_title('Начальная')
    ax[0][1].set_title('Выровненная')
    ax[0][2].set_title('Выровненная с ограничениями')
    plt.show()


def affinis(image: np.ndarray, k: float = 1, w: float = 0, c: float = 0, f: float = 0):
    """Метод для выполнения аффинных преобразований"""

    def u(x, y) -> int:
        return int(np.round(k * x * np.cos(w) + k * y * np.sin(w) + c))

    def v(x, y) -> int:
        return int(np.round(-k * x * np.sin(w) + k * y * np.cos(w) + f))

    w = w * np.pi / 180  # нампай принимает в радианах углы емае
    xlen, ylen = np.shape(image)
    new_image = np.full(np.shape(image), 127)
    for i in range(xlen):
        for j in range(ylen):
            try:
                u_temp = u(i, j)
                v_temp = v(i, j)
                if u_temp > image.shape[0] or u_temp < 0 or v_temp > image.shape[1] or v_temp < 0:
                    continue
                new_image[u_temp, v_temp] = image[i, j]
            except IndexError:
                pass

    return abs(new_image - 255)


def main():
    """Основная исполняющая функция"""
    warnings.simplefilter(action='ignore', category=UserWarning)  # потому что задрали

    filename = "orig.png"
    image = cv.imread(filename)
    image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    # аффинные преобразования
    # new = affinis(image_gray, w=30, k=0.8, c=100, f=100)
    # fig, ax = plt.subplots(1, 2, figsize=(16, 9))
    # base = ax[0].imshow(cv.cvtColor(image_gray, cv.COLOR_GRAY2BGRA))
    # affected = ax[1].imshow(cv.cvtColor(new.astype('uint8') * 255, cv.COLOR_GRAY2BGRA))
    # plt.show()

    # манипуляции с гистограммой
    # get_hists(image_gray)

    # гамма коррекция
    # gamma_image = gamma_corr(image_gray, 0.2)
    # fig, ax = plt.subplots(1, 2, figsize=(16, 9))
    # noncorr = ax[0].imshow(cv.cvtColor(image_gray, cv.COLOR_GRAY2BGRA))
    # corr = ax[1].imshow(cv.cvtColor(gamma_image, cv.COLOR_GRAY2BGRA))
    # plt.show()

    # квантование
    quant_image256 = quant(image_gray, 256)
    quant_image128 = quant(image_gray, 128)
    quant_image64 = quant(image_gray, 64)
    quant_image8 = quant(image_gray, 8)
    fig, ax = plt.subplots(1, 5, figsize=(16, 9))
    nonquanted = ax[0].imshow(cv.cvtColor(image_gray, cv.COLOR_GRAY2BGRA))
    quanted256 = ax[1].imshow(cv.cvtColor(quant_image256, cv.COLOR_GRAY2BGRA))
    quanted128 = ax[2].imshow(cv.cvtColor(quant_image128, cv.COLOR_GRAY2BGRA))
    quanted64 = ax[3].imshow(cv.cvtColor(quant_image64, cv.COLOR_GRAY2BGRA))
    quanted8 = ax[4].imshow(cv.cvtColor(quant_image8, cv.COLOR_GRAY2BGRA))
    ax[0].set_title('Оригинал')
    ax[1].set_title('256 уровней')
    ax[2].set_title('128 уровней')
    ax[3].set_title('64 уровня')
    ax[4].set_title('8 уровней')
    plt.show()


if __name__ == '__main__':
    main()
