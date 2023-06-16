from rest_framework.permissions import BasePermission

class CanSendTask(BasePermission):
    """
    Allows access only to users who can send tasks.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.staff.role != 'admin' and request.user.staff.role != 'doctor' and request.user.staff.role != 'assistant')

class CanReceiveTask(BasePermission):
    """
    Allows access only to users who can receive tasks.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.staff.role != 'admin' and  request.user.staff.role != 'dean')
    
class IsDoctorOrAssistant(BasePermission):
    """
    Allows access only to users who can send leaves request.
    """
    def has_permission(self, request, view):
       return bool(request.user and (request.user.staff.role == 'doctor' or request.user.staff.role == 'assistant'))

class IsDeanViceDeanHOD(BasePermission):
    """
    Allows access only to users who can accept/refuse leaves request.
    """
    def has_permission(self, request, view):
        return bool(request.user and (request.user.staff.role == 'dean' or request.user.staff.role == 'vice' or request.user.staff.role == 'head'))
    
class IsSecretaryAdmin(BasePermission):
    """
    Allow only Admin and Secretary to view Accepted Leaves
    """
    def has_permission(self, request, view):
        return bool(request.user and (request.user.staff.role == 'secretary' or request.user.staff.role == 'admin'))