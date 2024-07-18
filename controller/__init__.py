from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
    )
from flask import render_template
from model.db import db

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("base.html")
    elif request.method == "POST":
        return render_template("base.html")
    else:
        pass
        
