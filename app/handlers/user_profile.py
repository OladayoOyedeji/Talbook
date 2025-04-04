# user_profile.py
import os
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *

def handle_user_profile(username):
    
    if session['username'] != username:
        profile = get_data(username)
        
        profile['image_link'] = User.get_image_link(id)
        profile['skills'] = get_skills(id)
        profile['listings'] = get_listings(id)
        
        return render_template('user_profile.html',profile=profile, editable=False)
    else:
        return render_template('user_profile.html', profile=session, editable=True)
