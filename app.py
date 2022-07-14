from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from dynaconf import FlaskDynaconf
import sys
import os
import socket


app = Flask(__name__)

FlaskDynaconf(
    app,
    settings_files=[
        "settings.toml",
        ".secrets.toml",
        "/config/settings.toml",
        "/config/.secrets.toml",
    ],
    envvar_prefix="hello",
)

settings = app.config

app.secret_key = "secret key"
settings["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, "uploads")

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

settings["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def hello():
    data = {
        "hostname": socket.gethostname(),
        "ver": settings.get("ver", "4.0"),
        "greet": settings.get("greet", "Olá"),
        "secret": settings.get("secret", ""),
        "primary_color": settings.get("primary_color", "red"),
        "secondary_color": settings.get("secondary_color", "orange"),
        "arg": sys.argv[1] if len(sys.argv) > 1 else "",
    }
    return render_template("hello.html", data=data)


@app.route("/upload")
def upload_form():
    return render_template("upload.html")


@app.route("/uploader", methods=["POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Sem a parte do arquivo")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("Nenhum arquivo selecionado para o upload!")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("Arquivo enviado com sucesso")
            return redirect("/upload")
        else:
            flash("As extensões permitidas são: txt, pdf, png, jpg, jpeg, gif")
            return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
