"""Модуль для приема данных в сети"""
import socket
import asyncio
import struct
from courier import INS, SNS, BNR, DSC, SRNS, Time, Date, sns_data, ins_data
from gui import *
from dynamics import app_exec
import dynamics as graphs


def format_data(data):
    """Метод для форматированния данных в читаемый вариант"""

    formatted_data = ""
    for key, value in data.items():
        if isinstance(value, dict):
            formatted_data += f"{key} = {value['value']}\n"
        elif isinstance(value, int):
            formatted_data += f"{key} = {value}\n"
        elif isinstance(value, float):
            formatted_data += f"{key} = {value}\n"
        elif isinstance(value, Time):
            formatted_data += f"{key} = {value.hours}:{value.minute}:{value.second}\n"
        elif isinstance(value, Date):
            formatted_data += f"{key} = {value.years}-{value.months}-{value.days}\n"
        elif isinstance(value, SRNS):
            formatted_data += f"{key} = {value.mode}, {value.sub_modes}, {value.product_fail}\n"
        elif isinstance(value, BNR):
            formatted_data += f"{key} = {value.value}\n"
    return formatted_data


def receive_data(port, ins, sns):
    """Метод для приема данных"""

    # объявляем приложение
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = UI_Window()
    ui.setup_ui(window)
    window.show()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("127.0.0.1", port))
        for i in range(10):
            QtCore.QCoreApplication.processEvents()
            # QtTest.QTest.qWait(1)

            data, _ = s.recvfrom(1024)
            data_len = struct.unpack("!B", data[:1])[0]
            offset = 1
            received_data = {}

            try:
                for _ in range(data_len):
                    key_len = struct.unpack("!I", data[offset:offset + 4])[0]
                    offset += 4
                    key = data[offset:offset + key_len].decode()
                    offset += key_len
                    address = struct.unpack("!I", data[offset:offset + 4])[0]
                    offset += 4
                    value = struct.unpack("!f", data[offset:offset + 4])[0]
                    offset += 4
                    max_value = struct.unpack("!f", data[offset:offset + 4])[0]
                    offset += 4
                    received_data[key] = {"address": address, "value": value, "max_value": max_value}

                    # Добавляем для SRNS
                    mode = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1
                    sub_modes = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1
                    product_fail = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1

                    # Добавляем для Time
                    hours = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1
                    minute = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1
                    second = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1

                    # Добавляем для Date
                    empty_1 = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1
                    years = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1
                    months = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1
                    days = struct.unpack("!B", data[offset:offset + 1])[0]
                    offset += 1

                    received_data[key] = {
                        "address": address,
                        "value": value,
                        "max_value": max_value,
                        "mode": mode,
                        "sub_modes": sub_modes,
                        "product_fail": product_fail,
                        "hours": hours,
                        "minute": minute,
                        "second": second,
                        "empty_1": empty_1,
                        "years": years,
                        "months": months,
                        "days": days
                    }
            except TypeError:
                pass
            except struct.error:
                pass

            data = ''
            for item, contains in ins_data.items():
                value = contains['value']
                data += f'{item} = {value}\n'
            ui.output_data("Полученны данные ИНС:")
            ui.output_data(data)

            ins.start_system()
            ins.initialize_calibration()
            ins.update_navigation_data(received_data)

            data = ''
            for item, contains in sns_data.items():
                value = contains['value']
                data += f'{item} = {value}\n'
            ui.output_data("Полученны данные CНС:")
            ui.output_data(data)

            sys.exit(app_exec(app))


def main():
    # Создаем объекты ИНС и СНС
    ins = INS()
    sns = SNS()

    receive_data(12346, INS(), SNS())
    graphs.show()

    loop = asyncio.get_event_loop()
    receiver_task = loop.create_task(receive_data(12346, ins, sns))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        receiver_task.cancel()
        loop.run_until_complete(receiver_task)
        loop.close()


if __name__ == "__main__":
    main()
