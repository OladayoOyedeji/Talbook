# File: login.py
from flask import request, render_template, flash, redirect, url_for
from app.functions import is_valid_login

def handle_login():
    invalid_message = ''

    if (request.method == 'POST'):
        user_or_email = request.form.get('user_or_email')
        password = request.form.get('password')

        if is_valid_login(user_or_email, password):
            flash("Login successful.")
            return redirect(url_for('home'))
        else:
            invalid_message = "Invalid username, email, or password."

    return render_template('login.html', invalid_message=invalid_message)
