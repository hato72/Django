from rest_framework.permissions import BasePermission,SAFE_METHODS

class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        print(request)
        print(view)
        return True
    
class ProductPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return obj.user == request.user
        return True