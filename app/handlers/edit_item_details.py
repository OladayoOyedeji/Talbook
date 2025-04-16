# File: edit_item_details.py
from flask import request, render_template, session, redirect, url_for, flash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

from app.utils import mysql_util
from app.utils import photo  # Import your photo utility functions

def handle_edit_item_details(item_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Fetch the item details
    item_sql = "SELECT * FROM Item WHERE id = %s"
    item = mysql_util.execute_sql(item_sql, params=(item_id,), fetchone=True, fetchdict=True)

    if not item:
        flash("Item not found.", "error")
        return redirect(url_for("home")) 

    # verify ownership
    if item["seller_id"] != user_id:
        flash("You do not have permission to edit this item.", "error")
        return redirect(url_for("item_details", item_id=item_id))

    # Fetch associated photos
    photos_sql = "SELECT photo_id FROM Photo WHERE item_id = %s"
    photos_result = mysql_util.execute_sql(photos_sql, params=(item_id,), fetchdict=True)
    photos = photos_result if photos_result else []

    # Fetch associated tags
    tags_sql = """
    SELECT t.name
    FROM Tag t
    JOIN ItemTag it ON t.id = it.tag_id
    WHERE it.item_id = %s;
    """
    tags_result = mysql_util.execute_sql(tags_sql, params=(item_id,), fetchdict=True)
    tags = [tag['name'] for tag in tags_result] if tags_result else []

    if request.method == 'GET':
        return render_template('edit_item_details.html', item=item, photos=photos, tags=tags)

    elif request.method == 'POST':
        item_name = request.form.get('item_name')
        price = request.form.get('price')
        condition = request.form.get('condition')
        descrip = request.form.get('descrip')
        city = request.form.get('city')
        state = request.form.get('state')
        new_photos = request.files.getlist('photos')
        delete_photo_ids = request.form.getlist('delete_photos')
        tag_string = request.form.get('tags')

        # Basic validation
        if not item_name or not price:
            flash('Item name and price are required.', 'error')
            return render_template('edit_item_details.html', item=item, photos=photos, tags=tags)
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            flash('Price must be a valid positive number.', 'error')
            return render_template('edit_item_details.html', item=item, photos=photos, tags=tags)

        # Update item details
        update_item_sql = """
        UPDATE Item
        SET item_name = %s, price = %s, condition = %s, descrip = %s, city = %s, state = %s
        WHERE id = %s
        """
        mysql_util.execute_sql(
            update_item_sql,
            params=(item_name, price, condition, descrip, city, state, item_id),
            commit=True
        )

        upload_folder = 'app/static/images/uploads/' # Use the upload folder defined in photo.py
        store_folder = 'app/static/images/store/' # Define store folder for webp

        # Handle new photos
        for photo_file in new_photos:
            if photo_file and photo.allowed_file(photo_file.filename):
                filename = secure_filename(photo_file.filename)
                filepath = os.path.join(upload_folder, filename)
                photo_file.save(filepath)
                new_photo_id = photo.upload_image(filepath) # Use the upload_image function
                if new_photo_id:
                    link_item_photo_sql = "INSERT INTO ItemPhoto (item_id, photo_id, display_order) VALUES (%s, %s, 0)" # Default display order
                    mysql_util.execute_sql(link_item_photo_sql, params=(item_id, new_photo_id), commit=True)

        # Handle photo deletion
        if delete_photo_ids:
            for photo_id_to_delete in delete_photo_ids:
                # Verify the photo belongs to this item (for security)
                check_photo_sql = "SELECT filename FROM Photo WHERE photo_id = %s AND item_id = %s"
                photo_to_delete = mysql_util.execute_sql(check_photo_sql, params=(photo_id_to_delete, item_id), fetchone=True, fetchdict=True)
                if photo_to_delete:
                    filename_to_delete = photo_to_delete['filename']
                    filepath_to_delete = os.path.join(store_folder, filename_to_delete) # Assuming webp in store folder
                    if os.path.exists(filepath_to_delete):
                        os.remove(filepath_to_delete)
                    delete_photo_sql = "DELETE FROM Photo WHERE photo_id = %s"
                    mysql_util.execute_sql(delete_photo_sql, params=(photo_id_to_delete,), commit=True)
                    # Also remove from ItemPhoto link table
                    delete_item_photo_link_sql = "DELETE FROM ItemPhoto WHERE item_id = %s AND photo_id = %s"
                    mysql_util.execute_sql(delete_item_photo_link_sql, params=(item_id, photo_id_to_delete), commit=True)

        # Handle tags
        # Clear existing tags for the item
        delete_item_tags_sql = "DELETE FROM ItemTag WHERE item_id = %s"
        mysql_util.execute_sql(delete_item_tags_sql, params=(item_id,), commit=True)

        if tag_string:
            tags_list = [tag.strip().lower() for tag in tag_string.split(',') if tag.strip()]
            for tag_name in set(tags_list):  # Use set for unique tags
                # Check if the tag exists, if not, insert it
                check_tag_sql = "SELECT id FROM Tag WHERE name = %s"
                tag_result = mysql_util.execute_sql(check_tag_sql, params=(tag_name,), fetchone=True, fetchdict=True)
                if tag_result:
                    tag_id = tag_result['id']
                else:
                    insert_tag_sql = "INSERT INTO Tag (name) VALUES (%s)"
                    mysql_util.execute_sql(insert_tag_sql, params=(tag_name,), commit=True, get_lastrowid=True)
                    tag_id = mysql_util.execute_sql("SELECT LAST_INSERT_ID();", fetchone=True)[0] # Get last inserted ID
                # Link the tag to the item
                insert_item_tag_sql = "INSERT INTO ItemTag (item_id, tag_id) VALUES (%s, %s)"
                mysql_util.execute_sql(insert_item_tag_sql, params=(item_id, tag_id), commit=True)

        flash('Item details updated successfully!', 'success')
        return redirect(url_for('item_details', item_id=item_id))

    return render_template('edit_item_details.html', item=item, photos=photos, tags=tags)
