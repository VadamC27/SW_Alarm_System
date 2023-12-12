
#!/usr/bin/env python

from flask import flask

app = Flask(__name__)

@app.route('/')
def index():

    templateData = {
        'title' : 'Hello world' #wszystkie rzeczy przekazywane do html
        'przyklad' : 'Testowy tekst'
    }
    return render_template('site.html', **templateData)
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')