import psycopg2 as pscg


# класс для получения информации о таблицах и их содержимом
# без условий к содержимому
class Informer:

    # создаем соединение
    def __init__(self):
        creds = open("credentials.txt", 'r')
        self.conn = pscg.connect(f"{creds.read()}")
        self.cur = self.conn.cursor()
        print('Informer connection opened')

    # убираем соединение
    def __del__(self):
        self.conn.commit()
        self.cur.close()
        print('Informer connection closed')

    # функция возвращает все таблицы в БД
    def tables(self):
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        unedited_list = self.cur.fetchall()

        tables = []
        for item in unedited_list:
            tables.append(item[0])

        return tuple(tables)

    # функция возвращает все имена столбцов из таблицы в БД
    def columns(self, table_name):
        self.cur.execute(f"SELECT * FROM {table_name}")
        column_names = [name[0] for name in self.cur.description]
        return tuple(column_names)


class Fetcher:

    # создаем соединение
    def __init__(self):
        creds = open("credentials.txt", 'r')
        self.conn = pscg.connect(f"{creds.read()}")
        self.cur = self.conn.cursor()
        print('Fetcher connection opened')

    # убираем соединение
    def __del__(self):
        self.conn.commit()
        self.cur.close()
        print('Fetcher connection closed')

    # функция формирования запроса
    def request(self, columns, table, cond_object=None, condition=None, cond_boundary=None):
        request = "SELECT ("
        if type(columns) is str:
            request = request + columns + ") FROM " + table
        elif type(columns) is tuple:
            for column in columns:
                request += column + ", "
            request = request[:-2]
            request += ") FROM " + table
        else:
            raise Exception("Wrong columns format")

        if condition is None:
            return request

        request += " WHERE "
        if condition == "TTYPE":
            if type(cond_boundary) is tuple:
                request += cond_object + " in ('"
                for condition in cond_boundary:
                    request += condition + "', '"
                request = request[:-3]
                request += ")"
            elif type(cond_boundary) is str:
                request += cond_object + " in '" + cond_boundary + "'"
            else:
                raise Exception("Wrong condition boundary type")
        elif condition == "LIKE":
            request += cond_object + " LIKE " + cond_boundary
        elif condition == "BETWEEN":
            if len(cond_boundary) != 2 or type(cond_boundary) is not tuple:
                raise Exception("Condition must be tuple of 2 numbers (a, b)")
            elif cond_boundary[0] > cond_boundary[1]:
                raise Exception("First number must be lesser than the second one")
            request += cond_object + " BETWEEN " + str(cond_boundary[0]) + " AND " + str(cond_boundary[1])
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

        return request

    def execute(self, request):
        self.cur.execute(request)
        data = self.cur.fetchall()
        return tuple(data)

    # функция наложения правила порядка отображения для запроса (т.е. сортировка по колоннам в orders)
    def sort_request(self, request, orders):
        request += " ORDER BY "
        for order in orders:
            request += order
            request += ", "
        request = request[:-2]
        print(request)
        return request


# функция запуска программы
def main():
    menchik = Informer()
    boychik = Fetcher()

    tabs = menchik.tables()
    cols = menchik.columns('experiment')
    conditions = ("TTYPE", "LIKE", "BETWEEN", "!=", ">", "=", "<", ">=", "<=")

    # print(tabs)
    # print(cols)
    cond = (cols[0], cols[3])
    cond2 = tuple(['bigint', 'integer'])
    # req = boychik.request(cond, tabs[3], "exp_id", "TTYPE", cond2)
    req = boychik.request(cols[3], tabs[3])
    print(req)
    data = boychik.execute(req)
    print(data)  # this is tuple of strings
    print(data[0][0])  # this is string

    print('nah im tired bye')


if __name__ == "__main__":
    main()
