from django.contrib import admin
from .models import Video

# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'title', 'description', 'video_file' )



admin.site.register(Video, VideoAdmin)