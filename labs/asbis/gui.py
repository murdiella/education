"""Модуль, содержащий в себе реализацию GUI"""
from PyQt5 import QtCore, QtWidgets, QtTest, QtGui
import matplotlib.pyplot as plt
import sys
from numpy import arange


class UI_Window(object):
    """Класс окна-реализации GUI"""

    def setup_ui(self, main_window):
        """Метод для 'разметки' графического интерфейса"""

        main_window.setObjectName("main_window")
        main_window.resize(480, 640)

        main_window.setObjectName("GUI ASBIS")  # имя приложения в шапке

        # само окно, по сути
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # вывод текстовой информации
        self.message_viewer = QtWidgets.QTextBrowser(self.centralwidget)
        self.message_viewer.setGeometry(QtCore.QRect(10, 10, 460, 570))
        self.message_viewer.setObjectName("message_viewer")
        main_window.setCentralWidget(self.centralwidget)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        """Метод для выстраивания обращения к элементам интерфейса в коде"""
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "MainWindow"))

    def output_data(self, data: str):
        """Метод для вывода текстовых данных в приложение"""
        self.message_viewer.insertPlainText(f'{data}\n\n')


    # def close_event(self, *args, **kwargs):
    #     super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)


def graph(ins, sns, complex_, title: str = ''):
    """Фукнция для построения и вывода графика координат"""
    # if not (len(ins) == len(sns) == len(complex_)):
    #     raise ValueError('Массивы должны иметь')

    x = arange(1, len(ins) + 1, 1)
    plt.plot(x, ins, label='ins')
    plt.plot(x, sns, label='sns')
    plt.plot(x, complex_, '-.', label='complex')

    plt.xlabel("Номер принятого по счету пакета")
    plt.ylabel('Значения величины ИНС, СНС и комплексного')
    plt.legend()
    plt.title(title)
    plt.show()


def main():
    ins = [0, 1, 2, 3]
    sns = [3, 4, 5, 7]
    comp = [2, 2, 4, 5]

    graph(ins, sns, comp, title='test')

    # # объявляем приложение
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = UI_Window()

    ui.setup_ui(window)  # сетапим расположение элементов интерфейса
    ui.output_data("data")
    ui.output_data("lol")

    window.show()  # отображение окна
    sys.exit(app.exec_())  # закрытие на крестик


if __name__ == "__main__":
    main()
