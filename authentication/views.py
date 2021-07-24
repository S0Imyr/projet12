from authentication.permissions import ManagementPermission
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from .serializers import GroupSerializer, UserSerializer, RegisterSerializer
from .models import User

from django.contrib.auth.models import Group


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes=[ManagementPermission]


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes=[ManagementPermission]
