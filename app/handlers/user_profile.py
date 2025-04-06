# user_profile.py
import os
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *

def handle_user_profile(username):
    
    profile = (get_data(username))[0]
    print(profile)


    
    id = profile['id']
    
    profile['skills'] = get_skills(id)

    if profile['skills'] == None:
        profile['skills'] = ['']
    
    profile['listings'] = get_listings(id)
        
    return render_template('user_profile.html',profile=profile,
                           editable=(session['username']==username))
