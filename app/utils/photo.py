# File: photo.py
from PIL import Image
import io
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename

from app.utils import mysql_util
from app import app

UPLOAD_FOLDER = 'app/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     

def get_image(request):
    if 'file' not in request.files:
        flash('No file part')
        print('No file part')
        return None
    
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        print('No image selected for uploading')
        return None
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        print((os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        return (os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        print("here?")
        return None

def upload_image(file: str):
    """
    Converts an image file to a png with a name
    matching its id in the database.

    file: file path string
    """
    if isinstance(file, str):  # if it's a file path
        original_path = file
        if not os.path.exists(file):
            # raise FileNotFoundError("Image not found: %s" % file)
            print ("Image not found: %s" % file)
            return
        img = Image.open(file)
    
    # convert image to PNG
    png_buffer = io.BytesIO()
    img.save(png_buffer, format='PNG')
    png_buffer.seek(0)
    
    # save to database and get photo_id
    sql = '''
    INSERT INTO Photo () VALUES ()
    ''' # empty insert
    photo_id = mysql_util.execute_sql(sql, commit=True, get_lastrowid=True)
    
    # save file as {photo_id}.png
    filepath = ('app/static/images/store/%s.png' % photo_id)
    with open(filepath, 'wb') as f:
        f.write(png_buffer.getvalue())

    # delete original
    if filepath != original_path:
        os.remove(original_path)
    
    return photo_id

def link_item_photo(item_id: int, photo_id: int, display_order: int):
    sql = '''
    INSERT INTO Item_Photo (item_id, photo_id, display_order) VALUES
    (%s, %s, %s);
    '''
    mysql_util.execute_sql(sql, (item_id, photo_id, display_order), True)

def update_User_photo_id(photo_id, user_id):
    sql = '''
    UPDATE User SET photo_id = %s WHERE user_id = %s
    '''
    mysql_util.execute(sql, (photo_id, user_id), True)

if __name__ == '__main__':
    upload_image('app/static/images/uploads/harp.webp')
    upload_image('app/static/images/uploads/t1.png')
    upload_image('app/static/images/uploads/t2.png')
    upload_image('app/static/images/uploads/g0.webp')
    upload_image('app/static/images/uploads/g1.webp')
    upload_image('app/static/images/uploads/g2.webp')
    upload_image('app/static/images/uploads/trumpet1.jpg')
    upload_image('app/static/images/uploads/trumpet2.jpg')
    upload_image('app/static/images/uploads/trumpet3.jpg')
    upload_image('app/static/images/uploads/m1.webp')
    upload_image('app/static/images/uploads/m2.webp')
    upload_image('app/static/images/uploads/m3.webp')
    upload_image('app/static/images/uploads/m4.webp')
    
