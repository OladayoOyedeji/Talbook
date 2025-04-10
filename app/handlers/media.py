from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *
from app.utils.photo import *
from app.handlers.user_profile import handle_user_profile

def handle_media(username):
    return handle_user_profile(username, False)
    
