from re import S
from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user,login_required,logout_user
from app.models import User
from werkzeug.urls import url_parse

from sqlalchemy import func 
from app.api.errors import bad_request

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", home=True)

@app.route('/events')
def events():
    return render_template("events.html", event=True)

@app.route('/media')
def media():
    pass
    return render_template("media.html", media=True)

@app.route('/contact')
def contact():
<<<<<<< Updated upstream
    return render_template("contact.html")
=======
    return render_template("contact.html", contact=True)


# Login for admin only
#----------------------------------------------------------
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    #return redirect(url_for('login'))
    return redirect(url_for('approval'))


# View feedback and post approved feedback 
#----------------------------------------------------------
@app.route('/approval', methods=['GET', 'POST'])
@login_required
def approval():
    return render_template("approval.html", approval=True)


# For admin to post or delete events
#----------------------------------------------------------
@app.route('/updateevents', methods=['GET', 'POST'])
@login_required
def updateevents():
    return render_template("updateevents.html", upevent=True)


# Logout
#----------------------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Login/Sign In
#----------------------------------------------------------
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])

def login():

    if current_user.is_authenticated:
        return redirect(url_for('approval'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid admin account')
            return redirect(url_for('adminlogin'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('approval')
        return redirect(next_page)
    return render_template('adminlogin.html', title='Login for Admin', form=form)
>>>>>>> Stashed changes
