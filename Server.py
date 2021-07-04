# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:10:09 2020

@author: Kartik
"""

import socket
import pandas as pd
from datetime import timedelta,date
import threading
#user defined exception class to handle exception raised
class InvalidUser(Exception):
    pass
class InvalidPower(Exception):
    pass
# Thread function to handle each client
def ClientHandler(conn,addr,lock):
    """
    curr: socket object
    addr: tuple containing host and port connected
    lock: synchronization object
    """
    data=pd.DataFrame()
    amount=25.0
    print('connected by',addr)
    conn.sendall("New User?[y/n]".encode('utf-8'))
    new=conn.recv(1024).decode('utf-8')
    if new=='y':
        try:
            conn.sendall("Enter ID".encode('utf-8'))
            id = conn.recv(1024).decode('utf-8')
            conn.sendall("Enter password".encode('utf-8'))
            passwd = conn.recv(1024).decode('utf-8')
            conn.sendall("Enter name".encode('utf-8'))
            name = conn.recv(1024).decode('utf-8')
            conn.sendall("Enter Last Meter Reading".encode('utf-8'))
            prevReading = float(conn.recv(1024).decode('utf-8'))
            new_row = pd.DataFrame({"User ID":id,"Password":passwd,"User Name":name,"Last meter reading":prevReading},index=[0])
            lock.acquire(False)
            df = pd.read_excel("Book1.xlsx")
            df = pd.concat([new_row, df]).reset_index(drop = True)
            df.to_excel("Book1.xlsx",index=False)
            lock.release()
            conn.sendall("Thankyou".encode('utf-8'))
        except:
            print("Error Occured")
        finally:
            print("Closing connection",addr)
            conn.close()
    else:
        try:
            df = pd.read_excel("Book1.xlsx")
            conn.sendall("Electricity bill calculation".encode('utf-8'))
            conn.sendall("Enter User ID".encode('utf-8'))
            id = conn.recv(1024).decode('utf-8')
            conn.sendall("Enter Password".encode('utf-8'))
            passwd = conn.recv(1024).decode('utf-8')
            if id in df["User ID"].values:
                data = df[df["User ID"]==id]
                if passwd not in data["Password"].values:
                    raise InvalidUser
            else:
                raise InvalidUser
            indx = data.index.values[0]
            name = data.at[indx,"User Name"]
            conn.sendall(("Welcome "+name).encode('utf-8'))
            prevReading = data.at[indx,"Last meter reading"]
            conn.sendall(("Previous reading ="+str(prevReading)).encode('utf-8'))
            conn.sendall("\nEnter current reading:".encode('utf-8'))
            currReading=float(conn.recv(1024).decode('utf-8'))
            power=currReading-prevReading
            if(power<0):
                raise InvalidPower
            if power<100:
                amount+=(power*1.5)
            elif power<200:
                amount=amount+(100*1.5)+(power-100)*2.5
            elif power<500:
                amount=amount+(100*1.5)+(100*2.5)+(power-200)*3.5
            else:
                amount=amount+(100*1.5)+(100*2.5)+(300*3.5)+(power-500)*4
            conn.sendall(("Amount is "+str(round(amount,2))).encode('utf-8'))
            conn.sendall(("\nAmount to be paid within "+str((date.today()+timedelta(days=10)))).encode('utf-8'))
            conn.sendall("\nUpating in DataBase..".encode('utf-8'))
            lock.acquire()
            df = pd.read_excel("Book1.xlsx")
            data = df[df["User ID"]==id]
            indx = data.index.values[0]
            df.at[indx,"Last meter reading"]=currReading
            df.to_excel("Book1.xlsx",index=False)
            lock.release()
            conn.sendall("Updated".encode('utf-8'))
            conn.sendall("Thankyou".encode('utf-8'))
        except InvalidUser:
            conn.sendall("Invalid user".encode('utf-8'))
        except InvalidPower:
            conn.sendall("Invalid reading".encode('utf-8'))
        finally:
            print("closing connection",addr)
            conn.close()

# Setup server socket
HOST = '127.0.0.1'  #local host ipv4 addr
PORT = 5000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST,PORT))
# acquire lock for synchronization
lock = threading.Lock()
print("Server running")
try:
    s.listen()
    while True:
        conn, addr = s.accept()
        threading.Thread(target=ClientHandler,args = (conn, addr, lock)).start()
except:
    print("Closing connection")
    s.close()
