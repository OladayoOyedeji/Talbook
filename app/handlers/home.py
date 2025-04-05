# File: home.py
from flask import session, redirect, url_for, render_template, flash
from app.utils import mysql_util

def handle_home():
    username = session.get('username')
    if username:
        sql = '''
       SELECT 
            I.id,
            I.item_name,
            I.price,
            I.condition,
            U.username,
            IP.photo_id
        FROM Item as I
        JOIN User as U ON I.seller_id=U.id
        JOIN Item_Photo as IP ON I.id=IP.item_id and IP.display_order=0;
        '''
        items = mysql_util.execute_sql(sql)
        return render_template("homepage.html", items=items, user={'username': username})
    else:
        flash("You must log in to view this page.")
        return redirect(url_for('login'))
