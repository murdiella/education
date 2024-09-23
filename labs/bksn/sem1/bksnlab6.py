import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from scipy import ndimage


def contour(image: np.ndarray):
    """Метод реализации выделения контуров изображения"""

    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    roberts_cross_v = np.array([[1, 0], [0, -1]])
    roberts_cross_h = np.array([[0, 1], [-1, 0]])
    vertical = ndimage.convolve(image_gray, roberts_cross_v)
    horizontal = ndimage.convolve(image_gray, roberts_cross_h)
    edged_img = np.sqrt(np.square(horizontal) + np.square(vertical))
    kernel = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])
    ddepth = cv.CV_16S
    image_filter2d = cv.filter2D(image_gray, -1, kernel)

    sobel_h = cv.Sobel(image_gray, ddepth, 1, 0, ksize=3, borderType=cv.BORDER_DEFAULT)
    sobel_v = cv.Sobel(image_gray, ddepth, 0, 1, ksize=3, borderType=cv.BORDER_DEFAULT)

    abs_grad_x = cv.convertScaleAbs(sobel_h)
    abs_grad_y = cv.convertScaleAbs(sobel_v)

    sobel_image = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    laplas_image = cv.Laplacian(image_gray, ddepth, ksize=3)

    image_gray_gaussian_blur = cv.GaussianBlur(image_gray, (3, 3), 0)

    laplas2_image = cv.Laplacian(image_gray_gaussian_blur, ddepth, ksize=3)

    canny_image = cv.Canny(image_gray, 100, 200, 3)

    fig, ax = plt.subplots(2, 3, figsize=(16, 9))
    ax[0][0].imshow(image_gray, cmap='gray', vmin=0, vmax=255)
    ax[0][0].set_title("Исходное изображение")
    ax[1][0].imshow(image_filter2d, cmap='gray', vmin=0, vmax=255)
    ax[1][0].set_title(" 2D filter", y=-0.25)
    ax[0][1].imshow(sobel_image, cmap='gray', vmin=0, vmax=255)
    ax[0][1].set_title("Собель")
    ax[1][1].imshow(laplas_image, cmap='gray', vmin=0, vmax=255)
    ax[1][1].set_title("Гауссиан", y=-0.25)
    ax[0][2].imshow(laplas2_image, cmap='gray', vmin=0, vmax=255)
    ax[0][2].set_title("Пересечение 0")
    ax[1][2].imshow(canny_image, cmap='gray', vmin=0, vmax=255)
    ax[1][2].set_title("Метод Канни", y=-0.25)

    plt.show()


def high_pass_filter(image: np.ndarray):
    """Метод для реализации фильтров высоких частот"""

    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    kernel_9 = np.array([[-1, -1, -1],
                        [-1, 9, -1],
                        [-1, -1, -1]])

    filter_9 = cv.filter2D(image_gray, -1, kernel_9)

    kernel_51 = np.array([[0, -1, -0],
                        [-1, 5, -1],
                        [0, -1, 0]])

    filter_51 = cv.filter2D(image_gray, -1, kernel_51)

    kernel_52 = np.array([[1, -2, 1],
                        [-2, 5, -2],
                        [1, -2, 1]])

    filter_52 = cv.filter2D(image_gray, -1, kernel_52)

    kernel_5x5 = np.array([[-1, -2, -3, -2, -1],
                        [-2, 0, 2, 0, -2],
                        [-3, 2, 24, 2, -3],
                        [-2, 0, 2, 0, -2],
                        [-1, -2, -3, -2, -1]])

    filter_5x5 = cv.filter2D(image_gray, -1, kernel_5x5)

    fig, ax = plt.subplots(2, 2, figsize=(16, 9))
    ax[0][0].imshow(filter_9, cmap='gray', vmin=0, vmax=255)
    ax[0][0].set_title("Фильтр 3x3 с девяткой")
    ax[1][0].imshow(filter_51, cmap='gray', vmin=0, vmax=255)
    ax[1][0].set_title("Фильтр 3x3 с пятеркой и единицами", y=-0.25)
    ax[0][1].imshow(filter_52, cmap='gray', vmin=0, vmax=255)
    ax[0][1].set_title("Фильтр 3x3 с пятеркой и двойками")
    ax[1][1].imshow(filter_5x5, cmap='gray', vmin=0, vmax=255)
    ax[1][1].set_title("Фильтр 5x5", y=-0.25)
    plt.show()


def main():
    """Основная исполняющая функция"""
    filename = "orig.png"
    image = cv.imread(filename)

    # contour(image)
    high_pass_filter(image)


if __name__ == "__main__":
    main()
