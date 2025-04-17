# File: remove_item.py
from flask import request, session, redirect, url_for

from app.utils import mysql_util

def handle_remove_item(item_id: int):
    if request.method == "POST":
        user_id = session["user_id"]
        
        sql = '''
        SELECT seller_id FROM Item where id = %s;
        '''
        seller_id = mysql_util.execute_sql(sql, item_id, fetchone=True)[0]
        # print("seller_id:", seller_id)

         # if user_id is not seller_id, return
        if user_id != seller_id:
            return "You can not remove an item listing that is not your own"

        # set item as not available (prevents item from being shown)
        sql = '''
        UPDATE Item SET is_available = False where id = %s;
        '''
        mysql_util.execute_sql(sql, item_id, commit=True)

        return redirect(url_for("home"))

        
