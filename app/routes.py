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
    return render_template("home.html")

@app.route('/events')
def events():
    return render_template("events.html")

@app.route('/media')
def media():
    pass
    return render_template("media.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")
