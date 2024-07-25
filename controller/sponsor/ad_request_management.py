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

@app.route("/sponsor/ad_request/accept/<ad_request_id>")
def sponsor_accept_request(ad_request_id):
    ad_request = AdRequests.query.filter(AdRequests.id == ad_request_id).first()
    if "type" in session.keys() and session["type"] == "Sponsor" and ad_request.campaign.sponsor_id == session["user"]["id"]:
        ad_request.status = 2
        db.session.commit()
        return redirect(url_for("sponsor_dashboard"))
    else:
        return redirect(url_for("login"))

@app.route("/sponsor/ad_request/negotiate/<ad_request_id>/<amount>")
def sponsor_negotiate_request(ad_request_id, amount):
    ad_request = AdRequests.query.filter(AdRequests.id == ad_request_id).first()
    if "type" in session.keys() and session["type"] == "Sponsor" and ad_request.campaign.sponsor_id == session["user"]["id"]:
        ad_request.status = 1
        ad_request.payment_amount = amount 
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

