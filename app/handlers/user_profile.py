# user_profile.py
import os
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *

def handle_user_profile(username, listings=True):
    
    profile = (get_data(username))[0]
    print(profile)
    
    id = profile['id']

    print("here")
    if listings:
        profile['skills'] = get_services(id)
        print("or here?")
        if profile['skills'] == None:
            profile['skills'] = ['']
    
        profile['listings'] = get_listings(id)
        print()
        print(profile)
    # else:
    #     # get_from_post: post_id, list of pictures, list of videos, descrip, time

    profile['bookmarks'] = get_bookmarked_items(id)
    
    return render_template('user_profile.html', listings=listings, profile=profile,
                           editable=(session['username'] == username))
