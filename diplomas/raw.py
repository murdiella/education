# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diplomas.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pareto_button = QtWidgets.QPushButton(self.centralwidget)
        self.pareto_button.setGeometry(QtCore.QRect(380, 330, 191, 61))
        self.pareto_button.setObjectName("pareto_button")
        self.label_t = QtWidgets.QLabel(self.centralwidget)
        self.label_t.setGeometry(QtCore.QRect(60, 80, 47, 13))
        self.label_t.setObjectName("label_t")
        self.label_n_input = QtWidgets.QLabel(self.centralwidget)
        self.label_n_input.setGeometry(QtCore.QRect(60, 110, 47, 13))
        self.label_n_input.setObjectName("label_n_input")
        self.label_m_input = QtWidgets.QLabel(self.centralwidget)
        self.label_m_input.setGeometry(QtCore.QRect(150, 110, 47, 13))
        self.label_m_input.setObjectName("label_m_input")
        self.label_t1_min = QtWidgets.QLabel(self.centralwidget)
        self.label_t1_min.setGeometry(QtCore.QRect(60, 140, 47, 13))
        self.label_t1_min.setObjectName("label_t1_min")
        self.label_t2min_input = QtWidgets.QLabel(self.centralwidget)
        self.label_t2min_input.setGeometry(QtCore.QRect(60, 170, 47, 13))
        self.label_t2min_input.setObjectName("label_t2min_input")
        self.label_t3min_input = QtWidgets.QLabel(self.centralwidget)
        self.label_t3min_input.setGeometry(QtCore.QRect(60, 200, 47, 13))
        self.label_t3min_input.setObjectName("label_t3min_input")
        self.label_p_input = QtWidgets.QLabel(self.centralwidget)
        self.label_p_input.setGeometry(QtCore.QRect(60, 230, 47, 13))
        self.label_p_input.setObjectName("label_p_input")
        self.label_title_scalar = QtWidgets.QLabel(self.centralwidget)
        self.label_title_scalar.setGeometry(QtCore.QRect(400, 50, 161, 16))
        self.label_title_scalar.setObjectName("label_title_scalar")
        self.label_a1_input = QtWidgets.QLabel(self.centralwidget)
        self.label_a1_input.setGeometry(QtCore.QRect(60, 260, 47, 13))
        self.label_a1_input.setObjectName("label_a1_input")
        self.label_a2_input = QtWidgets.QLabel(self.centralwidget)
        self.label_a2_input.setGeometry(QtCore.QRect(150, 260, 47, 13))
        self.label_a2_input.setObjectName("label_a2_input")
        self.label_title_target = QtWidgets.QLabel(self.centralwidget)
        self.label_title_target.setGeometry(QtCore.QRect(410, 190, 211, 16))
        self.label_title_target.setObjectName("label_title_target")
        self.input_t = QtWidgets.QLineEdit(self.centralwidget)
        self.input_t.setGeometry(QtCore.QRect(100, 80, 141, 20))
        self.input_t.setObjectName("input_t")
        self.input_a1 = QtWidgets.QLineEdit(self.centralwidget)
        self.input_a1.setGeometry(QtCore.QRect(100, 260, 41, 20))
        self.input_a1.setObjectName("input_a1")
        self.input_a2 = QtWidgets.QLineEdit(self.centralwidget)
        self.input_a2.setGeometry(QtCore.QRect(200, 260, 41, 20))
        self.input_a2.setObjectName("input_a2")
        self.input_n = QtWidgets.QLineEdit(self.centralwidget)
        self.input_n.setGeometry(QtCore.QRect(100, 110, 41, 20))
        self.input_n.setObjectName("input_n")
        self.input_m = QtWidgets.QLineEdit(self.centralwidget)
        self.input_m.setGeometry(QtCore.QRect(200, 110, 41, 20))
        self.input_m.setObjectName("input_m")
        self.input_p = QtWidgets.QLineEdit(self.centralwidget)
        self.input_p.setGeometry(QtCore.QRect(100, 230, 41, 20))
        self.input_p.setObjectName("input_p")
        self.input_t3min = QtWidgets.QLineEdit(self.centralwidget)
        self.input_t3min.setGeometry(QtCore.QRect(100, 200, 41, 20))
        self.input_t3min.setObjectName("input_t3min")
        self.input_t3max = QtWidgets.QLineEdit(self.centralwidget)
        self.input_t3max.setGeometry(QtCore.QRect(200, 200, 41, 20))
        self.input_t3max.setObjectName("input_t3max")
        self.input_t1min = QtWidgets.QLineEdit(self.centralwidget)
        self.input_t1min.setGeometry(QtCore.QRect(100, 140, 41, 20))
        self.input_t1min.setObjectName("input_t1min")
        self.input_t2min = QtWidgets.QLineEdit(self.centralwidget)
        self.input_t2min.setGeometry(QtCore.QRect(100, 170, 41, 20))
        self.input_t2min.setObjectName("input_t2min")
        self.input_t1max = QtWidgets.QLineEdit(self.centralwidget)
        self.input_t1max.setGeometry(QtCore.QRect(200, 140, 41, 20))
        self.input_t1max.setObjectName("input_t1max")
        self.input_t2max = QtWidgets.QLineEdit(self.centralwidget)
        self.input_t2max.setGeometry(QtCore.QRect(200, 170, 41, 20))
        self.input_t2max.setObjectName("input_t2max")
        self.label_title_input = QtWidgets.QLabel(self.centralwidget)
        self.label_title_input.setGeometry(QtCore.QRect(90, 50, 131, 16))
        self.label_title_input.setObjectName("label_title_input")
        self.label_t1_min_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_t1_min_2.setGeometry(QtCore.QRect(150, 140, 47, 13))
        self.label_t1_min_2.setObjectName("label_t1_min_2")
        self.label_t2max_input = QtWidgets.QLabel(self.centralwidget)
        self.label_t2max_input.setGeometry(QtCore.QRect(150, 170, 47, 13))
        self.label_t2max_input.setObjectName("label_t2max_input")
        self.label_t3max_input = QtWidgets.QLabel(self.centralwidget)
        self.label_t3max_input.setGeometry(QtCore.QRect(150, 200, 47, 13))
        self.label_t3max_input.setObjectName("label_t3max_input")
        self.calc_button = QtWidgets.QPushButton(self.centralwidget)
        self.calc_button.setGeometry(QtCore.QRect(60, 330, 181, 61))
        self.calc_button.setObjectName("calc_button")
        self.output_scalar = QtWidgets.QTextBrowser(self.centralwidget)
        self.output_scalar.setGeometry(QtCore.QRect(380, 80, 191, 101))
        self.output_scalar.setObjectName("output_scalar")
        self.output_target = QtWidgets.QTextBrowser(self.centralwidget)
        self.output_target.setGeometry(QtCore.QRect(380, 210, 191, 101))
        self.output_target.setObjectName("output_target")
        self.label_intervals_input = QtWidgets.QLabel(self.centralwidget)
        self.label_intervals_input.setGeometry(QtCore.QRect(60, 290, 141, 16))
        self.label_intervals_input.setObjectName("label_intervals_input")
        self.input_interval_count = QtWidgets.QSpinBox(self.centralwidget)
        self.input_interval_count.setGeometry(QtCore.QRect(200, 290, 42, 22))
        self.input_interval_count.setMinimum(1)
        self.input_interval_count.setMaximum(999)
        self.input_interval_count.setProperty("value", 10)
        self.input_interval_count.setObjectName("input_interval_count")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GUI"))
        self.pareto_button.setText(_translate("MainWindow", "Построить множество Парето"))
        self.label_t.setText(_translate("MainWindow", "t = "))
        self.label_n_input.setText(_translate("MainWindow", "n ="))
        self.label_m_input.setText(_translate("MainWindow", "m ="))
        self.label_t1_min.setText(_translate("MainWindow", "t1min ="))
        self.label_t2min_input.setText(_translate("MainWindow", "t2min ="))
        self.label_t3min_input.setText(_translate("MainWindow", "t3min ="))
        self.label_p_input.setText(_translate("MainWindow", "p ="))
        self.label_title_scalar.setText(_translate("MainWindow", "Скалярная свертка критерия:"))
        self.label_a1_input.setText(_translate("MainWindow", "a1 ="))
        self.label_a2_input.setText(_translate("MainWindow", "a2 ="))
        self.label_title_target.setText(_translate("MainWindow", "Метод прицельной точки:"))
        self.label_title_input.setText(_translate("MainWindow", "Блок ввода параметров"))
        self.label_t1_min_2.setText(_translate("MainWindow", "t1max ="))
        self.label_t2max_input.setText(_translate("MainWindow", "t2max ="))
        self.label_t3max_input.setText(_translate("MainWindow", "t3max ="))
        self.calc_button.setText(_translate("MainWindow", "Рассчитать критерии"))
        self.label_intervals_input.setText(_translate("MainWindow", "Количество интервалов ="))