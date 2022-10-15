from sre_constants import SUCCESS
from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify, Response
from flask_login import current_user, login_user,login_required,logout_user
from app.models import User, Jointeam, Event, Feedback, Image, Admin
from app.forms import LoginForm, SignUpForm, FeedbackForm, AdminForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
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
#----------------------------------------------------------#
@app.route('/events', methods=['GET'])
def events():
    events = Event.query.all()
    return render_template("events.html", events=events, event=True)


# Media page (news)
#----------------------------------------------------------
@app.route('/media', methods=['GET'])
def media():
    feedbacks = Feedback.query.all()
    images = Image.query.all()
    return render_template("media.html", media=True, images=images, feedbacks=feedbacks)



# View Team
#----------------------------------------------------------
@app.route('/viewteam', methods=['GET','POST'])
#@login_required
def viewteam():
    mates = Jointeam.query.all()
    admins = Admin.query.all()
    ad = current_user
    form = AdminForm()
    if form.validate_on_submit():
        user = Admin(email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('viewteam'))
    return render_template("viewteam.html", ad=ad, current_user=current_user, form=form, admins=admins, mates=mates, viewteam=True)



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
    
    return redirect(url_for('login'))
    #return redirect(url_for('approval'))



# View feedback/galleries/join team requests 
#----------------------------------------------------------
@app.route('/approval', methods=['GET', 'POST'])
#@login_required
def approval():
    requests = Jointeam.query.all()
    feedbacks = Feedback.query.all()
    images = Image.query.all()
    ad = current_user
    return render_template("approval.html", ad=ad,approval=True, requests=requests, feedbacks=feedbacks, images=images)




# For admin to post or delete events
#----------------------------------------------------------
@app.route('/updateevents', methods=['GET', 'POST'])
#@login_required
def updateevents():
    if request.method == 'GET':
        events = Event.query.all()
        ad = current_user
        return render_template("updateevents.html", ad=ad, events=events, upevent=True)
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

    #requests = Jointeam.query.all()
    #feedbacks = Feedback.query.all()
    #return render_template("approval.html",approval=True, requests=requests, feedbacks=feedbacks)
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


# Approve image to post on webpage
#----------------------------------------------------------
@app.route('/approveImage', methods=['GET','POST'])
def approveImage():
    temp = request.get_json()
    id = json.loads(temp)

    target = Image.query.get(id)
    target.approved = True
    db.session.commit()
    return redirect(url_for('approval'))


# Dismiss image
#----------------------------------------------------------
@app.route('/dismissImage', methods=['GET','POST'])
#@login_required
def dismissImage():
    temp = request.get_json()
    id = json.loads(temp)

    # delete image in database
    target = Image.query.get(id)
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
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('viewteam'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()

        # Flash error message if credentials are incorrect
        if user is None or not user.check_password(form.password.data):
            #flash('Invalid admin account')
            return redirect(url_for('adminlogin'))
        
        # Log user in if credentials are correct and redirect them to the desired page if specified
        login_user(user, remember=True)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('viewteam')
        return redirect(next_page)
    return render_template('adminlogin.html', title='Login for Admin', form=form)


# Remove admin
#----------------------------------------------------------
@app.route('/removeAdmin', methods=['GET', 'POST'])
@login_required
def removeAdmin():
    temp = request.get_json()
    id = json.loads(temp)

    # delete admin in database
    target = Admin.query.get(id)
    db.session.delete(target)
    db.session.commit()
    
    return redirect(url_for('viewteam'))


# Sign up (add admin)
#----------------------------------------------------------
@app.route('/addadmin', methods=['GET', 'POST'])
def addadmin():
    form = AdminForm()
    if form.validate_on_submit():
        user = Admin(email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('viewteam'))
    return render_template('viewteam.html', form=form, viewteam=True)


@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['image_input']

    # check if there is a pic uploaded
    if not pic:
        flash("No picture uploaded")
        return 
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400
    
    img = Image(img=pic.read(), mimetype=mimetype, name=filename, approved=False)
    db.session.add(img)
    db.session.commit()

    flash("Thanks for sharing your experience with us!")
    return redirect(url_for('contact')) 


@app.route('/<int:id>', methods=['GET'])
def get_img(id):

    img = Image.query.filter_by(id=id).first()
    if not img:
        return render_template("404.html")
    return Response(img.img, mimetype=img.mimetype)