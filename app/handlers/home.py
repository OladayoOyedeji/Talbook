# File: home.py
from flask import session, redirect, url_for, render_template, flash

def handle_home():
    username = session.get('username')
    if username:
        return render_template('homepage.html', user={'username': username})
    else:
        flash("You must log in to view this page.")
        return redirect(url_for('login'))
