"""
    This module contains all permissions related to Adddress API.
"""
from rest_framework import permissions
from address.models import Address


class UserPermissionForAddressAPI(permissions.BasePermission):
    """ Users API permissions """

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True
        elif request.user == obj.user:
            if request.method == 'DELETE':
                return False
            else:
                return True
        else:
            self.message = 'You can not update/delete address of other user.'
            return False
