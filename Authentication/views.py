from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .serializers import RegisterSerializer
from .models import MyUser
from .utils import Util


# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = MyUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('Authentication:email-verify')
        ablurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

        email_body='hi  '+ user.username +" "+ "Use the Link bellow to verify your email \n   " + " " +ablurl
        data = {'email_body': email_body, 'email_subject':'verify your email','to_email':user.email}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass
