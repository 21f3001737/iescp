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
from sqlalchemy import and_

from controller.base import assign_user

class RegisterInfluencer(FlaskForm):
    name = StringField('Name', validators = [validators.input_required()])
    username = StringField('Username', validators=[validators.input_required()])
    password = PasswordField('Password', validators = [validators.input_required()])
    repeat_password = PasswordField('Repeat Password', validators = [validators.input_required()])
    category = StringField('Category', validators = [validators.input_required()])
    niche = SelectField('Neiche', validators=[validators.input_required()])
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
    revenue = DecimalField('Revenue')
    search  = SubmitField()


class NewAdRequestForm(FlaskForm):
    campaign_id = IntegerField('Campaign ID', validators=[validators.input_required()])
    messages = StringField('Message', validators = [validators.input_required()])
    requirements = StringField('Requirements', validators=[validators.input_required()])
    payment_amount = DecimalField('Payment Amount', validators = [validators.input_required()])
    submit = SubmitField('Done!')

def double_niche(niche):
    return niche[0]

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
        return render_template("form.html",title="Influencer Registration", form = influencer_form, login=False)
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
        active_requests = ad_requests_all.filter(AdRequests.status == 2).all()
        outgoing_requests = ad_requests_all.filter(AdRequests.status == 1).all()
        incoming_requests = ad_requests_all.filter(AdRequests.status == 0).all()
        return render_template("influencer/dashboard.html", campaigns = active_requests, incoming_requests = incoming_requests, outgoing_requests = outgoing_requests)
    else:
        return redirect(url_for("login"))

@app.route("/influencer/find", methods=["GET", "POST"])
def influencer_find():
    if "type" in session.keys() and session["type"] == "Influencer":
        search = SearchForm(request.form)
        ad_request_form = NewAdRequestForm(request.form)
        campaigns = Campaigns.query.filter(Campaigns.visibility==True)
        if request.method == "GET":
            return render_template("influencer/find.html", search_form = search, ad_request_form = ad_request_form, campaigns = campaigns.all())
        elif request.method == "POST":
            if search.search.data:
                campaigns = Campaigns.query.filter(Campaigns.visibility == True)
                if search.query_string.data:
                    campaigns = campaigns.filter(Campaigns.name.contains(search.query_string.data))
                if search.date.data:
                    campaigns = campaigns.filter(and_(Campaigns.start_date <= search.date.data,Campaigns.end_date >= search.date.data)) 
                if search.revenue.data:
                    campaigns = campaigns.filter(Campaigns.budget <= search.revenue.data)
            elif ad_request_form.submit.data:
                ad_request = AdRequests()
                ad_request_form.populate_obj(ad_request)
                ad_request.campaign_id = ad_request_form.campaign_id.data
                ad_request.influencer_id = session["user"]["id"]
                ad_request.status = 1
                db.session.add(ad_request)
                db.session.commit()
            return render_template("influencer/find.html", search_form = search,ad_request_form = ad_request_form, campaigns = campaigns.all())
    else:
        return redirect(url_for("login"))

@app.route("/influencer/stats")
def influencer_stats():
    if "type" in session.keys() and session["type"] == "Influencer":
        return render_template("influencer/stats.html")
    else:
        return redirect(url_for("login"))
