
#!/usr/bin/env python

from flask import Flask
import sqlite3

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
        except OperationalError, msg:
            print("Command skipped: ", msg)

@app.route('/')
def index():
    templateData = {
        'title' : 'Hello world', #wszystkie rzeczy przekazywane do html
        'przyklad' : 'Testowy tekst',
    }

    return render_template('site.html', **templateData)


if __name__ == '__main__':
    executeScriptsFromFile("kod_do_bazy_danych.sql")
    app.run(debug=True, port=8080, host='0.0.0.0')