# File: email_verification.py
from flask import request, render_template, flash, redirect, url_for, session

from app.utils.functions import is_valid_code
from app.utils.User import register_user

def handle_email_verification():
    if request.method == 'POST':
        if is_valid_code(request.form.get('code')):
            session['verified'] = True
            register_user(session['username'], session['email'], session['password'])
            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        else:
            flash("Invalid code. Please try again.")
    elif request.method == 'GET':
        return render_template('email_verification.html')
