from rest_framework import permissions
from src.common.constants import USER_GROUP_TEACHER, USER_GROUP_STUDENT, USER_GROUP_EXPERT


class IsTeacherUser(permissions.BasePermission):
    """
    Permission to only allow teachers to execute an action.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name=USER_GROUP_TEACHER).count() > 0


class IsStudentUser(permissions.BasePermission):
    """
    Permission to only allow students to execute an action.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name=USER_GROUP_STUDENT).count() > 0


class IsExpertUser(permissions.BasePermission):
    """
    Permission to only allow experts to execute an action.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name=USER_GROUP_EXPERT).count() > 0


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
