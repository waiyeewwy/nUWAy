from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user,login_required,logout_user
from app.models import User, Jointeam, Event, Feedback
from app.forms import LoginForm, SignUpForm, FeedbackForm
from werkzeug.urls import url_parse
from sqlalchemy import func 
from app.api.errors import bad_request

import json

# Home page
#----------------------------------------------------------
@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html", home=True)


# Upcoming event page
#----------------------------------------------------------
@app.route('/events', methods=['GET'])
def events():
    events = Event.query.all()
    return render_template("events.html", events=events, event=True)


# Media page (news)
#----------------------------------------------------------
@app.route('/media', methods=['GET'])
def media():
    feedbacks = Feedback.query.all()
    return render_template("media.html", media=True, feedbacks=feedbacks)



# View Team
#----------------------------------------------------------
@app.route('/viewteam', methods=['GET'])
def viewteam():
    mates = Jointeam.query.all()
    return render_template("viewteam.html", mates=mates, viewteam=True)



# Sign up to join team
#----------------------------------------------------------
@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = Jointeam(email=form.email.data.lower(), name=form.name.data, approved=False)
        db.session.add(user)
        db.session.commit()
        flash('You have succesfully submitted your interest, our team will contact you by email shortly.')
    return render_template("signup.html", form=form, signup=True)


# Contact us page
#----------------------------------------------------------
@app.route('/contact', methods=['GET','POST'])
def contact():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(feedback=form.feedback.data, name=form.name.data, approved=False)
        db.session.add(feedback)
        db.session.commit()
        flash('You have succesfully submitted your feedback.')

    return render_template('contact.html', title="Contact Us", form=form, contact=True)
    
    


# Login for admin only
#----------------------------------------------------------
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    
    #return redirect(url_for('login'))
    return redirect(url_for('approval'))



# View feedback/galleries/join team requests 
#----------------------------------------------------------
@app.route('/approval', methods=['GET', 'POST'])
#@login_required
def approval():
    requests = Jointeam.query.all()
    feedbacks = Feedback.query.all()
    return render_template("approval.html", approval=True, requests=requests, feedbacks=feedbacks)




# For admin to post or delete events
#----------------------------------------------------------
@app.route('/updateevents', methods=['GET', 'POST'])
#@login_required
def updateevents():
    if request.method == 'GET':
        events = Event.query.all()
        return render_template("updateevents.html", events=events, upevent=True)
    else:
        data = request.get_json() or {}
        event = Event(
            name=data['eventName'],
            date=data['eventDate'],
            info=data['eventInfo']
        )
        db.session.add(event)
        db.session.commit()

        
        # Return response
        response = jsonify(event.to_dict())
        response.status_code = 201 
        response.headers['Location'] = url_for('updateevents')
        return response



# Delete past event
#----------------------------------------------------------
@app.route('/deleteEvent', methods=['GET','POST'])
#@login_required
def deleteEvent():
    temp = request.get_json()
    eventId = json.loads(temp)

    # Restrict access to superadmin only
    #if current_user.email != "nuwayuwa@gmail.com":
    #    return bad_request("Action not allowed")
    
    # Delete event from database
    event = Event.query.get(eventId)
    db.session.delete(event)
    db.session.commit()
    return ('success')



# Join team
#----------------------------------------------------------
@app.route('/joinTeam', methods=['GET','POST'])
#@login_required
def joinTeam():
    temp = request.get_json()
    id = json.loads(temp)

    # Restrict access to superadmin only
    #if current_user.email != "nuwayuwa@gmail.com":
    #    return bad_request("Action not allowed")

    # Add people into team
    target = Jointeam.query.get(id)
    target.approved = True
    db.session.commit()
    
    return redirect(url_for('approval'))


# Dismiss join team request
#----------------------------------------------------------
@app.route('/denyJoinTeam', methods=['GET','POST'])
#@login_required
def denyJoinTeam():
    temp = request.get_json()
    id = json.loads(temp)

    # delete user in database
    target = Jointeam.query.get(id)
    db.session.delete(target)
    db.session.commit()
    
    return redirect(url_for('approval'))


# Leave team
#----------------------------------------------------------
@app.route('/leaveTeam', methods=['GET', 'POST'])
def leaveTeam():
    temp = request.get_json()
    id = json.loads(temp)

    # delete user in database
    target = Jointeam.query.get(id)
    db.session.delete(target)
    db.session.commit()
    
    return redirect(url_for('viewteam'))



# Approve feedback to post on webpage
#----------------------------------------------------------
@app.route('/approveFeedback', methods=['GET','POST'])
#@login_required
def approveFeedback():
    temp = request.get_json()
    id = json.loads(temp)

    # Restrict access to superadmin only
    #if current_user.email != "nuwayuwa@gmail.com":
    #    return bad_request("Action not allowed")

    # Add people into team
    target = Feedback.query.get(id)
    target.approved = True
    db.session.commit()

    requests = Jointeam.query.all()
    feedbacks = Feedback.query.all()
    return render_template("approval.html",approval=True, requests=requests, feedbacks=feedbacks)
    return redirect(url_for('approval'))



# Dismiss feedback
#----------------------------------------------------------
@app.route('/dismissFeedback', methods=['GET','POST'])
#@login_required
def dismissFeedback():
    temp = request.get_json()
    id = json.loads(temp)

    # delete user in database
    target = Feedback.query.get(id)
    db.session.delete(target)
    db.session.commit()
    
    return redirect(url_for('approval'))



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

