from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *
from app.utils.photo import *

def handle_edit_profile():
    profile=get_data(session['username'])[0]
    profile['photo_filename'] = '/static/Images/%s.png' %profile['photo_id']
    print(profile)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        descrip = request.form.get('descrip')

        if username:
            update_username(profile ,username)
        if email:
            update_email(profile, email)
        if descrip:
            update_descrip(profile,descrip)
        
        if 'file' in request.files:
            print('True')
            file = request.files['file']

        filename = get_image(request)
        if filename:
            image_id = upload_image(filename)
            update_User_photo_id(image_id, profile['id'])
        return redirect(url_for('user_profile', username=username))

    return render_template('edit_profile.html', profile=profile)
