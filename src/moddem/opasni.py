'''
Created on 22 Aug 2020

@author: dkr85djo
'''

import socket


HOST = socket.gethostbyname(socket.gethostname())

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))

s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

while True:        
    try:        
        print(s.recvfrom(65565)[0].decode(encoding="utf-8", errors='ignore'))       
        
    except KeyboardInterrupt:        
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        break
