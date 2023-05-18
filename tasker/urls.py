from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter 
from tasker.views import * 


router = DefaultRouter()
router.register('sent-tasks',SentTasksViewSet, basename='sent-tasks')
router.register('received-tasks',ReceivedTasksViewSet, basename='received-tasks')
router.register('receivers',ReceiversViewSet, basename='receivers')
router.register('tasks-responses',TaskResponseViewSet, basename='response')
router.register('tasks',TaskAdminViewSet, basename='tasks')
router.register('vacationapply', DoctorAssistantLeaveAPI, basename= 'leaveapply')
#router.register('vacationlist', DeanViceDeanHODLeaveAPI, basename= 'leavelist')
urlpatterns = [
    path ('', include(router.urls)),
]
