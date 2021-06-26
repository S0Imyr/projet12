from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication import views as auth_views
from crm import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', auth_views.UserViewSet, basename='user')
router.register(r'groups', auth_views.GroupViewSet, basename='group')
router.register(r'clients', views.ClientViewSet, basename='client')
router.register(r'contracts', views.ContractViewSet, basename='contract')
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'status', views.StatusViewSet, basename='status')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('signup/', auth_views.Register.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
]
