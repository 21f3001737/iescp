from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
    )
from flask import render_template
from model.db import db, Sponsors, Campaigns
from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    validators, 
    PasswordField, 
    SubmitField, 
    RadioField, 
    IntegerField,
    DecimalField,
    DateField,
    BooleanField,
)

class RegisterSponsor(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    username = StringField('Username', validators=[validators.input_required()])
    password = PasswordField('Password')
    repeat_password = PasswordField('Repeat Password')
    industry = StringField('Industry', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    submit = SubmitField('Submit')

class NewCampaignForm(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    description = StringField('Description', validators = [validators.input_required()])
    start_date = DateField('Start Date', validators = [validators.input_required()])
    end_date = DateField('End Date', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    visibility = BooleanField('Visible')
    goals = StringField('Goals', validators = [validators.input_required()])
    submit = SubmitField('Done!')
    
@app.route("/sponsor/register", methods = ["GET", "POST"])
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
        return render_template("sponsor/dashboard.html")
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/find")
def sponsor_find():
    if "type" in session.keys() and session["type"] == "Sponsor":
        return render_template("sponsor/find.html")
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/stats")
def sponsor_stats():
    if "type" in session.keys() and session["type"] == "Sponsor":
        return render_template("sponsor/stats.html")
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/campaigns", methods = ["GET", "POST"])
def sponsor_campaigns():
    if "type" in session.keys() and session["type"] == "Sponsor":
        campaign_form = NewCampaignForm()
        if request.method == "GET":
            campaigns = Campaigns.query.filter(Campaigns.sponsor_id == session["id"]).all()
            return render_template("sponsor/campaigns.html", form = campaign_form, campaigns = campaigns)
        elif request.method == "POST":
            if campaign_form.validate_on_submit():
                campaign = Campaigns()
                campaign_form.populate_obj(campaign)
                campaign.sponsor_id = session["id"]
                db.session.add(campaign)
                db.session.commit()
                return redirect(url_for("sponsor_campaigns"))
            else:
                return render_template("sponsor/campaigns.html", form = campaign_form)
    else:
        return redirect(url_for("login"))
    
