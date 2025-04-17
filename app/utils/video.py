# File: photo.py
from PIL import Image
import io
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename

# from app import app
from app.utils import mysql_util
UPLOAD_FOLDER = 'app/static/uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['mp4', 'mkv', 'wmv', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_video(request):
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
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        #print('upload_image filename: ' + filename)
        flash('video successfully uploaded and displayed below')
        print((os.path.join(UPLOAD_FOLDER, filename)))
        return (os.path.join(UPLOAD_FOLDER, filename))
    else:
        flash('Allowed video types are - mp4, mkv, wmv, gif')
        print("here?")
        return None

# def compress_image(input_path: str, output_path: str, quality: int = 30) -> None:
#     """
#     Compress an image and save it to a new location as a png
#     """
#     if not os.path.exists(input_path):
#         raise FileNotFoundError("Input file does not exist: %s" % input_path)

#     try:
#         img = Image.open(input_path)

#         if img.mode in ("RGBA", "P"):
#             img = img.convert("RGB")

#         img.save(output_path, format='PNG', optimize=True)

#         print("Compressed %s saved to: %s" % (input_path, output_path))

#     except Exception as e:
#         print("Error compressing image %s: %s" % (input_path, e))

def upload_video(file: str):
    """
    Converts an image file to a compressed png with a name
    matching its id in the database
    """
    if isinstance(file, str):  # if it's a file path
        original_path = file
        if not os.path.exists(file):
            print("Image not found: %s" % file)
            return

        img = Image.open(file)

    # save to database and get video_id
    sql = '''
    INSERT INTO Video () VALUES ()
    '''  # empty insert
    video_id = mysql_util.execute_sql(sql, commit=True, get_lastrowid=True)

    # save file as {photo_id}.png
    filepath = ('app/static/videos/store/%s.png' % video_id)

    # compress_image(original_path, filepath)

    # delete original
    if original_path != filepath:
        os.remove(original_path)

    return photo_id

def link_Post_Video(video_id, post_id):
    sql = '''
    INSERT INTO Post_Video ()
'''
