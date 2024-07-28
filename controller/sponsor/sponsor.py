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
from sqlalchemy import or_
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

from controller.base import assign_user

class RegisterSponsor(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    username = StringField('Username', validators=[validators.input_required(), validators.Regexp(r'^[\w.@+-_]+$'), validators.Length(min=6, max=20)])
    password = PasswordField('Password', validators=[validators.input_required(), validators.Length(min=6)])
    repeat_password = PasswordField('Repeat Password', validators=[validators.input_required(), validators.EqualTo('password', message='Passwords do not match')])
    industry = StringField('Industry', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    submit = SubmitField('Submit')

class UpdateSponsor(FlaskForm):
    name = StringField('Name', validators=[validators.input_required()])
    username = StringField('Username', validators=[validators.input_required()])
    category = StringField('Category', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    update = SubmitField('Update')

class NewAdRequestForm(FlaskForm):
    influencer_id = IntegerField('Influencer ID',  render_kw={'disabled':''})
    messages = StringField('Message')
    requirements = StringField('Requirements')
    payment_amount = DecimalField('Payment Amount', validators = [validators.input_required()])
    submit = SubmitField('Done!')

class SearchForm(FlaskForm):
    query_string = StringField('')
    date = DateField('Date')
    revenue = DecimalField('Revenue')
    search = SubmitField()

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

    
    
@app.route("/sponsor/register", methods = ["GET", "POST"])
def sponsor_register():
    sponsor_form = RegisterSponsor()
    if request.method == "GET":
        return render_template("auth/register.html",title="Sponsor Registration", form = sponsor_form, influencer=False)
    elif request.method == "POST":
        if sponsor_form.validate_on_submit():
            if sponsor_form.password.data == sponsor_form.repeat_password.data:
                sponsor = Sponsors()
                sponsor_form.populate_obj(sponsor)
                db.session.add(sponsor)
                db.session.commit()            
                session["type"] = "Sponsor"
                session["user"] = assign_user(sponsor)
                return redirect(url_for("sponsor_dashboard"))
            return render_template("error.html", error_code=404, error_message="Page Not Found")
        return render_template("error.html", error_code=404, error_message="Page Not Found")
    else:
        return render_template("error.html", error_code=404, error_message="Page Not Found")

@app.route("/sponsor/profile/<sponsor_id>", methods=["GET", "POST"])
def sponsor_profile(sponsor_id):
    sponsor =  Sponsors.query.filter(Sponsors.id == sponsor_id).first()
    update_form = UpdateSponsor(obj=sponsor)
    disabled = True
    if "type" in session.keys() and session["type"] == "Sponsor" and session["user"]["id"] == sponsor.id:
        disabled = False
    if sponsor:
        if request.method == "GET":
            return render_template("sponsor/profile.html", sponsor=sponsor, update_form=update_form, disabled = disabled)
        elif request.method == "POST":
            update_form.populate_obj(sponsor)
            db.session.commit()
            return render_template("sponsor/profile.html", sponsor=sponsor, update_form=update_form, disabled = disabled)
    else:
        return render_template("error.html", error_code=404, error_message="Sponsor Not Found")   

@app.route("/sponsor/dashboard", methods=["GET", "POST"])
def sponsor_dashboard():
    if "type" in session.keys() and session["type"] == "Sponsor":
        campaign_form = NewCampaignForm()
        campaigns = Campaigns.query.filter(Campaigns.sponsor_id == session["user"]["id"]).all()
        ad_requests = []
        for campaign in campaigns:
            ad_requests += campaign.ad_requests
        if request.method == "GET":
            return render_template("sponsor/dashboard.html", campaigns = campaigns, ad_requests = ad_requests, form=campaign_form)
        elif request.method == "POST":
            if campaign_form.validate_on_submit():
                new = True 
                campaign = None
                if campaign_form.campaign_id.data:
                    campaign = Campaigns.query.filter(Campaigns.id == campaign_form.campaign_id.data).first()
                    if campaign:
                        new = False
                    else:
                        campaign = Campaigns()
                else:
                    campaign = Campaigns()
                campaign_form.populate_obj(campaign)
                campaign.sponsor_id = session["user"]["id"]
                if new :
                    db.session.add(campaign)
                db.session.commit()
                return redirect(url_for("sponsor_dashboard"))
            else:
                return render_template("sponsor/dashboard.html",campaigns = campaigns, ad_requests = ad_requests, form = campaign_form)     
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/find", methods = ["GET", "POST"])
def sponsor_find():
    if "type" in session.keys() and session["type"] == "Sponsor":
        search = SearchForm()
        ad_request_form = NewAdRequestForm()
        campaigns = Campaigns.query.filter(Campaigns.visibility == True)
        influencers = Influencers.query.filter()
        if request.method == "GET":
            return render_template("sponsor/find.html", form = search,ad_request_form = ad_request_form, search_items = influencers.all() + campaigns.all() )
        elif request.method == "POST":
            if search.search.data:
                campaigns = Campaigns.query.filter(or_(Campaigns.visibility == True, Campaigns.id == session["user"]["id"]))
                influencers = Influencers.query
                if search.query_string.data:
                    influencers = influencers.filter(Influencers.name.contains(search.query_string.data))
                    campaigns = campaigns.filter(Campaigns.name.contains(search.query_string.data))
                if search.date.data:
                    campaigns = campaigns.filter(Campaigns.start_date <= search.date.data).filter(Campaigns.end_date >= search.date.data) 
                if search.revenue.data:
                    campaigns = campaigns.filter(Campaigns.budget <= search.revenue.data)
                    influencers = influencers.filter(Influencers.budget <= search.revenue.data)                    
            elif ad_request_form.submit_data:
                ad_request = AdRequests()
                ad_request_form.populate_obj(ad_request)
                ad_request.campaign_id == session["user"]["id"]
                ad_request.status = 0
                db.session.add(ad_request)
                db.session.commit()
            return render_template("sponsor/find.html", form = search, ad_request_form = ad_request_form, search_items = influencers.all() + campaigns.all() )
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/stats")
def sponsor_stats():
    if "type" in session.keys() and session["type"] == "Sponsor":
        return render_template("sponsor/stats.html")
    else:
        return redirect(url_for("login"))

