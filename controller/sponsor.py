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
    sponsor_form = RegisterSponsor()
    if request.method == "GET":
        return render_template("form.html",title="Sponsor Registration", form = sponsor_form, login=False)
    elif request.method == "POST":
        if sponsor_form.validate_on_submit():
            if sponsor_form.password.data == sponsor_form.repeat_password.data:
                sponsor = Sponsors()
                sponsor_form.populate_obj(sponsor)
                db.session.add(sponsor)
                db.session.commit()            
                return "Success"
            return "Passwords dont match"
        return "Validation Failed"
    else:
        return "Error Page"
        
