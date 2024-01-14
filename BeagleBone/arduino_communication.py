#!/usr/bin/env python

import sqlite3
from sqlite3 import OperationalError
import Adafruit_BBIO.UART as UART
import serial
from datetime import datetime

# setup database
conn = sqlite3.connect('sam.db')
c = conn.cursor()

# setup communication
pin = 'P9_26'
UART.setup("UART1") # Config UART1
ser = serial.Serial(port="/dev/ttyS1", baudrate=9600) # Config serial port
ser.close()
ser.open()

# wait and handle incomming messages
while True:
    if ser.isOpen(): # decode message
        data = ser.readline().rstrip().decode('utf-8')
    message = data[0:4] # strip to code name
    print(data)
    #alarm message
    if message == "alrm":
        if data[4] == "2": # check sensor and insert data into SQL db 
            date = datetime.now()
            c.execute("INSERT INTO zarejestrowan_ruch(data, id_czujnika) values(?,?)",(date,2))
            conn.commit()
        elif data[4] == "3":
            date = datetime.now()
            c.execute("INSERT INTO zarejestrowan_ruch(data, id_czujnika) values(?,?)",(date,3))
            conn.commit()
    # get code message
    elif message == "code":
        code = data[4:8] # strip to only code numbers
        # chceck if code does exist in data base
        query = f"SELECT COUNT(*) FROM kody WHERE kod = '{code}' AND LENGTH(kod) = 4;"
        c.execute(query)
        result = c.fetchone()[0]
        # reply to arduino
        if result>0 : # code found
            message = "1"
            ser.write(message.encode()) 
        else:
            message = "0"
            ser.write(message.encode()) 
    elif message == "errn": # print out error
        print("Nieznany czujnik")
    # change state for armed information
    elif message == "armd":
        # for concurrent access info about alarm is stored in database
        if data[4] == "1":
            c.execute("UPDATE isTriggered SET state = '1';")
            conn.commit()
        elif data[4] == "0":
            c.execute("UPDATE isTriggered SET state = '0';")
            conn.commit()
        else:
            print("Error: armed state unknown!!!")

    
    
