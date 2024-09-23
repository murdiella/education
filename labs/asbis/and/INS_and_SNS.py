from ctypes import Structure as s
from data import BNR, DSC, Time, Date, SRNS
from time import sleep
from data import coder_value, coder_address


class INS(s):
    _fields_ = [("latitude", BNR),
                ("longitude", BNR),
                ("height", BNR),
                ("true_course", BNR),
                ("pitch", BNR),
                ("roll", BNR),
                ("vel_nor", BNR),
                ("vel_west", BNR),
                ("vel_ver", BNR),
                ("ax", BNR),
                ("az", BNR),
                ("ay", BNR),
                ("status_word", DSC)
                ]

    def __init__(self):
        super(INS, self).__init__()

    def control(self):
        sleep(20)
        self.status_word = DSC(coder_address(address=270))
        self.status_word.not_init_data = 1
        self.status_word.servic_ins = 1
        print(self.status_word.not_init_data, self.status_word.servic_ins)

    def preparation(self):
        self.status_word.prep = 1
        print(self.status_word.not_init_data, self.status_word.servic_ins, self.status_word.prep)
        self.status_word.not_init_data = 0
        print(self.status_word.not_init_data)
        sleep(120)

    def navigation(self, data_dict):
        attributes = [x[0] for x in self._fields_]
        for attr in attributes:
            if attr != "status_word":
                setattr(self, attr,
                        BNR(coder_address(address=data_dict[attr]["address"]),
                            coder_value(value=data_dict[attr]["value"], n_bits=20,
                                      h_price=data_dict[attr]["h_price"]), 0, 1))


class SNS(s):
    _fields_ = [("h", BNR),
                ("h_dop", BNR),
                ("v_dop", BNR),
                ("ground_angle", BNR),
                ("cur_lat", BNR),
                ("cur_lat_exac", BNR),
                ("cur_long", BNR),
                ("cur_long_exac", BNR),
                ("delay", BNR),
                ("cur_time_eld", Time),
                ("cur_time_young", BNR),
                ("V_h", BNR),
                ("date", Date),
                ("feature", SRNS)
                ]

    def __init__(self):
        super(SNS, self).__init__()

    def control(self):
        sleep(20)
        self.feature = SRNS(coder_address(address=273))
        self.feature.mode = 2
        self.feature.sub_modes = 1
        self.feature.product_fail = 0
        print(self.feature.mode, self.feature.sub_modes, self.feature.product_fail)
        sleep(120)

    def navigation(self, data_dict):
        attributes = [x[0] for x in self._fields_]
        for attr in attributes:
            if (attr != "cur_time_eld") and (attr != "date") and (attr != "feature"):
                setattr(self, attr,
                        BNR(coder_address(address=data_dict[attr]["address"]),
                            coder_value(value=data_dict[attr]["value"], n_bits=20,
                                      h_price=data_dict[attr]["h_price"])))
        hours, minutes, seconds = data_dict["cur_time_eld"]["value"].split(",")
        self.cur_time_eld = Time(coder_address(address=data_dict["cur_time_eld"]["address"]), int(hours), int(minutes),
                                 int(seconds))
        years, months, days = data_dict["date"]["value"].split(",")
        self.date = Date(coder_address(address=data_dict["date"]["address"]), int(years), int(months), int(days))
        self.feature = SRNS(coder_address(address=data_dict["feature"]["address"]))



