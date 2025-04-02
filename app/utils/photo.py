# File: photo.py
from PIL import Image
import io
import os

from app.utils import mysql_util

def upload_image(file):
    """
    Converts an image file to a png with a name
    matching its id in the database.

    file: file path string
    """
    # handle both file paths and FileStorage objects
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
    with open(filepath, 'wb') as f:
        f.write(png_buffer.getvalue())

    # delete original
    os.remove(original_path)
    
    return photo_id

if __name__ == '__main__':
    upload_image('app/static/images/uploads/harp.webp')
