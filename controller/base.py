from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
    )
from flask import render_template
from model.db import db, Sponsors, Influencers
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
            return sponsor
        else:
            return None
    elif form.type.data == "Influencer":
        influencer = Influencers.query.filter(Influencers.username == form.username.data).first()
        if influencer:
            return influencer
        else:
            return None
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
            user = isValidUser(login)
            if user:
                session["type"] = login.type.data    
                session["username"] = user.username
                session["id"] = user.id
                return redirect(url_for("dashboard"))
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
    if "id" in session.keys():
        session.pop("id")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "type" in session.keys():
        if session["type"] == "Influencer":
            return redirect(url_for("influencer_dashboard"))
        elif session["type"] == "Sponsor":
            return redirect(url_for("sponsor_dashboard"))
        else:
            return redirect(url_for("login"))
