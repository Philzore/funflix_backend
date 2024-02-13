from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT) #total life time

# Create your views here.
class LoginView(ObtainAuthToken, APIView):
    def post(self, request, *args, **kwargs):
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
        

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MainView(APIView):
    
    def get(self, request):
        return JsonResponse({'success': False})