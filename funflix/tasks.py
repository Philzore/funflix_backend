import subprocess #befehle aus terminal ausführen
import os

def convert_videos(source):
    resolutions = ['480', '720', '1080']
    cutted_source = source[:-4]
    for resolution in resolutions:
        target = cutted_source + '_{}p.mp4'.format(resolution)
        cmd = 'ffmpeg -i "{}" -s hd{} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, resolution, target)
        subprocess.run(cmd)

    
def create_thumbnail(source):
    cutted_source = source[:-4]
    thumbnail_path = cutted_source + '_thumbnail.jpg'
    cmd_thumbnail = 'ffmpeg -i "{}" -frames:v 1 "{}"'.format(source, thumbnail_path)
    subprocess.run(cmd_thumbnail)