from flask import render_template, send_file
from App.main import app

@app.route("/images/<image>")
def gameroom_js(image):
    return send_file('App/static/images' + image, attachment_filename=image)