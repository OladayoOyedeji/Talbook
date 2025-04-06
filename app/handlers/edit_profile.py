from flask import request, render_template, flash, redirect, url_for, session, current_app as app
from app.utils.functions import *
from app.utils.User import *

def handle_edit_profile():
    return render_template('edit_profile.html')
