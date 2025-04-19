# File: selling.py
from flask import request, jsonify, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
import json
import uuid

from app.utils import mysql_util
from app.utils import photo

def create_listing(tags: list, values: tuple, photos: list, location_id: int):
    # insert item
    sql = '''
    INSERT INTO Item (seller_id, item_name, price, `condition`, descrip) VALUES
    (%s, %s, %s, %s, %s)
    '''
    item_id = mysql_util.execute_sql(sql, values, commit=True,
                                     get_lastrowid=True)

    # link location
    lsql = '''
    INSERT INTO Item_Location (item_id, location_id) VALUES
    (%s, %s);
    '''
    results = mysql_util.execute_sql(lsql,
                                     params=(item_id, location_id),
                                     commit=True)
    print(results)

    # insert tags and link them
    for tag in tags:
        tsql = "INSERT IGNORE INTO Tag (name) VALUES (%s)"
        mysql_util.execute_sql(tsql, (tag,), commit=True)
        tsql = "INSERT INTO Item_Tag (item_id, tag_id) SELECT %s, id FROM Tag WHERE name=%s"
        mysql_util.execute_sql(tsql, (item_id, tag), commit=True)

    # upload and link photos
    dir_path = "app/static/images/uploads/"
    for display_order, file in enumerate(photos):
        print("inserting photo %s" % (dir_path + file))
        photo_id = photo.upload_image(dir_path + file)
        print("photo id is %s" % photo_id)
        photo.link_item_photo(item_id, photo_id, display_order)

    return item_id

def handle_selling():
    if request.method == 'POST':
        seller_id = session['user_id']
        title = request.form.get('title')
        price = float(request.form.get('price'))
        condition = request.form.get('condition')
        description = request.form.get('description')
        city = request.form.get('city')
        state = request.form.get('state')
        values = (seller_id, title, price, condition, description)

        # test if location is valid
        lsql = '''
        SELECT id FROM Location WHERE city=%s AND state=%s;
        '''
        location_id = mysql_util.execute_sql(lsql, params=(city, state))
        if not location_id:
            return "Location not found in USA"
        location_id = location_id[0]
    
        # Parse tags JSON (Tagify sends JSON array)
        tags_raw = request.form.get('tags', '[]')
        try:
            tag_objs = json.loads(tags_raw)
            tags = [tag['value'] for tag in tag_objs if 'value' in tag]
        except (json.JSONDecodeError, TypeError):
            return "Invalid tag format", 400

        # Enforce tag limit
        if len(tags) > 30:
            return "Too many tags: limit is 30", 400

        # Handle photo uploads
        photos = request.files.getlist('photos')
        photo_names = []
        dir_path = "app/static/images/uploads/"
        for p in photos:
            if p.filename:
                filename = str(uuid.uuid4())
                filepath = dir_path + filename
                p.save(filepath)
                photo_names.append(filename)

        item_id = create_listing(tags, values, photo_names, city, state)
        return redirect(f'item/{item_id}')
    
    else:
        tag_count = mysql_util.get_all_tag_counts()
        tags = [f"{tag} ({count})" for tag, count in tag_count.items()]
        cities = mysql_util.get_all_distinct_cities()
        return render_template('selling.html', tag_count=tag_count, tags=tags, cities=cities, user={'username': session["username"]})
