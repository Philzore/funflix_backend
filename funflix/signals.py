import os
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Geiler Hengst')
    if (created):
        print('neues video wurde erstellt')

@receiver(post_delete, sender=Video)
def video_post_del(sender, instance, using, **kwargs):
    """
    deletes file from filesystem
    when corresponding video object is deleted
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)