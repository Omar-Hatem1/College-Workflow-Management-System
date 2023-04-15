from core.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView

class TokenObtainPairView (BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer