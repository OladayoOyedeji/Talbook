# user_profile.py
import os
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *

def handle_user_profile(username):
    
    profile = get_data(username)
    for values, key in profile:
        profile[key] = values[0]
    
    id = profile['id']
    
    profile['skills'] = get_skills(id)
    profile['listings'] = get_listings(id)
        
    return render_template('user_profile.html',profile=profile,
                           editable=(session['username']==username))
