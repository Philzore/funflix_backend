from django.db import models
from datetime import date

# Create your models here.
class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description  = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos', blank=True, null=False)
    
    def file_size(self):
        if self.video_file:
            size = self.video_file.size
            size_mb = size / (1024 * 1024)
            return "{:.2f} MB".format(size_mb)
        else:
            return "N/A"