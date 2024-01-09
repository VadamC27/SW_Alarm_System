#!/usr/bin/env python

import sqlite3
from sqlite3 import OperationalError
import Adafruit_BBIO.UART as UART
import serial
from datetime import datetime

conn = sqlite3.connect('sam.db')
c = conn.cursor()

pin = 'P9_26'
UART.setup("UART1") # Konfiguracja UART1
ser = serial.Serial(port="/dev/ttyS1", baudrate=9600) # Konfiguracja portu szeregowego
ser.close()
ser.open()

while True:
    if ser.isOpen():
      data = ser.readline()
    message = data[0:4]

    if message == "alrm":
        if data[4] == "2":
            date = date.now()
            c.execute("INSERT INTO zarejestrowan_ruch(data, id_czujnika) values(?,?)",date,2)
        elif data[4] == "3":
            date = date.now()
            c.execute("INSERT INTO zarejestrowan_ruch(data, id_czujnika) values(?,?)",date,3)       

    elif message == "code":
        code = data[4:8]
        query = f"SELECT COUNT(*) FROM tabela_kody WHERE kod = '{code}' AND LENGTH(kod) = 4;"
        c.execute(query)
        result = c.fetchone()[0]
        if result>0 :
            message = "1"
            ser.write(message.encode()) #kod w arduino nie jest w cudzysłowiach!!!!!
        else:
            message = "0"
            ser.write(message.encode()) #kod w arduino nie jest w cudzysłowiach!!!!!

    elif message == "errn":
        print("Nieznany czujnik")
       
    
    