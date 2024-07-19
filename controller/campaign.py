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
        if campaign.visibility == True or ("type" in session.keys() and session["type"] == "Sponsor" and session["id"] == campaign.sponsor_id):
            ad_request_form = NewAdRequestForm()
            if request.method == "GET":
                ad_request_form.influencer_id.choices = list(map(get_id_and_name,Influencers.query.all()))
                ad_requests = AdRequests.query.filter(AdRequests.campaign_id == campaign_id)
                return render_template("campaign/campaign.html", campaign = campaign, ad_requests = ad_requests, form = ad_request_form)
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
        
# status: 0 -> request by sponsor
# status: 1 -> request by influencer
# status: 2 -> negotiation
# status: 3 -> accepted
# status: 4 -> rejected
