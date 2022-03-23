import socket as sck
import threading as thr 

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

portMax = 500
portMin = 200
ip = 'localhost'

for port in range(portMin,portMax, 1):
    result = s.connect_ex((ip,port))
    print(result)