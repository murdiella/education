import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from INS_and_SNS import INS, SNS
from data import values
import socket as sc
from ctypes import *
from time import sleep
import matplotlib as plt

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('SNS/INS Control')

        # Создаем кнопки
        self.btn_ins = QPushButton('INS', self)
        self.btn_ins.clicked.connect(self.start_ins)

        self.btn_sns = QPushButton('SNS', self)
        self.btn_sns.clicked.connect(self.start_sns)

        # Создаем интерфейс
        vbox = QVBoxLayout()
        vbox.addWidget(self.btn_ins)
        vbox.addWidget(self.btn_sns)

        self.setLayout(vbox)

    def start_ins(self):
        ins = INS()
        ins.preparation()
        self.start_navigation(ins)

    def start_sns(self):
        sns = SNS()
        sns.control()
        self.start_navigation(sns)

    def start_navigation(self, device):
        addr = ('127.0.0.1', 12346)
        sck = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
        sck.connect(('localhost', 12346))

        for i in range(50):
            device.navigation(values)
            test = self.packing(device)
            sck.sendto(test, addr)
            sleep(0.5)

        sck.close()

    def packing(self, ctype_instance):
        buff = string_at(byref(ctype_instance), sizeof(ctype_instance))
        return buff


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())



