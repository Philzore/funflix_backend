import os
from .models import Video
from .tasks import convert_480p
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    
    if (created):
        print('neues video wurde erstellt')
        queue = django_rq.get_queue('default', autocommit= True)
        queue.enqueue(convert_480p, instance.video_file.path)
        

@receiver(post_delete, sender=Video)
def video_post_del(sender, instance, using, **kwargs):
    """
    deletes file from filesystem
    when corresponding video object is deleted
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)