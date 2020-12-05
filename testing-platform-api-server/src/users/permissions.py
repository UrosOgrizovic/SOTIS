from rest_framework import permissions


class IsTeacherUser(permissions.BasePermission):
    """
    Permission to only allow teachers to execute an action.
    """
    def has_permission(self, request, view):
        return request.user.is_teacher


class IsStudentUser(permissions.BasePermission):
    """
    Permission to only allow students to execute an action.
    """
    def has_permission(self, request, view):
        return request.user.is_student


class IsExpertUser(permissions.BasePermission):
    """
    Permission to only allow experts to execute an action.
    """
    def has_permission(self, request, view):
        return request.user.is_expert


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
