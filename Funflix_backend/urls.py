"""
URL configuration for Funflix_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import  settings
from django.conf.urls.static import static
from django.urls import path, include
from funflix.views import LoginView, RegisterView, ActivateAccount, UserView,ThumbnailView, GuestView, UploadVideoView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('guest/', GuestView.as_view()),
    path('register/', RegisterView.as_view()),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccount.as_view(), name='activate_account'),
    path('start-screen/get_user/', UserView.as_view()),
    path('start-screen/get_thumbnails/', ThumbnailView.as_view()),
    path('start-screen/add_video/', UploadVideoView.as_view(), name='upload_video'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('django-rq/', include('django_rq.urls')),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT) + staticfiles_urlpatterns() 
