# File: selling.py
from flask import request, jsonify, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
import json

from app.utils import mysql_util
from app.utils import photo

def create_listing(tags: list, values: tuple, photos: list, city: str, state: str):
    sql = '''
    INSERT INTO Item (seller_id, item_name, price, `condition`, descrip) VALUES
    (%s, %s, %s, %s, %s)
    '''

    # insert item
    item_id = mysql_util.execute_sql(sql, values, commit=True,
                                     get_lastrowid=True)

    # insert tags and link them
    for tag in tags:
        tsql = "INSERT IGNORE INTO TAG (name) VALUES (%s)"
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

    # link location
    lsql = '''
    SELECT id FROM Location WHERE city=%s AND state=%s;
    '''
    location_id = mysql_util.execute_sql(lsql, params=(city, state))
    if not location_id:
        raise Exception("Location not found.")

    location_id = location_id[0]

    lsql = '''
    INSERT INTO Item_Location (item_id, location_id) VALUES
    (%s, %s);
    '''
    results = mysql_util.execute_sql(lsql, params=(item_id, location_id),
                                     commit=True)
    print(results)

    return item_id

def handle_selling():
    if request.method == 'POST':
        print("FORM DATA: %s", request.form)
        # values
        seller_id = session['user_id']
        print("seller_id", seller_id)
        title = request.form.get('title')
        print("title", title)
        price = float(request.form.get('price'))
        print("price", price)
        condition = request.form.get('condition')
        print("condition", condition)
        description = request.form.get('description')
        print("description", description)

        values = (seller_id, title, price, condition, description)
        print(values)

        # location
        city = request.form.get('city')
        print("city", city)
        state = request.form.get('state')
        print("state", state)
            
        # Get tags (from hidden input)
        tags_data = request.form.get('tags-data')
        tags = json.loads(tags_data) if tags_data else []      
            
        # Handle file uploads
        photos = request.files.getlist('photos')
        photo_names = []
            
        # Save each photo
        dir_path = "app/static/images/uploads/"
        for p in photos:
            if p.filename:
                filename = secure_filename(p.filename)
                filepath = dir_path + filename
                p.save(filepath)
                photo_names.append(filename)

        item_id = create_listing(tags, values, photo_names,
                                     city, state)

        return redirect('item/%s' % item_id)
    
    else:
        # GET request handling
        tag_count = mysql_util.get_all_tag_counts()
        tags = [f"{tag} ({count})" for tag, count in tag_count.items()]
        cities = mysql_util.get_all_distinct_cities()
        return render_template('selling.html', tag_count=tag_count, tags=tags, cities=cities)
