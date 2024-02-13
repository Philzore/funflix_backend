import subprocess #befehle aus terminal ausführen

def convert_480p(source):
    target = source + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target) #fuegt variablen den string hinzu
    subprocess.run(cmd)