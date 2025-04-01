# item_details.py
from flask import request, render_template
from app.utils.mysql_util import execute_sql

def handle_item_details(item_id):
    return render_template("item_details.html")

