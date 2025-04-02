# File: routes.py
from flask import Flask
from app import app

# import all route handlers from handlers/
from app.handlers.base import handle_base
from app.handlers.signup import handle_signup
from app.handlers.email_verification import handle_email_verification
from app.handlers.login import handle_login
from app.handlers.home import handle_home
from app.handlers.home import handle_user_profile
from app.handlers.bazaar import handle_bazaar
from app.handlers.item_details import handle_item_details

##==============================================================
## Routes are defined here, but their logic is kept in separate
## handler files
##==============================================================
@app.route('/')
def base():
    return handle_base()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return handle_signup()

@app.route('/email_verification', methods=['GET', 'POST'])
def email_verification():
    return handle_email_verification()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return handle_login()

@app.route('/home')
def home():
    return handle_home()
    
@app.route('/user_profile/<username>')
def user_profile(username):
    return handle_user_profile(username)
    
@app.route("/item/<int:item_id>")
def item_details(item_id):
    return handle_item_details(item_id)
    
@app.route('/bazaar', methods=['GET', 'POST'])
def bazaar():
    return handle_bazaar()
