# File: item_details.py
from app import app
from flask import request, render_template, session, redirect, url_for

from app.utils import mysql_util

def is_bookmarked(user_id, item_id):
    sql = '''
    SELECT * FROM Bookmark where user_id=%s AND item_id=%s;
    '''
    results = mysql_util.execute_sql(sql, (user_id, item_id))
    return bool(results)

def add_bookmark(user_id, item_id):
    sql = '''
    INSERT INTO Bookmark (user_id, item_id) VALUES
    (%s, %s);
    '''
    mysql_util.execute_sql(sql, (user_id, item_id), commit=True)

def remove_bookmark(user_id, item_id):
    sql = '''
    DELETE FROM Bookmark WHERE user_id=%s AND item_id=%s;
    '''
    mysql_util.execute_sql(sql, (user_id, item_id), commit=True)
    
def handle_bookmark_item(item_id: int):
    user_id = session['user_id']
    action = request.form.get('action')

    if action == 'add':
        add_bookmark(user_id, item_id)
    elif action == 'remove':
        remove_bookmark(user_id, item_id)

    return redirect(url_for('item_details', item_id=item_id))

def handle_item_details(item_id):
    user_id = session["user_id"]
    
    sql1 = '''
    SELECT 
        I.id, I.item_name, I.price, I.condition, I.descrip, U.username as seller, I.created_at, U.id as seller_id
    FROM Item as I
    JOIN User as U ON I.seller_id = U.id
    WHERE I.id = %s;
    '''
    
    sql2 = '''
    SELECT photo_id, display_order 
    FROM Item_Photo 
    WHERE item_id = %s 
    ORDER BY display_order ASC;
    '''
    
    sql3 = '''
    SELECT T.name, COUNT(IT.item_id) AS tag_count
    FROM Tag AS T
    JOIN Item_Tag AS IT ON T.id=IT.tag_id
    WHERE T.id IN (
        SELECT tag_id FROM Item_Tag WHERE item_id=%s
        )
    GROUP BY T.name
    ORDER BY tag_count DESC, T.name ASC;
    '''

    sql4 = '''
    SELECT L.city, L.state
    FROM Location as L
    JOIN Item_Location as IL
    ON IL.item_id=%s and IL.location_id=L.id;
    '''

    values = mysql_util.execute_sql(sql1, (item_id,), fetchone=True, fetchdict=True)
    if not values:
        return "item not found"

    photos = mysql_util.execute_sql(sql2, (item_id,), fetchdict=True)
    tags = mysql_util.execute_sql(sql3, (item_id,), fetchdict=True)
    location = mysql_util.execute_sql(sql4, (item_id,), fetchone=True, fetchdict=True)
    city = location["city"]
    state = location["state"]

    if values:
        app.logger.debug("fetching values: %s" % values)
    if photos:
        app.logger.debug("fetching photos: %s" % photos)
    if tags:
        app.logger.debug("fetching tags: %s" % tags)
    if location:
        app.logger.debug("fetching location: %s" % location)

    return render_template("item_details.html", values=values,
                           photos=photos, tags=tags, city=city,
                           state=state, user_id=user_id,
                           is_bookmarked=is_bookmarked(user_id, item_id))
