from django.contrib import admin
from .models import CostumUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(CostumUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Individuelle Daten',
            {
                'fields' : (
                    'custom',
                    'phone',
                    'address'
                )
            }
        )
    ) 

