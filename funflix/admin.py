from django.contrib import admin
from .models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class VideoAdmin(ImportExportModelAdmin):
    list_display = ('created_at', 'title', 'description', 'video_file', 'file_size' )

class VideoResource(resources.ModelResource):
    class Meta:
        model = Video

admin.site.register(Video, VideoAdmin)