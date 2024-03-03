from .models import Video
from user.models import CustomUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ["username"]

class VideoThumbnailSerializer(serializers.Serializer):
    # video_filename = serializers.CharField()
    # thumbnail_filename = serializers.CharField()
    # author = serializers.SerializerMethodField()

    def get_author(self, instance):
        video = Video.objects.filter(video_file=instance).first()
        if video:
            return video.author.username
        return None
    
    def get_video_id(self, instance):
        video = Video.objects.filter(video_file=instance).first()
        if video:
            return video.id
        return None
    
    def get_video_title(self, instance):
        video = Video.objects.filter(video_file=instance).first()
        if video:
            return video.title
        return None
    
    def get_video_description(self, instance):
        video = Video.objects.filter(video_file=instance).first()
        if video:
            return video.description
        return None
    

    def to_representation(self, instance):
        video_filename = instance[:-len('_thumbnail.jpg')] + '.mp4'
        thumbnail_filename = instance[len('/media/'):]
        return {
            'video_id' : self.get_video_id(video_filename.lstrip('/media/')),
            'video_title' : self.get_video_title(video_filename.lstrip('/media/')),
            'video_description' : self.get_video_description(video_filename.lstrip('/media/')),
            'video_filename': video_filename.lstrip('/media/'),
            'thumbnail_filename': thumbnail_filename.lstrip('/media/'),
            'author': self.get_author(video_filename.lstrip('/media/'))
        }