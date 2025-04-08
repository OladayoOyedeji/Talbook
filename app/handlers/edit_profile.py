from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *
from app.utils.photo import *

def handle_edit_profile():
    profile=get_data(session['username'])[0]
    profile['photo_filename'] = '/static/Images/%s.png' %profile['photo_id']
    print(profile)
    if request.method == 'POST':
        if 'submit_info' in request.form:
            username = request.form.get('username')
            email = request.form.get('email')
            descrip = request.form.get('descrip')
            print(username, email, descrip)
            if username:
                update_username(profile, username)
                profile['username'] = username
            if email:
                update_email(profile, email)
                profile['email'] = email
            if descrip:
                update_descrip(profile,descrip)
                profile['descrip'] = descrip
            flash("info updated")
            # handle photo upload
        elif 'submit_photo' in request.form:
                # handle user info update
                
            filename = get_image(request)
        
            print("filename", filename)
            if filename:
                image_id = upload_image(filename)
                print(image_id)
                update_User_photo_id(image_id, profile['id'])
                flash("profile photo updated")
        # return redirect(url_for('user_profile', username=username))
        flash("profile saved")
    return render_template('edit_profile.html', profile=profile)
