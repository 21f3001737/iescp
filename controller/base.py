from flask import (
        current_app as app,
        session,
        request,
        url_for,
        redirect,
        flash,
        jsonify,
        render_template
    )
from model.db import db, Sponsors, Influencers, Admin
from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    validators, 
    PasswordField, 
    SubmitField, 
    RadioField, 
)

class Login(FlaskForm):
    username = StringField('Username', validators=[validators.input_required()])
    password = PasswordField('Password')
    type = RadioField(choices=['Admin', 'Sponsor', 'Influencer'], validators=[validators.input_required()])
    submit = SubmitField('Submit')
    
def isValidUser(form):
    if form.type.data == "Sponsor":
        sponsor = Sponsors.query.filter(Sponsors.username == form.username.data).first()
        if sponsor:
            if sponsor.password == form.password.data:
                return sponsor, None
            else:
                return None, 1
        else:
            return None, 2
    elif form.type.data == "Influencer":
        influencer = Influencers.query.filter(Influencers.username == form.username.data).first()
        if influencer:
            if influencer.password == form.password.data:
                return influencer, None
            else:
                return None, 1
        else:
            return None, 2
    elif form.type.data == "Admin":
        admin = Admin.query.filter(Admin.username == form.username.data).first()
        if admin:
            if admin.password == form.password.data:
                return admin, None
            else:
                return None, 1
        else:
            return None, 2
    else:
        return None, None
        

def assign_user(user):
    duser = dict()
    try:
        duser["id"] = user.id
        duser["name"] = user.name
        duser["username"] = user.username
        duser["budget"] = user.budget
        duser["category"] = user.category
        duser["industry"] = user.industry
    except AttributeError:
        pass
    return duser

@app.route("/")
def home():
    if "type" not in session.keys():
        return redirect(url_for('login'))
    else:
        return redirect(url_for('dashboard'))

@app.route("/login", methods = ["GET", "POST"])
def login():
    login = Login()
    if request.method == "GET":
        return render_template("auth/login.html",title="Login", form= login, login=True)
    elif request.method == "POST":
        if login.validate_on_submit():
            user, error = isValidUser(login)
            if user:
                session["type"] = login.type.data    
                session["user"] = assign_user(user)
                return redirect(url_for("dashboard"))
            else:
                if error == 1:
                    flash("Wrong Password!")
                    return render_template("auth/login.html", title="Login", form = login, login = True)
                elif error == 2:
                    flash("User not Found")
                    return render_template("auth/login.html", title="Login", form = login, login = True)
                else:
                    return render_template("error.html", error_code=500, error_message="Internal Server Error")
        else:
            return render_template("auth/login.html", title="Login", form=login, login = True)
    else:
        return render_template("error.html", error_code=501, error_message=request.method + " method Not Implemented")

@app.route("/logout")
def logout():
    if "type" in session.keys():
        session.pop("type")
    if "user" in session.keys():
        session.pop("user")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "type" in session.keys():
        if session["type"] == "Influencer":
            return redirect(url_for("influencer_dashboard"))
        elif session["type"] == "Sponsor":
            return redirect(url_for("sponsor_dashboard"))
        elif session["type"] == "Admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("login"))
