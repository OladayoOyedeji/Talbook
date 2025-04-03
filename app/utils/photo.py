# File: photo.py
from PIL import Image
import io
import os

from app.utils import mysql_util

def upload_image(file: str):
    """
    Converts an image file to a png with a name
    matching its id in the database.

    file: file path string
    """
    if isinstance(file, str):  # if it's a file path
        original_path = file
        if not os.path.exists(file):
            raise FileNotFoundError("Image not found: %s" % file)
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
    filepath = ('app/static/images/uploads/%s.png' % photo_id)
    if (original_path == filepath):
        return photo_id
    with open(filepath, 'wb') as f:
        f.write(png_buffer.getvalue())

    # delete original if different from original
    os.remove(original_path)
    
    return photo_id

def link_item_photo(item_id: int, photo_id: int, display_order: int):
    sql = '''
    INSERT INTO Item_Photo (item_id, photo_id, display_order) VALUES
    (%s, %s, %s);
    '''
    mysql_util.execute_sql(sql, (item_id, photo_id, display_order), True)

if __name__ == '__main__':
    upload_image('app/static/images/uploads/harp.webp')
    upload_image('app/static/images/uploads/t1.png')
    upload_image('app/static/images/uploads/t2.png')
