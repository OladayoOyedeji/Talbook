# File: base.py
from flask import request, render_template, flash, redirect, url_for, session, current_app as app

def handle_base():
    return render_template('base.html')
