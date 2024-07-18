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
from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    validators, 
    PasswordField, 
    SubmitField, 
    RadioField, 
    IntegerField,
    DecimalField    
)
class Login(FlaskForm):
    username = StringField('Username', validators=[validators.input_required()])
    password = PasswordField('Password')
    admin = RadioField(choices=['Admin', 'User'], validators=[validators.input_required()])
    submit = SubmitField('Submit')
    

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        login = Login()
        return render_template("form.html",title="Login", form= login, login=True)
    elif request.method == "POST":
        return render_template("base.html")
    else:
        pass
