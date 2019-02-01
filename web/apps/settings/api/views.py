
from rest_framework_jwt.views import ObtainJSONWebToken
from .serializers import JWTLoginSerializer

class JWTLoginView(ObtainJSONWebToken):
    serializer_class = JWTLoginSerializer