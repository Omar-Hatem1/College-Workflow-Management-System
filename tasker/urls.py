from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
#router.register('receivers', views)
router.register('tasks', views.TasksViewSet)
router.register('receivers', views.ReceiversViewSet, basename='receivers')
#router.register('response', views.TaskResponseViewSet)

urlpatterns = [
    path ('', include(router.urls)),
    #path ('receivers/', views.ReceiversList.as_view())
]
