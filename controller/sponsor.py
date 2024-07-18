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

class RegisterSponsor(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    username = StringField('Username', validators=[validators.input_required()])
    password = PasswordField('Password')
    repeat_password = PasswordField('Repeat Password')
    industry = StringField('Industry', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    submit = SubmitField('Submit')
        
@app.route("/register/sponsor", methods = ["GET", "POST"])
def register_sponsor():
    if request.method == "GET":
        sponsor_form = RegisterSponsor()
        return render_template("form.html",title="Sponsor Registration", form = sponsor_form, login=False)
    elif request.method == "POST":
        pass
    else:
        pass
        
