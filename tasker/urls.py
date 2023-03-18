from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
#router.register('receivers', views)
router.register('tasks', views.TasksViewSet, basename='tasks')
#router.register('response', views.TaskResponseViewSet)

urlpatterns = [
    path ('', include(router.urls))
]
