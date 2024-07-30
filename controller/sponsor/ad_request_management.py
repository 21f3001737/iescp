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
from controller.sponsor.sponsor import NegotiateForm

@app.route("/sponsor/ad_request/accept/<ad_request_id>")
def sponsor_accept_request(ad_request_id):
    ad_request = AdRequests.query.filter(AdRequests.id == ad_request_id).first()
    if "type" in session.keys() and session["type"] == "Sponsor" and ad_request.campaign.sponsor_id == session["user"]["id"]:
        ad_request.status = 2
        db.session.commit()
        return redirect(url_for("sponsor_dashboard"))
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/ad_request/negotiate/", methods=["POST"])
def sponsor_negotiate_request():
    negotiate_form = NegotiateForm(request.form)
    ad_request = AdRequests.query.filter(AdRequests.id == negotiate_form.ad_request_id.data).first()
    if "type" in session.keys() and session["type"] == "Sponsor" and ad_request.campaign.sponsor_id == session["user"]["id"]:
        ad_request.status = 0
        ad_request.payment_amount = negotiate_form.payment_amount.data 
        db.session.commit()
        return redirect(url_for("sponsor_dashboard"))
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/ad_request/reject/<ad_request_id>")
def sponsor_reject_request(ad_request_id):
    ad_request = AdRequests.query.filter(AdRequests.id == ad_request_id).first()
    if "type" in session.keys() and session["type"] == "Sponsor" and ad_request.campaign.sponsor_id == session["user"]["id"]:
        ad_request.status = 3
        db.session.commit()
        return redirect(url_for("sponsor_dashboard"))
    else:
        return redirect(url_for("login"))

