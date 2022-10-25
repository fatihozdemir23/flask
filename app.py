import os
import cv2
import werkzeug.utils
from werkzeug.serving import WSGIRequestHandler

from flask import Flask, request, jsonify, send_from_directory

from Face_Site import Predict, ToplamYuzSayisi

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

WSGIRequestHandler.protocol_version = "HTTP/1.1"


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("image"))
    for upload in request.files.getlist("image"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
    execution_path = target
    print(execution_path)
    image = Predict(os.path.join(execution_path, filename))
    facecount=ToplamYuzSayisi(os.path.join(execution_path, filename))

    out_image = cv2.imwrite(os.path.join(execution_path, "flask" + filename), image)

    return jsonify({
        "facecount": facecount,
        "path":"flaskdosya.jpg",
    })


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/')
def home():
    return "merharerbadsd"


if __name__=="__main__":
    app.run(debug=True)