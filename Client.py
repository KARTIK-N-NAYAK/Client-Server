# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:24:20 2020

@author: Kartik
"""

import socket
HOST = '127.0.0.1'
PORT = 5000
try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    print("Connected\n")
    print(s.recv(1024).decode('utf-8'))
    new=input()
    s.sendall(new.encode('utf-8'))
    if new == 'y':
        
        print(s.recv(1024).decode('utf-8'))
        s.sendall(input().encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        s.sendall(input().encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        s.sendall(input().encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        s.sendall(input().encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
    else:
        print(s.recv(1024).decode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        s.sendall(input().encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        s.sendall(input().encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        #print(s.recv(1024).decode('utf-8'))
        s.sendall(input().encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
except :
    print("Error occured")

finally :
    print("Closing connection")
    s.close()