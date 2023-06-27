from rest_framework import permissions
from hintonmovie.globals import AccountTypeEnum


class IsAdminorReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        else:
            return bool(request.user and request.user.is_staff)


class IsReviewUserorReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff
    

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return is_admin or request.method in permissions.SAFE_METHODS


class IsOwnerProfileOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.profile == request.user.profile
    

class IsMasterAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.profile and request.user.profile.is_super_admin and request.user.profile.broker and request.user.profile.broker.is_network)
    

class IsEditorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.profile and request.user.profile.account_type and request.user.profile.account_type.name == AccountTypeEnum.EDITOR.value and not request.user.profile.is_super_admin and request.user.profile.broker and request.user.profile.broker.is_network)
    

class IsMasterUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.profile and request.user.profile.broker and request.user.profile.broker.is_network)
    


class IsBusinessAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.profile and request.user.profile.is_super_admin and request.user.profile.broker and not request.user.profile.broker.is_network)
        

class IsSupervisorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.profile and not request.user.profile.is_super_admin and request.user.profile.account_type and request.user.profile.account_type.name == AccountTypeEnum.SUPERVISOR.value and request.user.profile.broker and not request.user.profile.broker.is_network)
    

class IsBusinessEditorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.profile and not request.user.profile.is_super_admin and request.user.profile.account_type and request.user.profile.account_type.name == AccountTypeEnum.EDITOR.value and request.user.profile.broker and not request.user.profile.broker.is_network)
        

class IsAdminInSystemOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.profile and request.user.profile.is_super_admin and request.user.profile.broker)
        

        

