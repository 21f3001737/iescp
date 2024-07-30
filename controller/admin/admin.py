from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
    )
from flask import render_template
from model.db import db, Influencers, Sponsors, Campaigns, AdRequests
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
    BooleanField
)
from datetime import date

from sqlalchemy import and_

class SearchForm(FlaskForm):
    query_string = StringField('')
    date = DateField('Date')
    revenue = DecimalField('Revenue')
    flag = BooleanField('Flagged')
    search = SubmitField()


@app.route("/admin/dashboard")
def admin_dashboard():
    if "type" in session.keys() and session["type"] == "Admin":
        campaigns = Campaigns.query.filter(Campaigns.flag == False).all()
        n_campaigns = Campaigns.query.count()
        n_users = Influencers.query.count() + Sponsors.query.count()
        n_ar = AdRequests.query.count()
        #.filter(and_(Campaigns.start_date <= date.today(), Campaigns.end_date >= date.today))
        flagged_users = Influencers.query.filter(Influencers.flag == True).all() + Sponsors.query.filter(Sponsors.flag == True).all()
        flagged_campaigns = Campaigns.query.filter(Campaigns.flag == True).all()
        return render_template("admin/dashboard.html", campaigns = campaigns, flagged = flagged_users + flagged_campaigns, n_campaigns = n_campaigns, n_ar = n_ar, n_users = n_users)
    else:
        return redirect(url_for('login'))

@app.route("/admin/find", methods = ["GET", "POST"])
def admin_find():
    if "type" in session.keys() and session["type"] == "Admin":
        search = SearchForm()
        campaigns = Campaigns.query
        influencers = Influencers.query
        sponsors = Sponsors.query
        if request.method == "GET":
            return render_template("admin/find.html", search_form = search, search_items = campaigns.all() + sponsors.all() + influencers.all())
        else:
            if search.search.data:
                if search.query_string.data:
                    campaigns = campaigns.filter(Campaigns.name.contains(search.query_string.data))
                    influencers = influencers.filter(Influencers.name.contains(search.query_string.data))
                    sponsors = sponsors.filter(Sponsors.name.contains(search.query_string.data))
                if search.date.data:
                    campaigns = campaigns.filter(and_(Campaigns.start_date <= search.date.data, Campaigns.end_date >= search.date.data))
                if search.revenue.data:
                    campaigns = campaigns.filter(Campaigns.budget <= search.revenue.data)
                    influencers = influencers.filter(Influencers.budget <= search.revenue.data)
                    sponsors = sponsors.filter(Sponsors.budget <= search.revenue.data)
                if search.flag.data:
                    campaigns = campaigns.filter(Campaigns.flag == True)
                    influencers = influencers.filter(Influencers.flag == True)
                    sponsors = sponsors.filter(Sponsors.flag == True)
            return render_template("admin/find.html", search_form = search, search_items = campaigns.all() + influencers.all() + sponsors.all())
    else:
        return redirect(url_for('login'))

@app.route("/admin/stats")
def admin_stats():
    if "type" in session.keys() and session["type"] == "Admin":
        return render_template("admin/stats.html")
    else:
        return redirect(url_for('login'))

# 0 -> Influencer
# 1 -> Sponsor
# 2 -> Campaign

@app.route("/admin/flag/<type>/<id>")
def admin_flag(type, id):
    if "type" in session.keys() and session["type"] == "Admin":
        match int(type):
            case 0:
                influencer = Influencers.query.filter(Influencers.id == id).first()
                if influencer:
                    influencer.flag = True 
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('error.html', error_code=404, error_message="Influencer Not Found")
            case 1:
                sponsor = Sponsors.query.filter(Sponsors.id == id).first()
                if sponsor:
                    sponsor.flag = True 
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('error.html', error_code=404, error_message="Sponsor Not Found")
            case 2:
                print(type, id)
                campaign = Campaigns.query.filter(Campaigns.id == id).first()
                if campaign:
                    campaign.flag = True 
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('error.html', error_code=404, error_message="Campaign Not Found")
            case _:
                return render_template('error.html', error_code=501, error_message="Internal Server Error")
    else:
        return redirect(url_for('login'))
@app.route("/admin/unflag/<type>/<id>")
def admin_unflag(type, id):
    if "type" in session.keys() and session["type"] == "Admin":
        match int(type):
            case 0:
                influencer = Influencers.query.filter(Influencers.id == id).first()
                if influencer:
                    influencer.flag = False 
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('error.html', error_code=404, error_message="Influencer Not Found")
            case 1:
                sponsor = Sponsors.query.filter(Sponsors.id == id).first()
                if sponsor:
                    sponsor.flag = False 
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('error.html', error_code=404, error_message="Sponsor Not Found")
            case 2:
                campaign = Campaigns.query.filter(Campaigns.id == id).first()
                if campaign:
                    campaign.flag = False 
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('error.html', error_code=404, error_message="Campaign Not Found")
            case _:
                return render_template('error.html', error_code=501, error_message="Internal Server Error")
    else:
        return redirect(url_for('login'))
