from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer, RegisterSerializer
from .models import User


class Register(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
