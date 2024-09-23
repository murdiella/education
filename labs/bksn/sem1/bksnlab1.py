from matplotlib import pyplot as plt
import cv2 as cv


def load_image(filename=None):
    """Функция для загрузки изображения, требуемая по заданию"""
    if filename is not None and isinstance(filename, str):
        return cv.imread(filename)
    else:
        if filename is None:
            raise ValueError('forgor to input a name :dead:')
        else:
            raise TypeError('shoulda been a string fool')


def image_typization(img=None, img_type=None):
    """Функция для перевода изображения в другой тип"""
    if img is not None and img_type is not None:
        img_type = img_type.upper()
        # на вводе img_type достаточно ввести тип нижним регистром
        match img_type:
            case 'GRAY':
                return cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            case 'BGR':
                return cv.cvtColor(img, cv.COLOR_RGB2BGR)
            case 'YCRCB':
                return cv.cvtColor(img, cv.COLOR_RGB2YCrCb)
            case 'HSV':
                return cv.cvtColor(img, cv.COLOR_RGB2HSV)
            case _:
                raise ValueError('wrong type input fool')
    else:
        raise ValueError('forgor to input an image or type fool')


def image_split(img=None):
    """Функция для вывода каналов и т.д. изображения из примера к ЛР"""
    if img is not None:
        img_gray = image_typization(img, 'gray')
        img_bgr = image_typization(img, 'bgr')

        r, g, b = cv.split(img)

        fig, ax = plt.subplots(3, 3, figsize=(16, 11))
        rc = ax[0, 0].imshow(r, cmap='Reds', vmin=0, vmax=255)
        gc = ax[0, 1].imshow(g, cmap='Greens', vmin=0, vmax=255)
        bc = ax[0, 2].imshow(b, cmap='Blues', vmin=0, vmax=255)
        bwc = ax[1, 0].imshow(img_gray, cmap='gray', vmin=0, vmax=255)
        ax[1, 1].imshow(cv.merge((b, g, r)))
        ax[1, 2].hist(img_gray.ravel(), bins=range(256), fc='k', ec='k')
        ax[2, 0].imshow(cv.merge((255 - b, 255 - g, 255 - r)))
        ax[2, 1].imshow(255 - img_bgr)
        tmp = ax[2, 2].imshow(r * g * b, cmap='gray', vmin=0, vmax=255)

        fig.colorbar(rc, ax=ax[0, 0])
        fig.colorbar(gc, ax=ax[0, 1])
        fig.colorbar(bc, ax=ax[0, 2])
        fig.colorbar(bwc, ax=ax[1, 0])
        fig.colorbar(tmp, ax=ax[2, 2])

        ax[0, 0].set_title('Красный канал')
        ax[0, 1].set_title('Зеленый канал')
        ax[0, 2].set_title('Синий канал')
        ax[1, 0].set_title('Черно-белое (интенсивность)')
        ax[1, 1].set_title('Наложение каналов')
        ax[1, 2].set_title('Распределение интенсивности')
        ax[2, 0].set_title('Каналы инвертированы по отдельности')
        ax[2, 1].set_title('Каналы инвертированы одновременно')

        plt.show()
    else:
        raise ValueError('forgor to input an image fool')


def get_image_info(img, img_bw=None):
    """Функция для получения информации об изображении, приведенная в задании"""
    if img is not None:
        if img_bw is None:
            img_bw = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        print('Размер изображения:\n\tШирина              {} px\n\tВысота              {} px\n\tКоличество каналов  {}'.format(img.shape[0], img.shape[1],img.shape[2]))
        print("Тип данных:\n\t{}".format(img.dtype))
        print('Основные стат. характеристики:\n\tМат. ожидание: {}\n\tДисперсия:     {}\n\tСКО:           {}'.format(img_bw.mean(), img_bw.var(), img_bw.std()))
    else:
        raise ValueError('forgor to input an image fool')


def image_split2(img=None):
    """Функция для вывода каналов RGB, YCrCb и HSV изображений, требуемая по заданию"""
    if img is not None:
        img_hsv = image_typization(img, 'hsv')
        img_ycrcb = image_typization(img, 'ycrcb')

        # дубликат фрагмента кода, приведенного в задании
        r, g, b = cv.split(img)

        fig, ax = plt.subplots(3, 4, figsize=(16, 11))
        ax[0, 0].set_title('Оригинал RGB')
        rgb = ax[0, 0].imshow(image_typization(img, 'bgr'))
        ax[0, 1].set_title('Красный канал')
        rc = ax[0, 1].imshow(r, cmap="Reds", vmin=0, vmax=255)
        ax[0, 2].set_title('Зеленый канал')
        gc = ax[0, 2].imshow(g, cmap="Greens", vmin=0, vmax=255)
        ax[0, 3].set_title('Синий канал')
        bc = ax[0, 3].imshow(b, cmap="Blues", vmin=0, vmax=255)

        ax[1, 0].set_title('Оригинал YCrCb')
        ycrcb = ax[1, 0].imshow(cv.cvtColor(img_ycrcb, cv.COLOR_YCrCb2BGR))
        # заполнение недостающих каналов изображения
        ax[1, 1].set_title('Y канал')
        only_Y = img_ycrcb.copy()
        only_Y[:, :, 1] = 128  # по сути, нейтрализуем все остальные каналы средним значением
        only_Y[:, :, 2] = 128
        y = ax[1, 1].imshow(cv.cvtColor(only_Y, cv.COLOR_YCrCb2BGR))
        ax[1, 2].set_title('Cr канал')
        only_Cr = img_ycrcb.copy()
        only_Cr[:, :, 0] = 128
        only_Cr[:, :, 2] = 128
        cr = ax[1, 2].imshow(cv.cvtColor(only_Cr, cv.COLOR_YCrCb2BGR))
        ax[1, 3].set_title('Cb канал')
        only_Cb = img_ycrcb.copy()
        only_Cb[:, :, 0] = 128
        only_Cb[:, :, 1] = 128
        cb = ax[1, 3].imshow(cv.cvtColor(only_Cb, cv.COLOR_YCrCb2BGR))

        ax[2, 0].set_title('Оригинал HSV')
        hsv = ax[2, 0].imshow(cv.cvtColor(img_hsv, cv.COLOR_HSV2BGR))
        # аналогичные действия как с изображением в YCrCb
        ax[2, 1].set_title('H канал')
        only_H = img_hsv.copy()
        only_H[:, :, 1] = 128
        only_H[:, :, 2] = 128
        h = ax[2, 1].imshow(cv.cvtColor(only_H, cv.COLOR_HSV2BGR))
        ax[2, 2].set_title('S канал')
        only_S = img_hsv.copy()
        only_S[:, :, 0] = 128
        only_S[:, :, 2] = 128
        s = ax[2, 2].imshow(cv.cvtColor(only_S, cv.COLOR_HSV2BGR))
        ax[2, 3].set_title('V канал')
        only_V = img_hsv.copy()
        only_V[:, :, 0] = 128
        only_V[:, :, 1] = 128
        v = ax[2, 3].imshow(cv.cvtColor(only_V, cv.COLOR_HSV2BGR))

        plt.show()

    else:
        raise ValueError('forgor to input an image fool')


def main():
    """Основная исполнительная функция для ЛР1"""
    img = load_image('orig.png')

    get_image_info(img)
    image_split2(img)


# предотвращение ненужных запусков при импортировании модуля
if __name__ == "__main__":
    main()
