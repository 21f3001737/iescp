from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
    )
from flask import render_template
from model.db import db, Influencers
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
        if influencer_form.validate_on_submit():
            if influencer_form.password.data == influencer_form.repeat_password.data:
                influencer = influencers()
                influencer_form.populate_obj(influencer)
                db.session.add(influencer)
                db.session.commit()            
                return "Success"
            return "Passwords dont match"
        return "Validation Failed"
    else:
        return "Error Page"
