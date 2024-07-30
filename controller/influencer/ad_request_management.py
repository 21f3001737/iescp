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

from controller.influencer.influencer import NegotiateForm

@app.route("/influencer/accept/<ad_request_id>")
def influencer_accept_request(ad_request_id):
    if "type" in session.keys() and session["type"] == "Influencer":
        ad_request = AdRequests.query.filter(AdRequests.id == ad_request_id).first()
        ad_request.status = 2
        db.session.commit()
        return redirect(url_for("influencer_dashboard"))
    else:
        return redirect(url_for("login"))

@app.route("/influencer/negotiate/", methods=["POST"])
def influencer_negotiate_request():
    if "type" in session.keys() and session["type"] == "Influencer":
        negotiate_form = NegotiateForm(request.form)
        ad_request = AdRequests.query.filter(AdRequests.id == negotiate_form.ad_request_id.data).first()
        ad_request.status = 1
        ad_request.payment_amount = negotiate_form.payment_amount.data 
        db.session.commit()
        return redirect(url_for("influencer_dashboard"))
    else:
        return redirect(url_for("login"))

@app.route("/influencer/reject/<ad_request_id>")
def influencer_reject_request(ad_request_id):
    if "type" in session.keys() and session["type"] == "Influencer":
        ad_request = AdRequests.query.filter(AdRequests.id == ad_request_id).first()
        ad_request.status = 3
        db.session.commit()
        return redirect(url_for("influencer_dashboard"))
    else:
        return redirect(url_for("login"))
