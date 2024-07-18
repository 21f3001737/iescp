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
    
class RegisterInfluencer(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    username = StringField('Username', validators=[validators.input_required()])
    password = PasswordField('Password')
    repeat_password = PasswordField('Repeat Password')
    category = StringField('Category', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    submit = SubmitField('Submit')

class RegisterSponsor(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    username = StringField('Username', validators=[validators.input_required()])
    password = PasswordField('Password')
    repeat_password = PasswordField('Repeat Password')
    industry = StringField('Industry', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    submit = SubmitField('Submit')
        
    

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        login = Login()
        return render_template("login.html",title="Login", form= login, login=True)
    elif request.method == "POST":
        return render_template("base.html")
    else:
        pass

@app.route("/register/influencer", methods = ["GET", "POST"])
def register_influencer():
    if request.method == "GET":
        influencer_form = RegisterInfluencer()
        return render_template("login.html",title="Influencer Registration", form = influencer_form, login=False)
    elif request.method == "POST":
        pass
    else:
        pass

@app.route("/register/sponsor", methods = ["GET", "POST"])
def register_sponsor():
    if request.method == "GET":
        sponsor_form = RegisterSponsor()
        return render_template("login.html",title="Sponsor Registration", form = sponsor_form, login=False)
    elif request.method == "POST":
        pass
    else:
        pass
        
