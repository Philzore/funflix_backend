from .models import *
from user.models import CustomUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ["username"]

# class ThumbnailSerializer(serializers.ModelSerializer):
#     author = serializers.ReadOnlyField(source='author.username')
#     class Meta:
#         model = Video
#         fields = "__all__"