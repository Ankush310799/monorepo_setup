"""
    This module contains all permissions related to Feed API.
"""
from rest_framework import permissions

class UserPermissionForFeedAPI(permissions.BasePermission):
    """ Users API permissions """

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True
        elif request.user == obj.created_by:
            return True
        else:
            self.message = 'You can not update/delete address of other user.'
            return False


class UserPermissionForReportFeedAPI(permissions.BasePermission):
    """ User Report on Feed API permissions """

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True
        else:
            return False
