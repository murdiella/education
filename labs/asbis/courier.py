"""Модуль для отправки данных по сети"""
import socket
import asyncio
import struct
from threading import Event


class BNR:
    """Класс для формата параметра BNR"""

    def __init__(self, address=0, value=0.0, empty=0, matrix=0, p=0):
        """Конструктор класса"""

        self.address = address
        self.value = value
        self.empty = empty
        self.matrix = matrix
        self.p = p

    def __repr__(self):
        return f"BNR(address={self.address}, value={self.value}, empty={self.empty}, matrix={self.matrix}, p={self.p})"


class DSC:
    """Класс для формата параметра DSC"""

    def __init__(self, address=0, sdi=0, prep=0, control=0, navigation=0, gyrocomp=0, empty_1=0, restart=0, init_exh=0,
                 servic_heat=0, control_temp=0, not_initialized=0, not_reception=0, service_inspection=0, ready_a=0, ready=0,
                 empty_2=0, sm=0, p=0):
        """Конструктор класса"""

        self.address = address
        self.sdi = sdi
        self.prep = prep
        self.control = control
        self.navigation = navigation
        self.gyrocomp = gyrocomp
        self.empty_1 = empty_1
        self.restart = restart
        self.init_exh = init_exh
        self.servic_heat = servic_heat
        self.control_temp = control_temp
        self.not_initialized = not_initialized
        self.not_reception = not_reception
        self.service_inspection = service_inspection
        self.ready_a = ready_a
        self.ready = ready
        self.empty_2 = empty_2
        self.sm = sm
        self.p = p

    def __getitem__(self, key):
        """Оверлоад метода получения атрибута класса"""

        return getattr(self, key)

    def __repr__(self):
        """Оверлоад получения информации об объекте класса"""

        return (
            f"DSC(address={self.address}, sdi={self.sdi}, prep={self.prep}, control={self.control}, navigation={self.navigation}, "
            f"gyrocomp={self.gyrocomp}, empty_1={self.empty_1}, restart={self.restart}, init_exh={self.init_exh}, "
            f"servic_heat={self.servic_heat}, control_temp={self.control_temp}, not_init_data={self.not_initialized}, "
            f"not_reception={self.not_reception}, servic_ins={self.service_inspection}, ready_a={self.ready_a}, ready={self.ready}, "
            f"empty_2={self.empty_2}, sm={self.sm}, p={self.p})"
        )

class Time:
    """Класс для формата параметра Time"""

    def __init__(self, address=0, hours=0, minute=0, second=0, empty=0, sm=0, p=0):
        """Конструктор класса"""

        self.address = address
        self.hours = hours
        self.minute = minute
        self.second = second
        self.empty = empty
        self.sm = sm
        self.p = p


class Date:
    """Класс для формата параметра Date"""

    def __init__(self, address=0, empty_1=0, years=0, months=0, days=0, matrix=0, empty=0):
        """Конструктор класса"""

        self.address = address
        self.empty_1 = empty_1
        self.years = years
        self.months = months
        self.days = days
        self.matrix = matrix
        self.empty = empty


class SRNS:
    """Класс для формата параметра SRNS"""

    def __init__(self, address=0, request_data=0, sns_type=0, almanac_gps=0, almanac_glonas=0, mode=0, sub_modes=0,
                 sign_time=0, empty_1=0, diff_mode=0, empty_2=0, product_fail=0, threshold=0, coord_system=0, empty_3=0,
                 matrix=0, parity=0):
        """Конструктор класса"""

        self.address = address
        self.request_data = request_data
        self.sns_type = sns_type
        self.almanac_gps = almanac_gps
        self.almanac_glonas = almanac_glonas
        self.mode = mode
        self.sub_modes = sub_modes
        self.sign_time = sign_time
        self.empty_1 = empty_1
        self.diff_mode = diff_mode
        self.empty_2 = empty_2
        self.product_fail = product_fail
        self.threshold = threshold
        self.coord_system = coord_system
        self.empty_3 = empty_3
        self.matrix = matrix
        self.parity = parity


def encode_value(value, n_bits, max_value):
    """Функция для нахождения количества бит на хранение значения"""

    return int((2 ** (n_bits - 1)) * value / max_value) if max_value != 0 else 0


def encode_address(address):
    """Функция для формирования адреса"""

    return sum(int(digit) * (8 ** (len(str(address)) - i - 1))
               for i, digit in enumerate(str(address)))


class INS:
    """Класс протокола ИНС"""

    def __init__(self):
        """Конструктор класса"""

        self.attributes = {
            "latitude": BNR(),
            "longitude": BNR(),
            "height": BNR(),
            "heading": BNR(),
            "pitch_angle": BNR(),
            "roll_angle": BNR(),
            "velocity_north": BNR(),
            "velocity_west": BNR(),
            "velocity_z": BNR(),
            "acceleration_x": BNR(),
            "acceleration_y": BNR(),
            "acceleration_z": BNR(),
            "system_status": DSC()
        }

    def start_system(self):
        """Метод для режима подготовки"""

        wait_event = Event()
        # wait_event.wait(timeout=120)  # закомментировано в целях экономии времени
        self.attributes["system_status"].preparation = 1
        self.attributes["system_status"].not_initialized = 0

    def initialize_calibration(self):
        """Метод для режима контроля"""

        wait_event = Event()
        wait_event.set()  # Устанавливаем событие
        self.attributes["system_status"] = DSC(encode_address(270))
        self.attributes["system_status"].not_initialized = 1
        self.attributes["system_status"].service_inspection = 1

    def update_navigation_data(self, data_dict):
        """Метод для режима навигация"""

        for attr, value in data_dict.items():
            if attr in self.attributes and attr != "system_status":
                bnr_instance = self.attributes[attr]
                bnr_instance.address = encode_address(value["address"])
                bnr_instance.value = encode_value(value["value"], 20, value["max_value"])


class SNS:
    """Класс протокола СНС"""

    def __init__(self):
        """Конструктор класса"""

        self.height = BNR()
        self.height_doppler = BNR()
        self.velocity_doppler = BNR()
        self.ground_angle = BNR()
        self.current_latitude = BNR()
        self.exact_latitude = BNR()
        self.current_longitude = BNR()
        self.exact_longitude = BNR()
        self.delay = BNR()
        self.current_time_eld = Time()
        self.current_time_young = BNR()
        self.horizontal_velocity = BNR()
        self.date = Date()
        self.feature = SRNS()
        self.event = Event()

    def system_check(self):
        """Метод для системной проверки"""

        self.event.set()
        # self.event.wait(timeout=20)  # закомментировано в целях экономии времени
        self.feature = SRNS(encode_address(273))
        self.feature.mode = 2
        self.feature.sub_modes = 1
        self.feature.product_fail = 0
        # self.event.wait(timeout=120)

    def navigation_update(self, data_dict):
        """Метод для режима навигация"""

        attributes = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

        for attr in attributes:
            if attr in data_dict:
                bnr_instance = getattr(self, attr)
                bnr_instance.address = encode_address(data_dict[attr]["address"])
                bnr_instance.value = encode_value(data_dict[attr]["value"], 20, data_dict[attr]["max_value"])

        if "current_time_eld" in data_dict:
            hours, minutes, seconds = data_dict["current_time_eld"]["value"].split(",")
            self.current_time_eld.address = encode_address(data_dict["current_time_eld"]["address"])
            self.current_time_eld.hours = int(hours)
            self.current_time_eld.minute = int(minutes)
            self.current_time_eld.second = int(seconds)

        if "date" in data_dict:
            years, months, days = data_dict["date"]["value"].split(",")
            self.date.address = encode_address(data_dict["date"]["address"])
            self.date.years = int(years)
            self.date.months = int(months)
            self.date.days = int(days)

        if "feature" in data_dict:
            self.feature.address = encode_address(data_dict["feature"]["address"])


async def send_data(address, port, data, interval):
    "Метод для отправки данных"
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            serialized_data = struct.pack("!B", len(data))
            for key, value in data.items():
                serialized_data += struct.pack("!I", len(key.encode())) + key.encode()
                serialized_data += struct.pack("!I", value["address"])

                if "value" in value:
                    serialized_data += struct.pack("!f", value["value"])
                else:
                    serialized_data += struct.pack("!f", 0.0)
                if "max_value" in value:
                    serialized_data += struct.pack("!f", value["max_value"])
                else:
                    serialized_data += struct.pack("!f", 0.0)
                # Добавляем для SRNS
                if "mode" in value:
                    serialized_data += struct.pack("!B", value["mode"])
                else:
                    serialized_data += struct.pack("!B", 0)

                if "sub_modes" in value:
                    serialized_data += struct.pack("!B", value["sub_modes"])
                else:
                    serialized_data += struct.pack("!B", 0)

                if "product_fail" in value:
                    serialized_data += struct.pack("!B", value["product_fail"])
                else:
                    serialized_data += struct.pack("!B", 0)

                # Добавляем для Time
                if "hours" in value:
                    serialized_data += struct.pack("!B", value["hours"])
                else:
                    serialized_data += struct.pack("!B", 0)

                if "minute" in value:
                    serialized_data += struct.pack("!B", value["minute"])
                else:
                    serialized_data += struct.pack("!B", 0)

                if "second" in value:
                    serialized_data += struct.pack("!B", value["second"])
                else:
                    serialized_data += struct.pack("!B", 0)

                # Добавляем для Date
                if "empty_1" in value:
                    serialized_data += struct.pack("!B", value["empty_1"])
                else:
                    serialized_data += struct.pack("!B", 0)

                if "years" in value:
                    serialized_data += struct.pack("!B", value["years"])
                else:
                    serialized_data += struct.pack("!B", 0)

                if "months" in value:
                    serialized_data += struct.pack("!B", value["months"])
                else:
                    serialized_data += struct.pack("!B", 0)

                if "days" in value:
                    serialized_data += struct.pack("!B", value["days"])
                else:
                    serialized_data += struct.pack("!B", 0)


            s.sendto(serialized_data, (address, port))
            await asyncio.sleep(interval)


async def send_data_sns(address, port, data, interval):
    """Метод для отправки данных СНС"""
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            out_str = ''
            for item, contains in data.items():
                value = contains['value']
                out_str += f'{item} = {value}\n'
            # temp = '!'
            # for _ in range(len(out_str)):
            #     temp += 's'
            value = bytes(value, 'utf-8')
            out_str = struct.pack("I%ds" % (len(value),), len(value), value)
            s.sendto(out_str, (address, port))
            await asyncio.sleep(interval)


# Словари с данными для протоколов
ins_data = {
    "latitude": {"address": 310, "value": 10.5, "max_value": 180},
    "longitude": {"address": 311, "value": 20.7, "max_value": 180},
    "height": {'address': 361, 'value': 3048, "max_value": 39950},
    "heading": {'address': 314, 'value': 10, "max_value": 180},
    "pitch_angle": {'address': 324, 'value': 5, "max_value": 180},
    "roll_angle": {'address': 325, 'value': 45, "max_value": 180},
    "velocity_north": {'address': 366, 'value': 102.888, "max_value": 1053.5822},
    "velocity_west": {'address': 367, 'value': 102.888, "max_value": 1053.5822},
    "velocity_z": {'address': 365, 'value': 3.048, "max_value": 83.2307},
    "acceleration_x": {'address': 331, 'value': 0.196133, "max_value": 19.62},
    "acceleration_y": {'address': 332, 'value': 0.98066, "max_value": 19.62},
    "acceleration_z": {'address': 333, 'value': 0.98066, "max_value": 19.62},
    # "system_status": {"address": 270, "not_initialized": 0, "service_inspection": 0}
}

sns_data = {
    "height": {"address": 86, "value": 500, "max_value": 1000},
    "height_doppler": {'address': 101, 'value': 312, "max_value": 512},
    "velocity_doppler": {'address': 102, 'value': 100, "max_value": 512},
    "ground_angle": {'address': 103, 'value': 45, "max_value": 180},
    "current_latitude": {'address': 110, 'value': 45, "max_value": 180},
    "exact_latitude": {'address': 120, 'value': 0.000057, "max_value": 0.00008583},
    "current_longitude": {'address': 111, 'value': 45, "max_value": 180},
    "exact_longitude": {'address': 121, 'value': 0.000057, "max_value": 0.00008583},
    "delay": {'address': 113, 'value': 57, "max_value": 512},
    "current_time_eld": {'address': 150, 'value': "7,13,20", "max_value": ""},
    "current_time_young": {'address': 140, 'value': 10, "max_value": 512},
    "horizontal_velocity": {'address': 165, 'value': 231, "max_value": 16384},
    "date": {'address': 260, 'value': "1,12,22", "max_value": ""},
    # "feature": {"address": 273, "mode": 1, "sub_modes": 0, "product_fail": 0}
}

sns_datas = ''
for item, contains in sns_data.items():
    value = contains['value']
    sns_datas += f'{item} = {value}\n'


def main():
    """Основной исполняющий метод"""

    # Создаем объекты ИНС и СНС
    ins = INS()
    sns = SNS()

    # Запускаем асинхронные потоки для отправки данных
    loop = asyncio.get_event_loop()
    ins_sender_task = loop.create_task(send_data("127.0.0.1", 12346, ins_data, 10))
    sns_sender_task = loop.create_task(send_data_sns("127.0.0.1", 12346, sns_data, 10))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        ins_sender_task.cancel()
        sns_sender_task.cancel()
        loop.run_until_complete(asyncio.gather(sns_sender_task, ins_sender_task))
        loop.close()


if __name__ == '__main__':
    main()
