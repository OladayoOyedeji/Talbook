# File: item_details.py
from app import app
from flask import request, render_template
from app.utils.mysql_util import execute_sql

def handle_item_details(item_id):
    sql1 = '''
    SELECT 
        I.id, I.item_name, I.price, I.condition, I.descrip, U.username as seller
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
    SELECT T.name, COUNT(IT.item_id) as tag_count
    FROM Tag as T
    JOIN Item_Tag as IT ON T.id=IT.tag_id
    WHERE IT.item_id = %s
    GROUP BY T.name
    ORDER BY tag_count DESC, T.name ASC;
    '''

    values = execute_sql(sql1, (item_id,), fetchone=True, fetchdict=True)
    if not values:
        return "item not found", 404

    photos = execute_sql(sql2, (item_id,), fetchdict=True)
    tags = execute_sql(sql3, (item_id,), fetchdict=True)

    app.logger.debug("fetching values: %s", values)
    app.logger.debug("fetching photos: %s", photos)
    app.logger.debug("fetching tags: %s", tags)

    return render_template("item_details.html", values=values, photos=photos, tags=tags)
