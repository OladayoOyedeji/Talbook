# File: photo.py
from moviepy.editor import VideoFileClip
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

def video_allowed_file(filename):
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
    
    if file and video_allowed_file(file.filename):
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

# def compress_video(input_path: str, output_path: str, bitrate: int = "500k") -> None:
#     """
#     Compress an image and save it to a new location as a png
#     """
#     if not os.path.exists(input_path):
#         raise FileNotFoundError("Input file does not exist: %s" % input_path)

#     try:
#         video_clip = VideoFileClip(input_path)
#         video_clip.write_videofile(output_path, bitrate=bitrate)
#         video_clip.close()
#         # img = Image.open(input_path)

#         # if img.mode in ("RGBA", "P"):
#         #     img = img.convert("RGB")

#         # img.save(output_path, format='PNG', optimize=True)

#         # print("Compressed %s saved to: %s" % (input_path, output_path))

#     except Exception as e:
#         print("Error compressing video %s: %s" % (input_path, e))

import ffmpeg

def compress_video(input_path, output_path, target_size_kb=1000):
    try:
        probe = ffmpeg.probe(input_path)
        duration = float(probe['format']['duration'])
        total_bitrate = int(probe['format']['bit_rate'])
        
        # Calculate target video bitrate based on desired file size
        target_video_bitrate = (target_size_kb * 8 * 1024) / duration
        
        # Ensure the target bitrate is not too low
        min_bitrate = 100000  # Minimum acceptable bitrate in bps
        if target_video_bitrate < min_bitrate:
            target_video_bitrate = min_bitrate
        
        # FFmpeg command for compression
        ffmpeg.input(input_path) \
            .output(output_path, 
                    vcodec='libx264',  # Use H.264 codec for speed and compatibility
                    video_bitrate=target_video_bitrate,
                    maxrate=target_video_bitrate * 1.2,  # Limit max bitrate
                    bufsize=target_video_bitrate * 2,    # Set buffer size
                    vf='scale=1280:720',                 # Optionally reduce resolution
                    acodec='aac',                       # Audio codec
                    audio_bitrate='128k') \
            .run(capture_stdout=True, capture_stderr=True)
        print(f"Video compressed successfully to {output_path}")
    except Exception as e:
        print(f"An error occurred during compression: ")

def create_thumbnail(video_path, output_path, time='00:00:00'):
    """
        Creates a thumbnail from a video using ffmpeg.
    
        Args:
            video_path (str): Path to the video file.
            output_path (str): Path to save the thumbnail image.
            time (str, optional): Timestamp for the thumbnail (HH:MM:SS). Defaults to '00:00:00'.
    """
    command = f'ffmpeg -i "{video_path}" -ss {time} -vframes 1 "{output_path}"'
    os.system(command)
    
def upload_video(file: str):
    """
    Converts an image file to a compressed png with a name
    matching its id in the database
    """
    if isinstance(file, str):  # if it's a file path
        original_path = file
        if not os.path.exists(file):
            print("Video not found: %s" % file)
            return

    # save to database and get video_id
    sql = '''
    INSERT INTO Video () VALUES ()
    '''  # empty insert
    video_id = mysql_util.execute_sql(sql, commit=True, get_lastrowid=True)

    # save file as {photo_id}.png
    filepath = ('app/static/videos/store/%s.mp4' % video_id)

    thumbnail_path = 'app/static/videos/store/thumbnail/%s.webp' % video_id

    print("did ts work?")
    compress_video(original_path, filepath)
    create_thumbnail(filepath, thumbnail_path)
    # delete original
    if original_path != filepath:
        os.remove(original_path)

    return video_id

def link_Post_Video(video_id, post_id):
    sql = '''
    INSERT INTO Post_Video ()
'''
