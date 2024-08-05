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
    SelectField
)

from controller.base import assign_user
from sqlalchemy import and_, or_
from datetime import date

class NegotiateForm(FlaskForm):
    ad_request_id = IntegerField('', validators=[validators.input_required()])
    payment_amount = DecimalField('Payment Amount', validators=[validators.input_required()])
    submit = SubmitField('Update')

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
    industry = StringField('Industry', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    update = SubmitField('Update')

class AdRequestForm(FlaskForm):
    ad_request_id = IntegerField('')
    influencer_id = SelectField('Influencer', validators=[validators.input_required()])
    campaign_id = SelectField('Campaign', validators=[validators.input_required()])
    messages = StringField('Message', validators=[validators.input_required()])
    requirements = StringField('Requirements', validators=[validators.input_required()])
    payment_amount = DecimalField('Payment Amount', validators = [validators.input_required()])
    submit = SubmitField('Done!')

class SearchForm(FlaskForm):
    query_string = StringField('')
    date = DateField('Date')
    revenue = DecimalField('Revenue')
    niche = StringField('Niche')
    search = SubmitField()

class CampaignForm(FlaskForm):
    campaign_id = IntegerField('Campaign ID')
    name = StringField('Name', validators = [validators.input_required()])
    description = StringField('Description', validators = [validators.input_required()])
    start_date = DateField('Start Date', validators = [validators.input_required()])
    end_date = DateField('End Date', validators = [validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    visibility = BooleanField('Visible')
    goals = StringField('Goals', validators = [validators.input_required()])
    niche = StringField('Niche', validators = [validators.input_required()])
    add = SubmitField('Done!')

def get_id_name(object):
    return (object.id, object.name)
    

def get_monthly_data(ad_requests):
    months = [0 for i in range(12)]
    for ad_request in ad_requests:
        start_month = ad_request.campaign.start_date.month - 1 
        end_month = ad_request.campaign.end_date.month - 1
        print(ad_request.id, start_month, end_month, ad_request.payment_amount)
        while(True):
            months[start_month] += int(ad_request.payment_amount)
            if start_month == end_month:
                break
            start_month = ( start_month + 1 ) % 12
    return months
       
    
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
                sponsor.flag = False
                db.session.add(sponsor)
                db.session.commit()            
                session["type"] = "Sponsor"
                session["user"] = assign_user(sponsor)
                return redirect(url_for("sponsor_dashboard"))
            return render_template("error.html", error_code="", error_message="Passwords did not match")
        return render_template("error.html", error_code="", error_message="Could Not Validate Form")
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
        campaign_form = CampaignForm()
        ad_request_form = AdRequestForm()
        campaigns = Campaigns.query.filter(Campaigns.sponsor_id == session["user"]["id"])
        influencers = Influencers.query
        campaigns_choice = list(map(get_id_name, Campaigns.query.filter(and_(Campaigns.sponsor_id == session["user"]["id"], and_(Campaigns.end_date >= date.today(), Campaigns.start_date <= date.today())))))
        ad_request_form.campaign_id.choices = campaigns_choice
        ad_request_form.influencer_id.choices = list(map(get_id_name, influencers))
        ad_requests = []
        negotiate_form = NegotiateForm()
        for campaign in campaigns.all():
            ad_requests += campaign.ad_requests
        if request.method == "GET":
            return render_template("sponsor/dashboard.html", today = date.today() , campaigns = campaigns.all(), ad_requests = ad_requests, form=campaign_form, negotiate_form = negotiate_form, ad_request_form= ad_request_form)
        elif request.method == "POST":
            print(campaign_form.add)
            print(campaign_form.add.data)
            print(ad_request_form.submit)
            print(ad_request_form.submit.data)
            if campaign_form.add.data:
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
                campaign.flag = False
                if new :
                    db.session.add(campaign)
                db.session.commit()
                return redirect(url_for("sponsor_dashboard"))
            elif ad_request_form.submit.data:
                ad_request = AdRequests.query.filter(AdRequests.id == ad_request_form.ad_request_id.data).first()
                if ad_request:
                    ad_request_form.populate_obj(ad_request)
                    db.session.commit()
                    return redirect(url_for("sponsor_dashboard"))
                else:
                    return render_template("error.html", error_code=404, error_message="Ad Request Not Found")
            else:
                return redirect(url_for("sponsor_dashboard"))
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/find", methods = ["GET", "POST"])
def sponsor_find():
    if "type" in session.keys() and session["type"] == "Sponsor":
        search = SearchForm()
        ad_request_form = AdRequestForm()
        campaigns_choice = list(map(get_id_name, Campaigns.query.filter(and_(Campaigns.sponsor_id == session["user"]["id"], and_(Campaigns.end_date >= date.today(), Campaigns.start_date <= date.today())))))
        campaigns = Campaigns.query.filter(Campaigns.visibility == True)
        influencers = Influencers.query
        ad_request_form.campaign_id.choices = campaigns_choice
        ad_request_form.influencer_id.choices = list(map(get_id_name, influencers))
        if request.method == "GET":
            return render_template("sponsor/find.html",today = date.today(), form = search,ad_request_form = ad_request_form, search_items = influencers.all() + campaigns.all() )
        elif request.method == "POST":
            if search.search.data:
                if search.query_string.data:
                    influencers = influencers.filter(Influencers.name.contains(search.query_string.data))
                    campaigns = campaigns.filter(Campaigns.name.contains(search.query_string.data))
                if search.date.data:
                    campaigns = campaigns.filter(and_(Campaigns.start_date <= search.date.data, Campaigns.end_date >= search.date.data)) 
                if search.revenue.data:
                    campaigns = campaigns.filter(Campaigns.budget <= search.revenue.data)
                    influencers = influencers.filter(Influencers.budget <= search.revenue.data)                    
                if search.niche.data:
                    campaigns = campaigns.filter(or_(Campaigns.niche.contains(search.niche.data),Campaigns.niche == search.niche.data))
                    influencers = influencers.filter(or_(Influencers.niche.contains(search.niche.data), Influencers.niche == search.niche.data))
            elif ad_request_form.submit.data:
                ad_request = AdRequests()
                ad_request_form.populate_obj(ad_request)
                print(ad_request_form.influencer_id)
                print(ad_request_form.influencer_id.data)
                ad_request.influencer_id = ad_request_form.influencer_id.data
                ad_request.status = 0
                db.session.add(ad_request)
                db.session.commit()
            return render_template("sponsor/find.html",today = date.today(), form = search, ad_request_form = ad_request_form, search_items = influencers.all() + campaigns.all() )
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/stats")
def sponsor_stats():
    if "type" in session.keys() and session["type"] == "Sponsor":
        ad_requests = AdRequests.query.filter(AdRequests.campaign.has(Campaigns.sponsor_id == session["user"]["id"]))
        new = ad_requests.filter(or_(AdRequests.status == 0 , AdRequests.status == 1)).count()
        accepted= ad_requests.filter(AdRequests.status == 2)
        ongoing = accepted.filter(and_(AdRequests.campaign.has(Campaigns.start_date <= date.today()), AdRequests.campaign.has(Campaigns.end_date >=  date.today()))).count()
        completed = accepted.filter(AdRequests.campaign.has(Campaigns.end_date <  date.today())).count()
        rejected = ad_requests.filter(AdRequests.status == 3).count()
        monthly_data = get_monthly_data(accepted)
        print(new, completed, ongoing, rejected, monthly_data)
        return render_template("sponsor/stats.html", ad_request_data = [new, ongoing , completed , rejected], monthly_data = monthly_data)
    else:
        return redirect(url_for("login")) 

