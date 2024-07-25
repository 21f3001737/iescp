from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
        render_template
    )
from model.db import db, Sponsors, Campaigns, AdRequests, Influencers
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

class NewCampaignForm(FlaskForm):
    campaign_id = IntegerField('Campaign ID')
    name = StringField('Name', validators = [validators.input_required()])
    description = StringField('Description', validators = [validators.input_required()])
    start_date = DateField('Start Date', validators = [validators.input_required()])
    end_date = DateField('End Date', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    visibility = BooleanField('Visible')
    goals = StringField('Goals', validators = [validators.input_required()])
    submit = SubmitField('Done!')


@app.route("/sponsor/campaigns", methods = ["GET", "POST"])
def sponsor_campaigns():
    if "type" in session.keys() and session["type"] == "Sponsor":
        campaign_form = NewCampaignForm()
        if request.method == "GET":
            campaigns = Campaigns.query.filter(Campaigns.sponsor_id == session["user"]["id"]).all()
            return render_template("sponsor/campaigns.html", form = campaign_form, campaigns = campaigns)
        elif request.method == "POST":
            if campaign_form.validate_on_submit():
                campaign = Campaigns()
                campaign_form.populate_obj(campaign)
                campaign.sponsor_id = session["user"]["id"]
                db.session.add(campaign)
                db.session.commit()
                return redirect(url_for("sponsor_campaigns"))
            else:
                return render_template("sponsor/campaigns.html", form = campaign_form)
    else:
        return redirect(url_for("login"))
    
@app.route("/sponsor/campaign/delete/<campaign_id>")
def sponsor_delete_campaign(campaign_id):
    campaign = Campaigns.query.filter(Campaigns.id == campaign_id).first()
    if "type" in session.keys() and session["type"] == "Sponsor" and campaign and campaign.sponsor_id == session["user"]["id"]:
        db.session.delete(campaign)
        db.session.commit()
        return redirect(url_for("sponsor_campaigns"))
    else:
        return redirect(url_for("login"))
    
@app.route("/sponsor/campaign/edit/<campaign_id>")
def sponsor_edit_campaign(campaign_id):
    campaign = Campaigns.query.filter(Campaigns.id == campaign_id).first()
    if "type" in session.keys() and session["type"] == "Sponsor" and campaign and campaign.sponsor_id == session["user"]["id"]:
        pass
    else:
        return redirect(url_for("login"))
    
