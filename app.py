from flask import Flask, render_template
from dynaconf import FlaskDynaconf
import sys
import socket


app = Flask(__name__)

FlaskDynaconf(app, settings_files=["settings.toml"])

settings = app.config

@app.route('/')
def hello():
    data = {
        'hostname': socket.gethostname(),
        'ver': settings.get("ver", "4.0"),
        'greet': settings.get("greet", "Olá"),
        'secret': settings.get("secret", ""),
        'primary_color': settings.get("primary_color", "red"),
        'secondary_color': settings.get("secondary_color", "orange"),
        'arg': sys.argv[1]
    }
    return render_template('hello.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')