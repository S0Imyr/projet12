from rest_framework.permissions import BasePermission


class ManagementPermission(BasePermission):
    message = 'Restricted to management team'
    
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Management').exists():
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Management').exists():
            return True
        else:
            return False