# File: remove_item.py
from flask import request, jsonify, render_template, session, redirect, url_for

from app.utils import mysql_util

def handle_remove_item(item_id: int):
    user_id = session["user_id"]

    # if user_id is not seller_id, return
