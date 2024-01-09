#!/usr/bin/env python

from flask import Flask, render_template, request, g
import sqlite3
from sqlite3 import OperationalError

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('sam.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(error):
    if 'db' in g:
        g.db.close()

def execute_scripts_from_file(filename):
    with app.app_context():
        try:
            db = get_db()
            cursor = db.cursor()
            fd = open(filename, 'r')
            sql_file = fd.read()
            fd.close()

            sql_commands = sql_file.split(';')

            for command in sql_commands:
                try:
                    cursor.execute(command)
                except OperationalError as msg:
                    print("Command skipped:", msg)

            db.commit()
        except Exception as e:
            print("Error executing scripts:", e)

@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            print("Button 1")
        elif request.form.get('action2') == 'VALUE2':
            print("Button 2")
        elif request.form.get('action3') == 'VALUE3':
            print("Button 3")

    template_data = {
        'title': 'System alarmowy',
        'example': 'Testowy tekst',
    }
    return render_template('site.html', **template_data)

@app.route('/', methods=['GET', 'POST'])
def login():
    template_data = {
        'title': 'Logowanie',
        'example': 'Przykładowy tekst dla logowania',
    }
    return render_template('login.html', **template_data)

@app.route('/entries', methods=['GET', 'POST'])
def entries():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM zarejestrowan_ruch')
        rows = cursor.fetchall()

    return render_template('entries.html', rows_from_database=rows)

@app.route('/options', methods=['GET', 'POST'])
def options():
    template_data = {
        'title': 'Ustawienia',
        'example': 'Przykładowy tekst dla ustawień',
    }
    return render_template('options.html', **template_data)

@app.route('/change_code', methods=['GET', 'POST'])
def change_code():
    template_data = {
        'title': 'Zmiana kodu',
        'example': 'Przykładowy tekst dla zmiany kodu',
    }
    return render_template('password.html', **template_data)

@app.route('/notification_settings', methods=['GET', 'POST'])
def notification_settings():
    template_data = {
        'title': 'Zmiana kodu',
        'example': 'Przykładowy tekst dla zmiany kodu',
    }
    return render_template('notifications.html', **template_data)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    template_data = {
        'title': 'Zmiana kodu',
        'example': 'Przykładowy tekst dla zmiany kodu',
    }
    return render_template('adduser.html', **template_data)

if __name__ == '__main__':
    execute_scripts_from_file("kod_do_bazy_danych.sql")
    app.teardown_appcontext(close_db)
    app.run(debug=True, port=8080, host='0.0.0.0')
