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

class RegisterInfluencer(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    username = StringField('Username', validators=[validators.input_required()])
    password = PasswordField('Password')
    repeat_password = PasswordField('Repeat Password')
    category = StringField('Category', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    submit = SubmitField('Submit')


@app.route("/register/influencer", methods = ["GET", "POST"])
def register_influencer():
    if request.method == "GET":
        influencer_form = RegisterInfluencer()
        return render_template("form.html",title="Influencer Registration", form = influencer_form, login=False)
    elif request.method == "POST":
        pass
    else:
        pass
