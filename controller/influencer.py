from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
    )
from flask import render_template
from model.db import db, Influencers, Campaigns, AdRequests
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
    influencer_form = RegisterInfluencer()
    if request.method == "GET":
        return render_template("form.html",title="Influencer Registration", form = influencer_form, login=False)
    elif request.method == "POST":
        if influencer_form.validate_on_submit():
            if influencer_form.password.data == influencer_form.repeat_password.data:
                influencer = Influencers()
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
        ad_requests_all = AdRequests.query.filter(AdRequests.influencer_id == session["id"])
        active_requests = ad_requests_all.filter(AdRequests.status == 2).all()
        new_requests = ad_requests_all.filter(AdRequests.status == 0).all()
        return render_template("influencer/dashboard.html", campaigns = active_requests, requests = new_requests)
    else:
        return redirect(url_for("login"))

@app.route("/influencer/find")
def influencer_find():
    if "type" in session.keys() and session["type"] == "Influencer":
        return render_template("influencer/find.html")
    else:
        return redirect(url_for("login"))

@app.route("/influencer/stats")
def influencer_stats():
    if "type" in session.keys() and session["type"] == "Influencer":
        return render_template("influencer/stats.html")
    else:
        return redirect(url_for("login"))

@app.route("/influencer/accept/<ad_request_id>")
def accept_request(ad_request_id):
    if "type" in session.keys() and session["type"] == "Influencer":
        ad_request = AdRequests.query.filter(AdRequests.id == ad_request_id).first()
        ad_request.status = 2
        db.session.commit()
        return redirect(url_for("influencer_dashboard"))
    else:
        return redirect(url_for("login"))

@app.route("/influencer/negotiate/<ad_request_id>/<amount>")
def negotiate_request(ad_request_id, amount):
    if "type" in session.keys() and session["type"] == "Influencer":
        ad_request = AdRequests.query.filter(AdRequests.id == ad_request_id).first()
        ad_request.status = 1
        ad_request.payment_amount = amount 
        db.session.commit()
        return redirect(url_for("influencer_dashboard"))
    else:
        return redirect(url_for("login"))

@app.route("/influencer/accept/<ad_request_id>")
def reject_request(ad_request_id):
    if "type" in session.keys() and session["type"] == "Influencer":
        ad_request = AdRequests.query.filter(AdRequests.id == ad_request_id).first()
        ad_request.status = 2
        db.session.commit()
        return redirect(url_for("influencer_dashboard"))
    else:
        return redirect(url_for("login"))
