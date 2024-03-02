from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Video
from .serializer import *

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT) #total life time
User = get_user_model()

# Create your views here.
class LoginView(ObtainAuthToken, APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username' : user.username
            })
        except Exception as e:
            err_msg = str(e)
            return JsonResponse({'success': False, 'error': err_msg})
        
class GuestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            guest_user = User.objects.create_guest_user()
            guest_user.is_active = True
            guest_user.save()
            token, created = Token.objects.get_or_create(user=guest_user)
            return Response({
                'token': token.key,
                'user_id': guest_user.pk,
                'email': guest_user.email,
                'username' : guest_user.username
            })
        except Exception as e:
            err_msg = str(e)
            return JsonResponse({'success': False, 'error': err_msg})

class RegisterView(APIView):

    def post(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            
            new_user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
            
            new_user.is_active = False
            new_user.save()

            #generate token
            token = default_token_generator.make_token(new_user)
           
            #create link
            uid = urlsafe_base64_encode(force_bytes(new_user.pk))
            current_site = 'localhost:4200'
            
            activation_link = reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
            activation_url = 'http://' + current_site + activation_link
            print(activation_url)
            #send mail
            subject = 'Activate your account please'
            message = f'Hi! {new_user.username}, click on the following link, to activate your account: {activation_url}'
            send_mail(subject, message, settings.EMAIL_HOST_USER , [new_user.email])

            return JsonResponse({'success': True})
        except Exception as e:
            err_msg = str(e)
            return JsonResponse({'success': False, 'error': err_msg}) 

class ActivateAccount(APIView):

     def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return JsonResponse({'success': True, 'message': 'Account activated successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid token. Try again!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        

# @method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MainView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        usernames = User.objects.all()
        serializer = UserSerializer(usernames, many= True)
        return Response(serializer.data)
    
    
class UploadVideoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            author = request.user
            video_title = request.data.get('title')
            video_description = request.data.get('description')
            video_file = request.data.get('file')
            print(video_file)
            #check if video object wioth same title exist
            if Video.objects.filter(title=video_title).exists():
                return JsonResponse({'success': False, 'message': 'Title already exist'})
            #create new video object
            new_video_model = Video.objects.create(author=author, title= video_title, description= video_description,video_file= video_file)
            new_video_model.save()
            return JsonResponse({'success': True, 'message': 'Good job'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})