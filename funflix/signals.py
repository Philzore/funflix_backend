import os
from .models import Video
from .tasks import create_thumbnail, convert_videos, delete_videos, delete_thumbnail
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    
    if (created and instance.video_file):
        print(f'neues video wurde erstellt {instance.video_file}')
        queue = django_rq.get_queue('default', autocommit= True)
        
        queue.enqueue(convert_videos, instance.video_file.path)
       
        queue.enqueue(create_thumbnail, instance.video_file.path)
    else:
        print (f'Kein neues Video, video Filee : {instance.video_file}')
        

@receiver(post_delete, sender=Video)
def video_post_del(sender, instance, using, **kwargs):
    """
    deletes file from filesystem
    when corresponding video object is deleted
    """
    if instance.video_file: #check if video exist
        if os.path.isfile(instance.video_file.path): #check if video file exist on data system
            os.remove(instance.video_file.path) #remove original video file from file system
            queue = django_rq.get_queue('default', autocommit= True)
            queue.enqueue(delete_videos, instance.video_file.path) #remove converted videos from file system
            
            
    
        