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


@app.route("/influencer/register", methods = ["GET", "POST"])
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
                session["username"] = influencer.username
                session["type"] = "Influencer"
                return redirect(url_for("influencer_dashboard"))
            return render_template("error.html", error_code=404, error_message="Page Not Found")
        return render_template("error.html", error_code=404, error_message="Page Not Found")
    else:
        return render_template("error.html", error_code=404, error_message="Page Not Found")

@app.route("/influencer/dashboard")
def influencer_dashboard():
    if "type" in session.keys() and session["type"] == "Influencer":
        return render_template("influencer_dashboard.html")
    else:
        return redirect(url_for("login"))

@app.route("/influencer/find")
def influencer_find():
    if "type" in session.keys() and session["type"] == "Influencer":
        pass
    else:
        return redirect(url_for("login"))

@app.route("/influencer/stats")
def influencer_stats():
    if "type" in session.keys() and session["type"] == "Influencer":
        pass
    else:
        return redirect(url_for("login"))
