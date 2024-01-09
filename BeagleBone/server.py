#!/usr/bin/env python

from flask import Flask, render_template, request
import sqlite3
from sqlite3 import OperationalError

app = Flask(__name__)

conn = sqlite3.connect('sam.db')
c = conn.cursor()

login = 'example_user'

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

    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            print("Buton1")
        elif  request.form.get('action2') == 'VALUE2':
            print("Buton2")
        elif  request.form.get('action3') == 'VALUE3':
            print("Buton3")

    templateData = {
        'title' : 'System alarmowy', #wszystkie rzeczy przekazywane do html
        'przyklad' : 'Testowy tekst',
    }
    return render_template('site.html', **templateData)

@app.route('/login', methods=['GET', 'POST'])
def login():
    templateData = {
        'title': 'Logowanie',
        'example': 'Przykładowy tekst dla logowania',
    }
    return render_template('login.html', **templateData)

@app.route('/entries', methods=['GET', 'POST'])
def entries():
    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            print("Buton1")
        elif  request.form.get('action2') == 'VALUE2':
            print("Buton2")
        elif  request.form.get('action3') == 'VALUE3':
            print("Buton3")

    templateData = {
        'title' : 'Zarejestrowane przejścia', #wszystkie rzeczy przekazywane do html
        'test' : 'Testowy tekst',
    }
    return render_template('entries.html', **templateData)

@app.route('/options', methods=['GET', 'POST'])
def options():
    templateData = {
        'title': 'Ustawienia',
        'example': 'Przykładowy tekst dla ustawień',
    }
    return render_template('options.html', **templateData)

@app.route('/change_code', methods=['GET', 'POST'])
def change_code():
    error_message = None

    if request.method == 'POST':
        old_password = request.form.get('oldPassword')
        new_password = request.form.get('newPassword')

        current_user_login = 'example_user'

        try:
            # Check if the old password matches the one in the database for the current user
            c.execute("SELECT kod FROM kody WHERE login=? AND kod=?", (current_user_login, old_password))
            result = c.fetchone()

            if result:
                # Update the database with the new password
                c.execute("UPDATE kody SET kod=? WHERE login=?", (new_password, current_user_login))
                c.commit()               
            else:
                error_message = "Incorrect old password. Password update failed."
        except Exception as e:
            error_message = "An error occurred while updating the password."

    template_data = {
        'title': 'Zmiana kodu',
        'example': 'Przykładowy tekst dla zmiany kodu',
        'error_message': error_message,
    }
    return render_template('password.html', **template_data)

@app.route('/notification_settings', methods=['GET', 'POST'])
def notification_settings():
    templateData = {
        'title': 'Zmiana kodu',
        'example': 'Przykładowy tekst dla zmiany kodu',
    }
    return render_template('notifications.html', **templateData)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    templateData = {
        'title': 'Zmiana kodu',
        'example': 'Przykładowy tekst dla zmiany kodu',
    }
    return render_template('adduser.html', **templateData)

if __name__ == '__main__':
    executeScriptsFromFile("kod_do_bazy_danych.sql")
    c.execute("INSERT INTO czujniki(id_czujnika, nazwa) values(?,?)",(2,"czujnik_1"))
    c.execute("INSERT INTO czujniki(id_czujnika, nazwa) values(?,?)",(3,"czujnik_2"))
    c.execute("INSERT INTO uzytkownicy(login,haslo) values(?,?)",("admin","admin"))
    c.execute("INSERT INTO kody(login, kod) values(?,?)",("example_user","1234"))
    conn.commit()
    app.run(debug=True, port=8080, host='0.0.0.0')

