# File: bazaar.py
from flask import request, render_template
from app.utils.mysql_util import execute_sql

def handle_bazaar():
    """
    Fetches all items from the database and renders them in the bazaar page.
    """
    sql = '''
       SELECT 
            i.id, i.item_name, i.price, i.condition, u.username
        FROM Item i
        JOIN User u ON i.seller_id = u.id;
    '''
    items = execute_sql(sql)
    return render_template("bazaar.html", items=items)
