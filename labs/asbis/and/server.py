import socket as sc
from ctypes import *
from INS_and_SNS import INS, SNS
from data import decode

AF_INET = sc.AF_INET

sck = sc.socket(AF_INET, sc.SOCK_DGRAM)
addr = ('127.0.0.1', 12346)
sck.bind(addr)

def unpacking(ctype, buff):
    cstring = create_string_buffer(buff)
    ctype_instance = cast(pointer(cstring), POINTER(ctype)).contents
    return ctype_instance


while True:
    data = sck.recv(1024)
    if len(data) == 52:
        data_length = unpacking(INS, data)
        print(decode(data_length.latitude.value, 20, 90))
    if len(data) == 56:
        data_length = unpacking(SNS, data)
        print(decode(data_length.cur_lat.value, 20, 90))
sck.close()
