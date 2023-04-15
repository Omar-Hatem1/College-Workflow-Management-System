from rest_framework.permissions import BasePermission

class CanSendTask(BasePermission):
    """
    Allows access only to users who can send tasks.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.staff.role != 'dr')

class CanReceiveTask(BasePermission):
    """
    Allows access only to users who can receive tasks.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.staff.role != 'dean')