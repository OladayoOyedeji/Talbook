# File: selling.py
from flask import request, render_template, flash, redirect, url_for
from app.utils import mysql_util

def handle_selling():
    sql = '''
    SELECT T.name, COUNT(IT.item_id) AS tag_count
    FROM Tag as T
    JOIN Item_Tag AS IT ON T.id=IT.tag_id
    GROUP BY T.name;
    '''
    tag_count = mysql_util.execute_sql(sql, fetchdict=True)
    tag_count = {item['name']: item['tag_count'] for item in tag_count}
    return render_template('selling.html', tag_count=tag_count)
