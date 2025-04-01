# File: signup.py
from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import is_valid_username, is_valid_password, invalid_message_password, send_verification_code

def handle_signup():
    is_valid = {'username': True, 'password': True}  # default values
    invalid_message = {'username': '', 'password': ''}
    
    if (request.method == 'POST'):
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        app.logger.debug("email:%s, username:%s, password:%s" % (email, username, password))
        
        # verify fields
        is_valid = {'username': is_valid_username(username),
                    'password': is_valid_password(password)}

        invalid_message = {'username': 'username already used',
                           'password': invalid_message_password()}
        app.logger.debug(is_valid)
        # sends the verification code
        if is_valid['username'] and is_valid['password'] and email:
            session['email'] = email  
            session['username'] = username
            session['password'] = password
            send_verification_code(email)  
            flash("Verification code sent. Please check your email.")
            return redirect(url_for('email_verification'))
        else:
            flash("Registration failed: %s %s" % (is_valid, email))

    return render_template('signup.html', is_valid=is_valid, invalid_message=invalid_message)
