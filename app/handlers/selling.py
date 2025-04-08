# File: selling.py
from flask import request, render_template, flash, redirect, url_for

def handle_selling():
    return render_template('selling.html')
