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

@app.route("/sponsor/register", methods = ["GET", "POST"])
def register_sponsor():
    if request.method == "GET":
        sponsor_form = RegisterSponsor()
        return render_template("form.html",title="Sponsor Registration", form = sponsor_form, login=False)
    elif request.method == "POST":
        if sponsor_form.validate_on_submit():
            if sponsor_form.password.data == sponsor_form.repeat_password.data:
                sponsor = sponsors()
                sponsor_form.populate_obj(sponsor)
                db.session.add(sponsor)
                db.session.commit()            
                session["username"] = sponsor.username
                session["type"] = "Sponsor"
                return redirect(url_for("sponsor_dashboard"))
            return render_template("error.html", error_code=404, error_message="Page Not Found")
        return render_template("error.html", error_code=404, error_message="Page Not Found")
    else:
        return render_template("error.html", error_code=404, error_message="Page Not Found")

@app.route("/sponsor/dashboard")
def sponsor_dashboard():
    if "type" in session.keys() and session["type"] == "Sponsor":
        return render_template("sponsor_dashboard.html")
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/find")
def sponsor_find():
    if "type" in session.keys() and session["type"] == "Sponsor":
        pass
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/stats")
def sponsor_stats():
    if "type" in session.keys() and session["type"] == "Sponsor":
        pass
    else:
        return redirect(url_for("login"))
