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
    DecimalField,
    DateField,
    SelectField
)
from sqlalchemy import and_, or_
from datetime import date
from controller.base import assign_user

class RegisterInfluencer(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    username = StringField('Username', validators=[validators.input_required(), validators.Regexp(r'^[\w.@+-_]+$'), validators.Length(min=4,max=20)])
    password = PasswordField('Password', validators = [validators.input_required(), validators.Length(min=6)])
    repeat_password = PasswordField('Repeat Password', validators = [validators.input_required(), validators.EqualTo('password', message='Passwords do not match')])
    category = StringField('Category', validators = [validators.input_required()])
    niche = StringField('Niche', validators=[validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    followers = IntegerField('Followers', validators=[validators.input_required()])
    submit = SubmitField('Submit')

class UpdateInfluencer(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    username = StringField('Username', validators=[validators.input_required()])
    category = StringField('Category', validators = [validators.input_required()])
    niche = StringField('Niche', validators=[validators.input_required()])
    budget = DecimalField('Budget', validators = [validators.input_required()])
    followers = IntegerField('Followers', validators=[validators.input_required()])
    update = SubmitField('Update')
    

class SearchForm(FlaskForm):
    query_string = StringField('')
    date = DateField('Date')
    revenue = DecimalField('Max Revenue')
    search  = SubmitField()


class NewAdRequestForm(FlaskForm):
    campaign_id = IntegerField('Campaign ID', validators=[validators.input_required()])
    messages = StringField('Message', validators = [validators.input_required()])
    requirements = StringField('Requirements', validators=[validators.input_required()])
    payment_amount = DecimalField('Payment Amount', validators = [validators.input_required()])
    submit = SubmitField('Done!')

class NegotiateForm(FlaskForm):
    ad_request_id = IntegerField('', validators=[validators.input_required()])
    payment_amount = DecimalField('Payment Amount', validators=[validators.input_required()])
    submit = SubmitField('Update')

def double_niche(niche):
    return niche[0]

def get_monthly_data(ad_requests):
    months = [0 for i in range(12)]
    for ad_request in ad_requests:
        start_month = ad_request.campaign.start_date.month - 1
        end_month = ad_request.campaign.end_date.month - 1
        while(start_month != end_month):
            months[start_month] += int(ad_request.payment_amount)
            start_month = (start_month + 1) % 12
    return months
        

@app.route("/influencer/profile/<influencer_id>", methods=["GET", "POST"])
def influencer_profile(influencer_id):
    niches = list(map(double_niche, db.session.query(Influencers.niche).distinct().all()))
    influencer =  Influencers.query.filter(Influencers.id == influencer_id).first()
    update_form = UpdateInfluencer(obj=influencer)
    disabled = True
    if "type" in session.keys() and session["type"] == "Influencer" and session["user"]["id"] == influencer.id:
        disabled = False
    if influencer:
        if request.method == "GET":
            return render_template("influencer/profile.html", influencer=influencer, update_form=update_form, disabled = disabled, niches = niches)
        elif request.method == "POST":
            update_form.populate_obj(influencer)
            db.session.commit()
            return render_template("influencer/profile.html", influencer=influencer, update_form=update_form, disabled = disabled, niches = niches)
    else:
        return render_template("error.html", error_code=404, error_message="Influencer Not Found")   

@app.route("/influencer/register", methods = ["GET", "POST"])
def influencer_register():
    influencer_form = RegisterInfluencer()
    if request.method == "GET":
        return render_template("auth/register.html",title="Influencer Registration", form = influencer_form, influencer=True)
    elif request.method == "POST":
        if influencer_form.validate_on_submit():
            if influencer_form.password.data == influencer_form.repeat_password.data:
                influencer = Influencers()
                influencer_form.populate_obj(influencer)
                db.session.add(influencer)
                db.session.commit()            
                session["type"] = "Influencer"
                session["user"] = assign_user(influencer)
                return redirect(url_for("influencer_dashboard"))
            return render_template("error.html", error_code=404, error_message="Page Not Found")
        return render_template("error.html", error_code=404, error_message="Page Not Found")
    else:
        return render_template("error.html", error_code=404, error_message="Page Not Found")

@app.route("/influencer/dashboard")
def influencer_dashboard():
    if "type" in session.keys() and session["type"] == "Influencer":
        ad_requests_all = AdRequests.query.filter(AdRequests.influencer_id == session["user"]["id"])
        total = ad_requests_all.count()
        ongoing = ad_requests_all.filter(and_(AdRequests.campaign.has(Campaigns.start_date <= date.today()), AdRequests.campaign.has(Campaigns.end_date >= date.today()))).filter(AdRequests.status != 3).count()
        new = ad_requests_all.filter(AdRequests.status != 3).filter(AdRequests.status !=2).count()        
        negotiate_form = NegotiateForm()
        return render_template("influencer/dashboard.html", today = date.today(), ad_requests = ad_requests_all, negotiate_form = negotiate_form, total = total, ongoing = ongoing, new = new)
    else:
        return redirect(url_for("login"))

@app.route("/influencer/find", methods=["GET", "POST"])
def influencer_find():
    if "type" in session.keys() and session["type"] == "Influencer":
        search = SearchForm(request.form)
        ad_request_form = NewAdRequestForm(request.form)
        campaigns = Campaigns.query.filter(Campaigns.visibility==True)
        if request.method == "GET":
            return render_template("influencer/find.html", search_form = search, ad_request_form = ad_request_form, campaigns = campaigns.all(), today = date.today())
        elif request.method == "POST":
            if search.search.data:
                campaigns = Campaigns.query.filter(Campaigns.visibility == True)
                if search.query_string.data:
                    campaigns = campaigns.filter(Campaigns.name.contains(search.query_string.data))
                if search.date.data:
                    campaigns = campaigns.filter(and_(Campaigns.start_date <= search.date.data,Campaigns.end_date >= search.date.data)) 
                if search.revenue.data:
                    print(search.revenue.data)
                    campaigns = campaigns.filter(Campaigns.budget == float(search.revenue.data))
            elif ad_request_form.submit.data:
                ad_request = AdRequests()
                ad_request_form.populate_obj(ad_request)
                ad_request.campaign_id = ad_request_form.campaign_id.data
                ad_request.influencer_id = session["user"]["id"]
                ad_request.status = 1
                db.session.add(ad_request)
                db.session.commit()
            return render_template("influencer/find.html", search_form = search,ad_request_form = ad_request_form, campaigns = campaigns.all(), today = date.today())
    else:
        return redirect(url_for("login"))

@app.route("/influencer/stats")
def influencer_stats():
    if "type" in session.keys() and session["type"] == "Influencer":
        ad_requests = AdRequests.query.filter(AdRequests.influencer_id == session["user"]["id"])
        new = ad_requests.filter(or_(AdRequests.status == 0 , AdRequests.status == 1)).count()
        accepted= ad_requests.filter(AdRequests.status == 2)
        ongoing = accepted.filter(and_(AdRequests.campaign.has(Campaigns.start_date <= date.today()), AdRequests.campaign.has(Campaigns.end_date >=  date.today()))).count()
        completed = accepted.filter(AdRequests.campaign.has(Campaigns.end_date <  date.today())).count()
        rejected = ad_requests.filter(AdRequests.status == 3).count()
        monthly_data = get_monthly_data(accepted)
        print(new, completed, ongoing, rejected, monthly_data)
        return render_template("influencer/stats.html", ad_request_data = [new, ongoing , completed , rejected], monthly_data = monthly_data)
    else:
        return redirect(url_for("login"))
