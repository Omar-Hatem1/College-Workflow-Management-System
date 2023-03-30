from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
#from rest_framework_nested.routers import DefaultRouter , NestedDefaultRouter


router = DefaultRouter()
router.register('sent-tasks', views.SentTasksViewSet, basename='sent-tasks')
router.register('received-tasks', views.ReceivedTasksViewSet, basename='received-tasks')
router.register('receivers', views.ReceiversViewSet, basename='receivers')



# tasks_router=NestedDefaultRouter(router, 'received-tasks', lookup = 'receivedtask')
# tasks_router.register('response', views.TaskResponseViewSet, basename='task-response')





urlpatterns = [
    path ('', include(router.urls)),
    #path ('', include(tasks_router.urls)),
    #path ('receivers/', views.ReceiversList.as_view())
]
