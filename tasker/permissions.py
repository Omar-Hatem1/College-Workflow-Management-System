from rest_framework.permissions import BasePermission

class CanSendTask(BasePermission):
    """
    Allows access only to users who can send tasks.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.staff.role != 'Admin' and request.user.staff.role != 'Doctor' and request.user.staff.role != 'Assistant')

class CanReceiveTask(BasePermission):
    """
    Allows access only to users who can receive tasks.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.staff.role != 'Admin' and  request.user.staff.role != 'Dean')
    
class IsDoctorOrAssistant(BasePermission):
    def has_permission(self, request, view):
       bool(request.user and (request.user.staff.role == 'Doctor' or  request.user.staff.role == 'Assistant'))

class IsDeanViceDeanHOD(BasePermission):
    def has_permission(self, request, view):
        bool(request.user and (request.user.staff.role == 'Dean' or request.user.staff.role == 'Vice_Dean' or request.user.staff.role == 'Head_of_department'))