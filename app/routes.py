# File: routes.py
from flask import Flask, render_template, session
from app import app

# import all route handlers from handlers/
from app.handlers.base import handle_base
from app.handlers.signup import handle_signup
from app.handlers.email_verification import handle_email_verification
from app.handlers.login import handle_login
from app.handlers.home import handle_home
from app.handlers.user_profile import handle_user_profile
from app.handlers.bazaar import handle_bazaar
from app.handlers.item_details import handle_item_details
from app.handlers.edit_profile import handle_edit_profile
from app.handlers.selling import handle_selling
from app.handlers.media import handle_media
from app.handlers.inbox import handle_inbox
from app.handlers.chat import handle_chat
from app.handlers.chat_details import handle_chat_details
from app.handlers.start_chat import handle_start_chat

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

@app.route('/user_profile/<username>/media')
def media(username):
    return handle_media(username)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    return handle_edit_profile()

@app.route('/search')
def search():
    return handle_search()

@app.route('/inbox')
def inbox():
    return handle_inbox()

@app.route('/selling', methods=['GET', 'POST'])
def selling():
    return handle_selling()

@app.route("/item/<int:item_id>")
def item_details(item_id):
    return handle_item_details(item_id)
    
@app.route('/bazaar', methods=['GET', 'POST'])
def bazaar():
    return handle_bazaar()

@app.route('/start_chat/<int:seller_id>/<int:item_id>', methods=['POST'])
def start_chat(seller_id, item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        return handle_start_chat(seller_id, item_id)
    
@app.route("/chat")
def chat():
    return handle_chat()

@app.route("/chat/<int:chat_id>", methods=['GET', 'POST'])
def chat_details(chat_id):
    return handle_chat_details(chat_id)

##==============================================================
## Testing routes
##==============================================================
@app.route('/tags')
def tags():
    return render_template('tags.html')
