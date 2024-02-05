from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

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
            'email': user.email
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
            current_site = get_current_site(request)
            activation_link = reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
            activation_url = 'http://' + current_site.domain + activation_link
            #send mail
            subject = 'Activate your account please'
            message = f'Hi! {new_user.username}, click on the following link, to activate your account: {activation_url}'
            send_mail(subject, message, 'from@example.com', [new_user.email])

            return JsonResponse({'success': True})
        except Exception as e:
            err_msg = str(e)
            return JsonResponse({'success': False, 'error': err_msg}) 

class ActivateAccount(APIView):

    def post(self, request):
        pass