from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
    )
from flask import render_template
from model.db import db, Sponsors
from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    validators, 
    PasswordField, 
    SubmitField, 
    RadioField, 
    IntegerField,
)
class Login(FlaskForm):
    username = StringField('Username', validators=[validators.input_required()])
    password = PasswordField('Password')
    type = RadioField(choices=['Admin', 'Sponsor', 'Influencer'], validators=[validators.input_required()])
    submit = SubmitField('Submit')
    
def isValidUser(form):
    if form.type.data == "Sponsor":
        sponsor = Sponsors.query.filter(Sponsors.username == form.username.data).first()
        if sponsor:
            return True
        else:
            return False
    elif form.type.data == "Influencer":
        pass
    else:
        pass

@app.route("/")
def home():
    return render_template("base.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    login = Login()
    if request.method == "GET":
        return render_template("form.html",title="Login", form= login, login=True)
    elif request.method == "POST":
        if login.validate_on_submit():
            if isValidUser(login):
                session["type"] = login.type.data    
                session["username"] = login.username.data
            else:
                return render_template("error.html", error_code=404, error_message="User Not Found")
        else:
            return render_template("form.html", title="Login", form=login, login = True)
        return render_template("base.html")
    else:
        return render_template("error.html", error_code=404, error_message="Page Not Found")

@app.route("/logout")
def logout():
    if "type" in session.keys():
        session.pop("type")
    if "username" in session.keys():
        session.pop("username")
    return redirect(url_for("login"))
