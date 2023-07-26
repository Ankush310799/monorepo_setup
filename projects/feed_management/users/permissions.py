"""
    This module contains all permissions related to users.
"""
from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """ Users API permissions """

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True
        elif request.user==obj:
            if request.method == 'DELETE':
                return False
            else:
                return True
        else:
            return False
