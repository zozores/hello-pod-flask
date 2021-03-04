from flask import Flask, render_template
import socket
app = Flask(__name__)


@app.route('/')
def hello():
    data = {
        'hostname': socket.gethostname(),
        'version': '1.0'
    }
    return render_template('hello.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')