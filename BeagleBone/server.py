#!/usr/bin/env python

from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3
from sqlite3 import OperationalError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

def send_email(subject, body, to_email):
    # Konfiguracja parametrów serwera SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'marianowicka1236@gmail.com'
    smtp_password = 'erki xrqj rmpl tbbo'

    # Adres e-mail nadawcy
    from_email = 'marianowicka1236@gmail.com'

    # Tworzenie obiektu MIME do przechowywania wiadomości
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Dodawanie treści wiadomości
    msg.attach(MIMEText(body, 'plain'))

    # Inicjalizacja połączenia SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Logowanie do konta e-mail
    server.login(smtp_username, smtp_password)

    # Wysyłanie wiadomości
    server.sendmail(from_email, to_email, msg.as_string())

    # Zamykanie połączenia
    server.quit()

def get_mail():
    subject = 'Testowa wiadomość'
    body = 'Cześć, to jest treść testowej wiadomości.'
    to_email = 'mysiol007@gmail.com'

    send_email(subject, body, to_email)

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

def validate_login(username, password):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM uzytkownicy WHERE login=?", (username,))
        user_data = cursor.fetchone()

        if user_data is not None:
            if user_data['haslo'] == password:
                return 'success'
            else:
                return 'incorrect_password'
        else:
            return 'incorrect_username'
    except Exception as e:
        print("Error during login validation:", e)
        return 'error'

@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        if request.form.get('action2') == 'Zaloguj':
            username = request.form.get('username')
            password = request.form.get('password')

            # Validate login and password against the database
            login_result = validate_login(username, password)

            if login_result == 'success':
                # Successful login
                return redirect(url_for('index'))
            else:
                # Failed login
                if login_result == 'incorrect_username':
                    error_message = 'Błędna nazwa użytkownika.'
                elif login_result == 'incorrect_password':
                    error_message = 'Błędny kod.'

    template_data = {
        'title': 'System alarmowy',
        'example': 'Testowy tekst',
        'error_message': error_message,
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
    error_message = None

    if request.method == 'POST':
        old_password = request.form.get('oldPassword')
        new_password = request.form.get('newPassword')

        current_user_login = 'example_user'

        try:
            # Check if the form is submitted with non-empty values
            if old_password.strip() and new_password.strip():
                # Check if the old password matches the one in the database for the current user
                db = get_db()
                cursor = db.cursor()
                cursor.execute("SELECT kod FROM kody WHERE login=? AND kod=?", (current_user_login, old_password))
                result = cursor.fetchone()

                if result:
                    # Update the database with the new password
                    cursor.execute("UPDATE kody SET kod=? WHERE login=?", (new_password, current_user_login))
                    db.commit()
                else:
                    error_message = "Niepoprawny stary kod."
            else:
                error_message = "Musisz wpisac stary i nowy kod."

        except Exception as e:
            error_message = ""

    template_data = {
        'title': 'Zmiana kodu',
        'example': 'Przykładowy tekst dla zmiany kodu',
        'error_message': error_message,
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
    with app.app_context():
        execute_scripts_from_file("kod_do_bazy_danych.sql")
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO czujniki(id_czujnika, nazwa) values(?,?)",(2,"czujnik_1"))
        c.execute("INSERT INTO czujniki(id_czujnika, nazwa) values(?,?)",(3,"czujnik_2"))
        c.execute("INSERT INTO uzytkownicy(login,haslo) values(?,?)",("admin","admin"))
        c.execute("INSERT INTO kody(login, kod) values(?,?)",("example_user","1234"))
        db.commit()

    app.teardown_appcontext(close_db)
    app.run(debug=True, port=8080, host='0.0.0.0')
