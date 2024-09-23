import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import random as r
import scipy


def mask(image: np.ndarray):
    """Масочное фильтрование, представленное в методичке"""
    src = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    ddepth = -1
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    mask_image = cv.filter2D(src, ddepth, kernel)
    plt.figure(figsize=(14, 12))
    plt.subplot(121), plt.imshow(src), plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(mask_image), plt.title('Outline')
    plt.xticks([]), plt.yticks([])
    plt.show()


def freq_response(image: np.ndarray):
    """Функция построения ЛАЧХ фильтра из методички"""
    image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    N = 4
    Wn = 0.01
    b, a = scipy.signal.butter(N, Wn, btype='low', analog=True, output='ba')
    w, h = scipy.signal.freqs(b, a)  # нахождение АЧХ фильтра
    plt.semilogx(w, 20 * np.log10(abs(h)))  # логарифмирование АЧХ
    plt.title('Butterworth filter frequency response')
    plt.xlabel('Frequency [radians / second]')
    plt.ylabel('Amplitude [dB]')
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.show()  # вывод графика

    image_gray_filtered = scipy.signal.lfilter(b,a,image_gray)

    fig, ax = plt.subplots(1, 2, figsize=(16, 9))
    ax[0].imshow(image_gray, cmap="gray")
    ax[0].set_title('Исходное полутоновое')
    ax[1].imshow(image_gray_filtered,cmap="gray")
    ax[1].set_title('АЧХ фильтрация')
    plt.show()


def median_filter(image: np.ndarray):
    """Функция медианной фильтрации из методички"""
    image = salt_pepper(image)
    r, g, b = cv.split(image)
    src = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    med_r = scipy.signal.medfilt(r, kernel_size=5)
    med_g = scipy.signal.medfilt(g, kernel_size=5)
    med_b = scipy.signal.medfilt(b, kernel_size=5)
    med_image = cv.merge((med_b, med_g, med_r))
    plt.figure(figsize=(14, 12))
    plt.subplot(121), plt.imshow(src), plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(med_image), plt.title('Median')
    plt.xticks([]), plt.yticks([])
    plt.show()


def rank_filter(image: np.ndarray):
    """Ранговая фильтрация из методички"""
    r, g, b = cv.split(image)
    src = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    domain = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    focus_r = scipy.signal.order_filter(r, domain, 0)
    focus_g = scipy.signal.order_filter(g, domain, 0)
    focus_b = scipy.signal.order_filter(b, domain, 0)
    unfocus_r = scipy.signal.order_filter(r, domain, 8)
    unfocus_g = scipy.signal.order_filter(g, domain, 8)
    unfocus_b = scipy.signal.order_filter(b, domain, 8)
    focus_image = cv.merge((focus_b, focus_g, focus_r))
    unfocus_image = cv.merge((unfocus_b, unfocus_g, unfocus_r))
    plt.figure(figsize=(22, 12))
    plt.subplot(131), plt.imshow(src), plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(focus_image), plt.title('Focus')
    plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(unfocus_image), plt.title('Unfocus')
    plt.xticks([]), plt.yticks([])
    plt.show()


def wiener_filter(image: np.ndarray):
    """Фильтрация методом Винера из методички"""
    image = cv.cvtColor(image, cv.COLOR_GRAY2RGB)
    r, g, b = cv.split(image)
    src = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    auto_r = scipy.signal.wiener(r)
    auto_g = scipy.signal.wiener(g)
    auto_b = scipy.signal.wiener(b)
    wiener_r = scipy.signal.wiener(r, mysize=5, noise=1)
    wiener_g = scipy.signal.wiener(g, mysize=5, noise=1)
    wiener_b = scipy.signal.wiener(b, mysize=5, noise=1)
    auto_image = cv.merge((auto_b, auto_g, auto_r))
    wiener_image = cv.merge((wiener_b, wiener_g, wiener_r))
    height, width, channels = image.shape
    normalizedAuto = np.zeros((height, width))
    normalizedWiener = np.zeros((height, width))
    normalizedAuto = cv.normalize(auto_image, normalizedAuto, 0, 1, cv.NORM_MINMAX)
    normalizedWiener = cv.normalize(wiener_image, normalizedWiener, 0, 1, cv.NORM_MINMAX)
    plt.figure(figsize=(22, 12))
    plt.subplot(131), plt.imshow(src), plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(normalizedAuto), plt.title('Auto Wiener')
    plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(normalizedWiener), plt.title('Wiener')
    plt.xticks([]), plt.yticks([])
    plt.show()


def my_mask_filter(image: np.ndarray):
    """Вручную реализованная функция масочной фильтрации"""
    image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    mask_image = np.empty_like(image)
    a, b = np.shape(image_gray)
    for i in range(a - 2):
        for j in range(b - 2):
            mask_image[i + 1][j + 1] = (image_gray[i][j] * kernel[0][0]
                                        + image_gray[i + 1][j] * kernel[1][0]
                                        + image_gray[i + 2][j] * kernel[2][0]
                                        + image_gray[i][j + 1] * kernel[0][1]
                                        + image_gray[i + 1][j + 1] * kernel[1][1]
                                        + image_gray[i + 2][j + 1] * kernel[2][1]
                                        + image_gray[i][j + 2] * kernel[0][2]
                                        + image_gray[i + 1][j + 2] * kernel[1][2]
                                        + image_gray[i + 2][j + 2] * kernel[2][2])
    fig, ax = plt.subplots(1, 2, figsize=(16, 9))
    ax[0].imshow(image_gray, cmap="gray")
    ax[0].set_title('Original')
    ax[1].imshow(mask_image)
    ax[1].set_title('Outline')
    plt.show()


def salt_pepper(image: np.ndarray, prob: float = 0.15):
    """Метод для добавления на изображение шума типа соль-перец"""
    if abs(prob) >= 1:
        raise Exception('Вероятность не может быть большей чем 1')
    new_image = image.copy()
    try:
        a, b, _ = np.shape(image)
    except ValueError:
        a, b = np.shape(image)
    for i in range(a):
        for j in range(b):
            if r.uniform(0, 1) < prob:
                if r.uniform(0, 1) < 0.5:
                    new_image[i][j] = 0
                else:
                    new_image[i][j] = 255

    return new_image


def gaussian(image: np.ndarray, mean=0, std=100):
    """Метод добавления на изображение гауссовского шума"""
    image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    noise = np.zeros(image_gray.shape, np.uint8)
    cv.randn(noise, mean, std)

    return cv.add(image_gray, noise)


def main():
    """Основная исполняющая функция"""
    image = cv.imread('orig.png')
    image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    peppered_image = salt_pepper(image_gray)
    gaussed_image = gaussian(image)

    # my_mask_filter(image)
    # mask(image)
    # freq_response(image)
    # median_filter(image)
    # rank_filter(image)
    wiener_filter(gaussed_image)


if __name__ == "__main__":
    main()
