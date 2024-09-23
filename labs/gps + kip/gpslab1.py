import numpy as np
from pyrtcm import RTCMReader

# mu = 3.9860050E14
# OMGE = 7.2921151467E-5
# SC2RAD = 3.1415926535898
P2_5 = 0.03125
P2_19 = 1.907348632812500E-06
P2_29 = 1.862645149230957E-09
P2_31 = 4.656612873077393E-10
P2_33 = 1.164153218269348E-10
P2_43 = 1.136868377216160E-13
P2_55 = 2.775557561562891E-17


def main():
    with open('1019 - gpslab1.rtcm', 'rb') as file:
        f = file.read()
        # data = hashlib.sha256(f).hexdigest()
        data = RTCMReader.parse(f)
    print(data)

    tk = -10
    a = data.DF092 ** 2  # 1
    mu = 3.9860050e14  # 2
    deln = data.DF087
    n = np.sqrt(mu / (a ** 3)) + deln
    M0 = data.DF088 * 3.1415926535898  # 3
    M = M0 + tk * n
    e = data.DF090 * 2 ** -33  # 4

    def Ei(E_input):
        return M + e * np.sin(E_input)

    E = M
    for _ in range(3):
        E = Ei(E)
    nu = np.arctan2(np.sin(E) * np.sqrt(1 - e**2), np.cos(E) - e)  # 5
    w = data.DF099 * 3.1415926535898  # 6
    u = nu + w
    sin2u = np.sin(2 * u)  # 7
    cos2u = np.cos(2 * u)
    crs = data.DF086  # 8
    crc = data.DF098
    r = a * (1 - e * np.cos(E)) + crs * sin2u + crc * cos2u
    i0 = data.DF097 * 3.1415926535898  # 9
    idot = data.DF079 * 3.1415926535898
    cis = data.DF096
    cic = data.DF094
    i = i0 + idot * tk + cis * sin2u + cic * cos2u
    cus = data.DF091  # 10
    cuc = data.DF089
    u += cus * sin2u + cuc * cos2u
    xs = r * np.cos(u)  # 11
    ys = r * np.sin(u)
    omega_0 = data.DF095 * 3.1415926535898  # 12
    OMGd = data.DF100 * 3.1415926535898
    OMGE = 7.2921151467E-5
    omega = omega_0 + OMGd * tk - OMGE * tk
    sin_omega = np.sin(omega)  # 13
    cos_omega = np.cos(omega)
    x_ecef = xs * cos_omega - ys * np.cos(i) * sin_omega  # 14
    y_ecef = xs * sin_omega + ys * np.cos(i) * cos_omega
    z_ecef = ys * np.sin(i)
    print(x_ecef)
    print(y_ecef)
    print(z_ecef)


if __name__ == '__main__':
    main()
