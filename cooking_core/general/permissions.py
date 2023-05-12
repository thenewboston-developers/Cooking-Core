from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, AnonymousUser):
            return False

        return obj.account_number == request.user.account_number


class IsObjectCreatorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user
