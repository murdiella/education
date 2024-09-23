import psycopg2 as pscg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QTableWidgetItem
import sys


# класс для получения информации о таблицах и их содержимом
# без условий к содержимому
class Informer:

    # создаем соединение
    def __init__(self):
        creds = open("credentials.txt", 'r')
        self.conn = pscg.connect(f"{creds.read()}")
        self.cur = self.conn.cursor()

    # убираем соединение
    def __del__(self):
        self.conn.commit()
        self.cur.close()

    # функция возвращает все таблицы в БД
    def tables(self):
        # ставим указатель на столбец table_name из таблицы inf_schema.tables из схемы public
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        unedited_list = self.cur.fetchall()

        # разбиваем на тюпл названий таблиц и возвращаем
        tables = []
        for item in unedited_list:
            tables.append(item[0])

        return tuple(tables)

    # функция возвращает все имена столбцов из таблицы в БД
    def columns(self, table_name):
        # указатель на всю таблицу
        self.cur.execute(f"SELECT * FROM {table_name}")
        # имена столбцов (нулевые элементы) в таблице description
        column_names = [name[0] for name in self.cur.description]
        return tuple(column_names)


# класс для создания и выполнения запросов
class Fetcher:

    # создаем соединение
    def __init__(self):
        creds = open("credentials.txt", 'r')
        self.conn = pscg.connect(f"{creds.read()}")
        self.cur = self.conn.cursor()

    # убираем соединение
    def __del__(self):
        self.conn.commit()
        self.cur.close()

    # функция формирования запроса
    # по умолчанию условий запроса нет
    # cond_object -- столбец, на ячейки которого накладывается ограничение condition
    # cond_boundary -- переменная в условии, отвечающая за границы ограничения condition
    def request(self, columns, table, cond_object="None", condition="None", cond_boundary="None"):
        request = "SELECT ("
        # для строчного ввода одного элемента
        if type(columns) is str:
            request = request + columns + ") FROM " + table
        # разбиентие тюпла столбцов на составляющие и вставка в запрос
        elif type(columns) is tuple:
            for column in columns:
                request += column + ", "
            request = request[:-2]
            request += ") FROM " + table
        else:
            raise Exception("Неверный формат столбцов")

        # по умолчанию, без условий
        if condition == "None":
            return request

        # обработка условий
        request += " WHERE "
        if condition == "TYPE":
            request += cond_object + " in " + cond_boundary
        elif condition == "LIKE":
            request += cond_object + " LIKE " + cond_boundary + " ESCAPE ''"
        elif condition == "BETWEEN":
            request += cond_object + " BETWEEN " + cond_boundary
        elif condition == "!=":  # equal to IS NOT
            request += cond_object + " != " + cond_boundary
        elif condition == ">":
            request += cond_object + " > " + cond_boundary
        elif condition == "=":
            request += cond_object + " = " + cond_boundary
        elif condition == "<":
            request += cond_object + " < " + cond_boundary
        elif condition == ">=":
            request += cond_object + " >= " + cond_boundary
        elif condition == "<=":
            request += cond_object + " <= " + cond_boundary
        else:
            raise Exception("Неверные условия")

        # возврат запроса с учетом условий
        return request

    # вызов условия, который предварительно либо пишем вручную, либо формируем в фукнции request
    def execute(self, request):
        self.cur.execute(request)
        data = self.cur.fetchall()
        return tuple(data)

    # функция наложения правила порядка отображения для запроса (т.е. сортировка по колоннам в orders)
    def sort_request(self, request, orders):
        # проверяем, есть ли в запросе порядок
        # если None, порядка в запросе не будет
        if orders != "None" and orders != ('None',):
            request += " ORDER BY "
            for order in orders:
                request += order
                request += ", "
            request = request[:-2]
            print(request)
            return request
        else:
            return request


# класс окна приложения, в котором определяется положение и связи кнопок/полей с функциями ниже
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # основное окно приложения
        MainWindow.setObjectName("MainWindow")  # имя приложения в шапке
        MainWindow.resize(643, 764)  # размер окна
        self.centralwidget = QtWidgets.QWidget(MainWindow)  # виджет окна
        self.centralwidget.setObjectName("centralwidget")  # имя для обращение к окну в коде

        # надпись в верху окна, сама надпись внесена в след. функции
        self.label = QtWidgets.QLabel(self.centralwidget)  # объявляем виджет
        self.label.setGeometry(QtCore.QRect(250, 30, 141, 20))  # сама надпись умещается в рамке с координатами углов
        font = QtGui.QFont()  # шрифт надписи
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # надпись 2, она же надпись над окном выбора порядка
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(190, 570, 81, 21))
        self.label_2.setObjectName("label_2")

        # кнопка для выполнения сформированного запроса
        self.go_button = QtWidgets.QPushButton(self.centralwidget)
        self.go_button.setGeometry(QtCore.QRect(350, 610, 171, 71))
        self.go_button.setObjectName("go_button")
        self.go_button.clicked.connect(self.show_data)  # при нажатии выполняем функцию show_data

        # кнопка для начала работы с приложением, при нажатии которой появятся таблицы в БД
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(150, 240, 75, 23))
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.choose_table)

        # пин (кнопка с отметкой), нажатие на которую выбирает условие TYPE
        self.type_button = QtWidgets.QRadioButton(self.centralwidget)
        self.type_button.setGeometry(QtCore.QRect(340, 400, 82, 17))
        self.type_button.setObjectName("type_button")
        self.type_button.clicked.connect(lambda: self.choose_condition("TYPE"))  # привязываем функцию с аргументом через лямбда-функцию

        # условие LIKE
        self.like_button = QtWidgets.QRadioButton(self.centralwidget)
        self.like_button.setGeometry(QtCore.QRect(340, 420, 82, 17))
        self.like_button.setObjectName("like_button")
        self.like_button.clicked.connect(lambda: self.choose_condition("LIKE"))

        # условие BETWEEN
        self.between_button = QtWidgets.QRadioButton(self.centralwidget)
        self.between_button.setGeometry(QtCore.QRect(340, 440, 82, 17))
        self.between_button.setObjectName("between_button")
        self.between_button.clicked.connect(lambda: self.choose_condition("BETWEEN"))

        # условие !=
        self.inequal_button = QtWidgets.QRadioButton(self.centralwidget)
        self.inequal_button.setGeometry(QtCore.QRect(340, 460, 82, 17))
        self.inequal_button.setObjectName("inequal_button")
        self.inequal_button.clicked.connect(lambda: self.choose_condition("!="))

        # условие =
        self.equal_button = QtWidgets.QRadioButton(self.centralwidget)
        self.equal_button.setGeometry(QtCore.QRect(340, 480, 82, 17))
        self.equal_button.setObjectName("equal_button")
        self.equal_button.clicked.connect(lambda: self.choose_condition("="))

        # условие >
        self.bigger_button = QtWidgets.QRadioButton(self.centralwidget)
        self.bigger_button.setGeometry(QtCore.QRect(410, 460, 82, 17))
        self.bigger_button.setObjectName("bigger_button")
        self.bigger_button.clicked.connect(lambda: self.choose_condition(">"))

        # условие >=
        self.bigger_or_equal_button = QtWidgets.QRadioButton(self.centralwidget)
        self.bigger_or_equal_button.setGeometry(QtCore.QRect(410, 480, 82, 17))
        self.bigger_or_equal_button.setObjectName("bigger_or_equal_button")
        self.bigger_or_equal_button.clicked.connect(lambda: self.choose_condition(">="))

        # условие <
        self.lesser_button = QtWidgets.QRadioButton(self.centralwidget)
        self.lesser_button.setGeometry(QtCore.QRect(470, 460, 82, 17))
        self.lesser_button.setObjectName("lesser_button")
        self.lesser_button.clicked.connect(lambda: self.choose_condition("<"))

        # условие =<
        self.lesser_or_equal_button = QtWidgets.QRadioButton(self.centralwidget)
        self.lesser_or_equal_button.setGeometry(QtCore.QRect(470, 480, 82, 17))
        self.lesser_or_equal_button.setObjectName("lesser_or_equal_button")
        self.lesser_or_equal_button.clicked.connect(lambda: self.choose_condition("=<"))

        # строка для ввода cond_boundary
        self.condition_boundary_text = QtWidgets.QTextEdit(self.centralwidget)
        self.condition_boundary_text.setGeometry(QtCore.QRect(70, 530, 501, 31))
        self.condition_boundary_text.setObjectName("condition_boundary_text")
        self.condition_boundary_text.setPlaceholderText("None")  # текст по умолчанию (т.е. для отсутствия ограничений)

        # пин для отсутствия условий
        self.None_button = QtWidgets.QRadioButton(self.centralwidget)
        self.None_button.setGeometry(QtCore.QRect(430, 400, 101, 21))
        self.None_button.setObjectName("None_button")
        self.None_button.clicked.connect(lambda: self.choose_condition("None"))

        # поле с выбором таблиц
        # использован layout на этапе проектирования внешнего вида окна
        # layout позволяет избежать путаницы с размером и положении полей при изменении таковых у других объектов, таких как основное окно или соседние поля
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 270, 241, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.tables_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)  # объявляем layout
        self.tables_layout.setContentsMargins(0, 0, 0, 0)  # устанавливаем допустимый выход данных за пределы layout (т.е. выходить они у нас не будут)
        self.tables_layout.setObjectName("tables_layout")
        self.tables_list = QtWidgets.QListWidget(self.verticalLayoutWidget)  # создаем виджет в границах layout'а, который мы привяжем ниже
        self.tables_list.setObjectName("tables_list")
        self.tables_layout.addWidget(self.tables_list)  # привязываем виджет к layout
        self.tables_list.itemSelectionChanged.connect(self.choose_column)  # привязка функции, которая выполняется при изменении выбранных объектов в поле

        # поле с выбором столбцов
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(330, 270, 241, 111))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.columns_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.columns_layout.setContentsMargins(0, 0, 0, 0)
        self.columns_layout.setObjectName("columns_layout")
        self.columns_list = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.columns_list.setObjectName("columns_list")
        self.columns_list.setSelectionMode(QAbstractItemView.MultiSelection)  # включаем возможность выбора нескольких элементов в поле со столбцами
        self.columns_layout.addWidget(self.columns_list)
        self.columns_list.itemSelectionChanged.connect(self.show_condition_object)
        self.columns_list.itemSelectionChanged.connect(self.show_order)

        # поле с выбором объекта наложения условий
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(70, 400, 241, 111))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.condition_object_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.condition_object_layout.setContentsMargins(0, 0, 0, 0)
        self.condition_object_layout.setObjectName("condition_object_layout")
        self.condition_object_list = QtWidgets.QListWidget(self.verticalLayoutWidget_3)
        self.condition_object_list.setObjectName("condition_object_list")
        self.condition_object_layout.addWidget(self.condition_object_list)
        self.condition_object_list.itemSelectionChanged.connect(self.choose_condition_object)

        # поле отображения запроса
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(70, 60, 501, 171))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.contains_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.contains_layout.setContentsMargins(0, 0, 0, 0)
        self.contains_layout.setObjectName("contains_layout")
        self.view_contains = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.view_contains.setObjectName("view_contains")
        self.view_contains.setColumnCount(0)
        self.view_contains.setRowCount(0)
        self.contains_layout.addWidget(self.view_contains, 0, 0, 1, 1)

        # поле выбора столбцов, по которым строится порядок отображения результатов запроса
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(90, 590, 241, 111))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.order_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.order_layout.setContentsMargins(0, 0, 0, 0)
        self.order_layout.setObjectName("order_layout")
        self.order_list = QtWidgets.QListWidget(self.verticalLayoutWidget_4)
        self.order_list.setObjectName("order_list")
        self.order_layout.addWidget(self.order_list)
        self.order_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.order_list.itemSelectionChanged.connect(self.choose_order)

        # включаем отображение виджетов в основном окне
        MainWindow.setCentralWidget(self.centralwidget)  # выбор основного окна
        self.retranslateUi(MainWindow)  # подключаем возможность изменения надписей в окне
        QtCore.QMetaObject.connectSlotsByName(MainWindow)  # подключаем все виджеты

    # функция с обозначениями кнопок
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate  # функция нужна для внутренних переводов строк для библиотеки pyqt
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Database Viewer"))
        self.go_button.setText(_translate("MainWindow", "GO"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.type_button.setText(_translate("MainWindow", "Type"))
        self.like_button.setText(_translate("MainWindow", "Like"))
        self.between_button.setText(_translate("MainWindow", "Between"))
        self.inequal_button.setText(_translate("MainWindow", "!="))
        self.equal_button.setText(_translate("MainWindow", "="))
        self.bigger_button.setText(_translate("MainWindow", ">"))
        self.bigger_or_equal_button.setText(_translate("MainWindow", ">="))
        self.lesser_button.setText(_translate("MainWindow", "<"))
        self.lesser_or_equal_button.setText(_translate("MainWindow", "=<"))
        self.None_button.setText(_translate("MainWindow", "None"))
        self.label_2.setText(_translate("MainWindow", "Order by:"))

    # функция отображения таблиц
    def choose_table(self):
        # обнуляем выбор условий
        self.condition_object = "None"
        self.condition_boundary = "None"
        self.condition = "None"

        # создаем экземпляр класса Informer для получения таблиц
        info = Informer()
        tables = info.tables()

        # очищаем поле tables_list и вставляем в него таблицы при перевызове функции
        self.tables_list.clear()
        self.tables_list.addItems(tables)

    # функция отображения столбцов, аналогично таблицам
    def choose_column(self):
        info = Informer()
        # заносим сюда название выбранной таблицы в соотв. поле
        self.selected_table = self.tables_list.currentItem().text()
        columns = info.columns(self.selected_table)

        self.columns_list.clear()
        self.columns_list.addItems(columns)

    # функция отображения выбранных столбцов в поле для выбора объекта ограничения
    def show_condition_object(self):
        current_columns = self.columns_list.selectedItems()
        # делаем тюпл с названиями выбранных столбцов
        self.selected_columns = []
        for item in current_columns:
            self.selected_columns.append(item.text())
        self.selected_columns = tuple(self.selected_columns)

        self.condition_object_list.clear()
        # добавим кнопку None, если ограничение нужно убрать
        self.condition_object_list.addItem("None")
        self.condition_object_list.addItems(self.selected_columns)

    # функция возвращает имя выбранного объекта ограничений
    def choose_condition_object(self):
        self.condition_object = self.condition_object_list.currentItem().text()

    # функция возвращает ограничение, которое передавалось как аргумент на кнопках при нажатии с помощью лямбда-функции
    def choose_condition(self, cond):
        self.condition = cond

    # функция отображения выбранных столбцов, нужная чтобы выбрать порядок сортировки вывода запроса
    def show_order(self):
        current_columns = self.columns_list.selectedItems()
        self.selected_columns = []
        for item in current_columns:
            self.selected_columns.append(item.text())
        self.selected_columns = tuple(self.selected_columns)

        self.order_list.clear()
        self.order_list.addItem("None")
        self.order_list.addItems(self.selected_columns)

    # определяем столбцы для выстроения порядка по выбранным в соотв. поле
    def choose_order(self):
        current_orders = self.order_list.selectedItems()
        self.orders = []
        for item in current_orders:
            self.orders.append(item.text())
        self.orders = tuple(self.orders)

    # функция для вывода результата запроса
    def show_data(self):
        # получаем введенное в строку условий значение в виде строки
        self.condition_boundary = self.condition_boundary_text.toPlainText()

        # очищаем поле при перевызове
        while self.view_contains.rowCount() > 0:
            self.view_contains.removeRow(0)

        # экземпляр класса для создания и выполнения запроса
        data_miner = Fetcher()

        # получаем строку с именем таблицы в виде строки (а не экземпляров класса item библиотеки pyqt)
        self.selected_table = self.tables_list.currentItem().text()

        # получаем тюпл с именами столбцов в виде строк
        current_columns = self.columns_list.selectedItems()
        self.selected_columns = []
        for item in current_columns:
            self.selected_columns.append(item.text())
        if len(self.selected_columns) != 1:
            self.selected_columns = tuple(self.selected_columns)
        else:
            self.selected_columns = self.selected_columns[0]

        # формируем запрос с определенными ранее аргументами
        req = data_miner.request(self.selected_columns, self.selected_table, self.condition_object, self.condition, self.condition_boundary)
        # че там по порядку?
        try:
            req = data_miner.sort_request(req, self.orders)
        except AttributeError:
            self.orders = "None"
            req = data_miner.sort_request(req, self.orders)
        print(req)  # контроль правильности запроса (просто в консоль выводит при формировании)

        data = data_miner.execute(req)  # выполнение запроса

        # добавление нужного количества столбцов в поле-таблицу с выводом
        self.view_contains.setColumnCount(len(self.selected_columns))
        # проставляем имена столбцов
        self.view_contains.setHorizontalHeaderLabels(list(self.selected_columns))

        # заполняем таблицу
        for item in data:
            row_count = self.view_contains.rowCount()  # текущее количество строк (текущая строка, по сути)
            self.view_contains.setRowCount(row_count + 1)  # добавляем одну
            # запрос возвращается в каком-то НЕПОТРЕБНОМ виде, как тюпл из тюплов, а внутри второго одна единственная строка и None
            nums = tuple(map(str, item[0][1:-1].split(',')))  # разбиваем полученное НЕПОТРЕБСТВО на удобный тюпл со строками для отображения
            # заполняем новую строчку таблицы cells содержимым тюпла
            cells = []
            for i in range(len(nums)):
                cells.append(QTableWidgetItem(str(nums[i])))
            # вставляем cells по порядку в строчку по столбикам
            for i in range(len(self.selected_columns)):
                if cells[i] is not None:
                    self.view_contains.setItem(row_count, i, cells[i])
                else:
                    self.view_contains.setItem(row_count, i, " ")


# тут запуск программы
def main():
    app = QtWidgets.QApplication(sys.argv)  # объявляем наше приложение
    MainWindow = QtWidgets.QMainWindow()  # основное окно
    ui = Ui_MainWindow()  # ui = user interface, по сути объявляем интерфейс
    ui.setupUi(MainWindow)  # сетапим расположение (внутри setupUi будет вызов функции с сетапом надписей и т.д.)
    MainWindow.show()  # отображаем наше окошко!
    sys.exit(app.exec_())  # закрытие на крестик


# я вам ЗАПРЕЩАЮ запускаться при добавлении этого модуля в другие проекты
if __name__ == "__main__":
    main()
