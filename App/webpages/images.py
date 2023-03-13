from flask import render_template, send_file
from App.main import app

@app.route("/images/<image>")
def images(image):
    print(image)
    return send_file('static/images/' + image, mimetype='image/webp')