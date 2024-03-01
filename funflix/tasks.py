import subprocess #befehle aus terminal ausführen
import os

resolutions = ['480', '720', '1080']

def convert_videos(source):
    cutted_source = source[:-4]
    for resolution in resolutions:
        target = cutted_source + '_{}p.mp4'.format(resolution)
        cmd = 'ffmpeg -i "{}" -s hd{} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, resolution, target)
        subprocess.run(cmd)

def delete_videos(source):
    cutted_source = source[:-4]
    for resolution in resolutions:
        delete_path = cutted_source + '_{}p.mp4'.format(resolution) 
        os.remove(delete_path)
    delete_thumbnail(cutted_source)
    
def create_thumbnail(source):
    cutted_source = source[:-4]
    thumbnail_path = cutted_source + '_thumbnail.jpg'
    cmd_thumbnail = 'ffmpeg -i "{}" -frames:v 1 "{}"'.format(source, thumbnail_path)
    subprocess.run(cmd_thumbnail)
    
def delete_thumbnail(cutted_source):
    thumbnail_path = cutted_source + '_thumbnail.jpg'
    os.remove(thumbnail_path)