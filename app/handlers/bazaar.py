# File: bazaar.py
from flask import request, render_template
from app.utils.mysql_util import execute_sql

def handle_bazaar():
    """
    Fetches all items from the database and renders them in the bazaar page
    """
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
    items = execute_sql(sql)
    return render_template("bazaar.html", items=items)
