# user_profile.py
import os
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *

def handle_user_profile(username):
    
    editable = session['username'] == username
    #id = get_user_id(username)
    image_link = User.get_image_link(username)
    print(image_link)
    #things_you_do = get_subcategories(username)
    profile = {'username':username, 'image':image_link}#, 'things_you_do':things_you_do}
    return render_template('user_profile.html',profile=profile,editable=editable)
