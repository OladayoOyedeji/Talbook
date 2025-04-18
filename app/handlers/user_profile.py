# user_profile.py
import os
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *

def handle_user_profile(username, listings=True):
    
    profile = (get_data(username))[0]
    print(profile)
    
    id = profile['id']
    profile['following_list'] = get_follower_list(id)
    profile['followers_list'] = get_followed_list(id)

    profile['following_count'] = len(profile['following_list'])
    profile['followers_count'] = len(profile['followers_list'])
    print(profile['following_count'], profile['followers_count'])
    print("here")
    if listings:
        profile['skills'] = get_services(id)
        print("or here?")
        if profile['skills'] == None:
            profile['skills'] = ['']
    
        profile['listings'] = get_listings(id)
        print()
        print(profile)
        
    else:
        profile['media'] = get_posts(id)
        if not profile['media']:
            profile['media'] = []
        profile['media'].sort(reverse=True)

        print(profile['media'])

    if (session['username']!=username):
        profile['is_following'] = is_following(session['user_id'], profile['id'])
        if request.method == 'POST':
            print("this is follow", profile['is_following'])
            if profile['is_following']:
                unfollow(session['user_id'], profile['id'])
                profile['followers_count'] -= 1
                profile['is_following'] = False
            else:
                follow(session['user_id'], profile['id'])
                profile['followers_count'] += 1
                profile['is_following'] = True
    

    profile['bookmarks'] = get_bookmarked_items(id)

    return render_template('user_profile.html', listings=listings, profile=profile,
                           editable=(session['username'] == username))
