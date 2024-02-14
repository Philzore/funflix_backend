from django.contrib.auth.forms import UserCreationForm
from .models import CostumUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CostumUser
        fields = '__all__'