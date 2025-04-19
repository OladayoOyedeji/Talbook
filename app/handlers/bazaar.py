# File: bazaar.py
from flask import request, render_template
from app.utils.mysql_util import execute_sql

def handle_bazaar():
    return render_template("bazaar.html")
