from flask import Flask, render_template
from dynaconf import FlaskDynaconf
import socket


app = Flask(__name__)

FlaskDynaconf(app, settings_files=["settings.toml"], root_path="conf/")

settings = app.config

@app.route('/')
def hello():
    data = {
        'hostname': socket.gethostname(),
        'ver': settings.get("ver", ""),
        'greet': settings.get("greet", ""),
        'hide': settings.get("hide", "")
    }
    return render_template('hello.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')