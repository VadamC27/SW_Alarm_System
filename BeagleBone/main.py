#!/usr/bin/env python

from flask import Flask, render_template, request
import sqlite3
from sqlite3 import OperationalError

app = Flask(__name__)

conn = sqlite3.connect('sam.db')
c = conn.cursor()

def executeScriptsFromFile(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            c.execute(command)
        except OperationalError as msg:
            print("Command skipped: ", msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    templateData = {
        'title' : 'Hello world', #wszystkie rzeczy przekazywane do html
        'przyklad' : 'Testowy tekst',
    }
    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            print("Buton1")
        elif  request.form.get('action2') == 'VALUE2':
            print("Buton2")
        else:
            pass # unknown
    return render_template('site.html', **templateData)


if __name__ == '__main__':
    executeScriptsFromFile("kod_do_bazy_danych.sql")
    app.run(debug=True, port=8080, host='0.0.0.0')