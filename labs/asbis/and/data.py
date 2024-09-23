from ctypes import Structure as s, c_ulong

def coder_value(value, n_bits: int, h_price):
    return int(2 ** (n_bits - 1) * value / h_price)

def coder_address(address):
    str_addr = str(address)
    coder_addr = 0
    for i in range(len(str_addr)):
        coder_addr += int(int(str_addr[i]) * 8 ** (len(str_addr) - i - 1))
    return coder_addr

def decode(value, n_bit, h_price):
    return h_price * value / 2 ** (n_bit - 1)


# Задаем исходные значения
values = {
    # Протокол передачи ИНС
    "latitude": {
        'address': 310, 'value': 22.5, "h_price": 90
    },
    "longitude": {
        'address': 311, 'value': 22.5, "h_price": 90
    },
    "height": {
        'address': 361, 'value': 3048, "h_price": 19975.3728
    },
    "true_course": {
        'address': 314, 'value': 10, "h_price": 90
    },
    "pitch": {
        'address': 324, 'value': 5, "h_price": 90
    },
    "roll": {
        'address': 325, 'value': 45, "h_price": 90
    },
    "vel_nor": {
        'address': 366, 'value': 102.888, "h_price": 1053.5822
    },
    "vel_west": {
        'address': 367, 'value': 102.888, "h_price": 1053.5822
    },
    "vel_ver": {
        'address': 365, 'value': 3.048, "h_price": 83.2307
    },
    "ax": {
        'address': 331, 'value': 0.196133, "h_price": 19.62
    },
    "az": {
        'address': 332, 'value': 0.98066, "h_price": 19.62
    },
    "ay": {
        'address': 333, 'value': 0.98066, "h_price": 19.62
    },
    "status_word": {
        'address': 270
    },
    # Протокол передачи СНС
    "h": {
        'address': 76, 'value': 9834, "h_price": 65536
    },
    "h_dop": {
        'address': 101, 'value': 312, "h_price": 512
    },
    "v_dop": {
        'address': 102, 'value': 100, "h_price": 512
    },
    "ground_angle": {
        'address': 103, 'value': 45, "h_price": 90
    },
    "cur_lat": {
        'address': 110, 'value': 45, "h_price": 90
    },
    "cur_lat_exac": {
        'address': 120, 'value': 0.000057, "h_price": 0.00008583
    },
    "cur_long": {
        'address': 111, 'value': 45, "h_price": 90
    },
    "cur_long_exac": {
        'address': 121, 'value': 0.000057, "h_price": 0.00008583
    },
    "delay": {
        'address': 113, 'value': 57, "h_price": 512
    },
    "cur_time_eld": {
        'address': 150, 'value': "7,35,8", "h_price": "16,32,32"
    },
    "cur_time_young": {
        'address': 140, 'value': 10, "h_price": 512
    },
    "V_h": {
        'address': 165, 'value': 231, "h_price": 16384
    },
    "date": {
        'address': 260, 'value': "1,12,22", "h_price": ""
    },
    "feature": {
        'address': 273, 'value': 1, "h_price": ""
    }
}

# Создаем классы для различных форматов параметров

class BNR(s):
    _fields_ = [("address", c_ulong, 8),
                ("value", c_ulong, 20),
                ("empty", c_ulong, 1),
                ("matrix", c_ulong, 2),
                ("p", c_ulong, 1)
                ]


class DSC(s):
    _fields_ = [
        ("address", c_ulong, 8),
        ("sdi", c_ulong, 2),
        ("prep", c_ulong, 1),
        ("control", c_ulong, 1),
        ("navigation", c_ulong, 1),
        ("gyrocomp", c_ulong, 1),
        ("empty_1", c_ulong, 1),
        ("restart", c_ulong, 1),
        ("init_exh", c_ulong, 3),
        ("servic_heat", c_ulong, 1),
        ("control_temp", c_ulong, 1),
        ("not_init_data", c_ulong, 1),
        ("not_reception", c_ulong, 1),
        ("servic_ins", c_ulong, 1),
        ("ready_a", c_ulong, 1),
        ("ready", c_ulong, 1),
        ("empty_2", c_ulong, 3),
        ("sm", c_ulong, 2),
        ("p", c_ulong, 1)
    ]


class Time(s):
    _fields_ = [("address", c_ulong, 8),
                ("hours", c_ulong, 5),
                ("minute", c_ulong, 6),
                ("second", c_ulong, 6),
                ("empty", c_ulong, 4),
                ("sm", c_ulong, 2),
                ("p", c_ulong, 1)
                ]


class Date(s):
    _fields_ = [("address", c_ulong, 8),
                ("empty_1", c_ulong, 2),
                ("years", c_ulong, 8),
                ("months", c_ulong, 5),
                ("days", c_ulong, 6),
                ("matrix", c_ulong, 2),
                ("empty", c_ulong, 1)
                ]


class SRNS(s):
    _fields_ = [("address", c_ulong, 8),
                ("request_data", c_ulong, 1),
                ("sns_type", c_ulong, 3),
                ("almanac_gps", c_ulong, 1),
                ("almanac_glonas", c_ulong, 1),
                ("mode", c_ulong, 2),
                ("sub_modes", c_ulong, 1),
                ("sign_time", c_ulong, 1),
                ("empty_1", c_ulong, 2),
                ("diff_mode", c_ulong, 1),
                ("empty_2", c_ulong, 1),
                ("product_fail", c_ulong, 1),
                ("threshold", c_ulong, 1),
                ("coord_system", c_ulong, 2),
                ("empty_3", c_ulong, 3),
                ("matrix", c_ulong, 2),
                ("parity", c_ulong, 1)
                ]


