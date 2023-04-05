from rest_framework.permissions import BasePermission

class CanSendTask(BasePermission):
    """
    Allows access only to users who can send tasks.
    """

    def has_permission(self, request, view):
        return bool(request.user.staff.role == 'dean' or request.user.staff.role == 'vice' or request.user.staff.role == 'head')