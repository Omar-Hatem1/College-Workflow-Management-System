from django.urls import path, include
from rest_framework.routers import SimpleRouter
from core.views import *
router = SimpleRouter() 

router.register('users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path ('users/', UsersViewSet.as_view()),
    # path ('users/<int:pk>', UsersViewSet.as_view())
]