from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
