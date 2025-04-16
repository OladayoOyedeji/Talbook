from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *
from app.utils.photo import *

def handle_edit_profile():
    profile=get_data(session['username'])[0]
    profile['photo_filename'] = '/static/Images/%s.webp' % profile['photo_id']
    profile['services'] = get_services(profile['id'])
    skills = get_skills()
    
    d = dict(skills)
    
    print(profile)
    if request.method == 'POST':
        print(request.form)
        
        if 'submit_info' in request.form:
            username = request.form.get('username')
            email = request.form.get('email')
            descrip = request.form.get('descrip')
            services = request.form.getlist('skills')

            print(services)
            
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
            
                # services is the new list
                # profile['services'] is the old list
                # new list - old list are the things you wanna add
                # old list - new list are the things you wanna delete
            new_id = []
            old_id = []
            print(id, type(id))
            for i in services:
                print(d[i])
                new_id.append(d[i])
            for i, in profile['services']:
                old_id.append(d[i])
            print(id)
            print(services, '\n', profile['services'])
            add_skills = list(set(new_id) - set(old_id))
            delete_skills = list(set(old_id) - set(new_id))
            
            update_services(profile, add_skills, delete_skills)
            profile['services'] = get_services(profile['id'])
            flash("info updated")
            # handle photo upload
            
        elif 'file' in request.files:
                # handle user info update
            
            filename = get_image(request)
        
            print("filename", filename)
            if filename:
                image_id = upload_image(filename)
                profile['photo_id'] = image_id
                print(image_id)
                update_User_photo_id(image_id, profile['id'])
                flash("profile photo updated")
        # return redirect(url_for('user_profile', username=username))
        flash("profile saved")
    return render_template('edit_profile.html', profile=profile, skills=skills)

