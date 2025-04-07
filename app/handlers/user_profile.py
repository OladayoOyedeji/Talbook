# user_profile.py
import os
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *

def handle_user_profile(username):
    
    profile = (get_data(username))[0]
    print(profile)


    
    id = profile['id']

    print("here")
    profile['skills'] = get_skills(id)
    print("or here?")
    if profile['skills'] == None:
        profile['skills'] = ['']
    
    profile['listings'] = get_listings(id)
    print()
    print(profile['listings'])
    return render_template('user_profile.html',profile=profile,
                           editable=(session['username']==username))
