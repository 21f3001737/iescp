from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
    )
from flask import render_template
from model.db import db, Sponsors, Campaigns,AdRequests, Influencers
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
    SelectField,
)
from datetime import date
from sqlalchemy import and_, or_

def get_id_and_name(influencer):
    return (influencer.id, influencer.name)
    

class NewAdRequestForm(FlaskForm):
    influencer_id = SelectField('Influencer')
    messages = StringField('Message')
    requirements = StringField('Requirements')
    payment_amount = DecimalField('Payment Amount', validators = [validators.input_required()])
    submit = SubmitField('Done!')

@app.route("/campaign/<campaign_id>", methods =["GET", "POST"])
def campaign_page(campaign_id):
    campaign = Campaigns.query.filter(Campaigns.id == campaign_id).first()
    if campaign:
        owned = False
        if "type" in session.keys() and session["type"] == "Sponsor" and session["user"]["id"] == campaign.sponsor_id:
            owned = True
        if campaign.visibility == True or owned:
            ad_request_form = NewAdRequestForm()
            if request.method == "GET":
                ad_request_form.influencer_id.choices = list(map(get_id_and_name,Influencers.query.all()))
                ad_requests = AdRequests.query.filter(and_(AdRequests.campaign_id == campaign_id, AdRequests.status == 2)).all()
                if owned:
                    ad_requests = ad_requests + AdRequests.query.filter(and_(AdRequests.campaign_id == campaign_id, AdRequests.campaign.has(Campaigns.sponsor_id == session["user"]["id"]))).all()
                return render_template("campaign/campaign.html", today=date.today(), campaign = campaign, ad_requests = ad_requests, form = ad_request_form)
            else:
                ad_request = AdRequests()
                ad_request_form.populate_obj(ad_request)
                ad_request.campaign_id = campaign_id
                ad_request.status = 0
                db.session.add(ad_request)
                db.session.commit()
                return redirect(url_for("campaign_page", campaign_id = campaign_id))               
                
        else:
            return render_template("error.html", error_code=404, error_message="Campaign is not Public")                              
    else:
        return render_template("error.html", error_code=404, error_message="Campaign Not Found")
        
# status: 0 -> negotiation by sponsor
# status: 1 -> negotiation by influencer
# status: 2 -> accepted
# status: 3 -> rejected
