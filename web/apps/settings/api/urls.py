from django.conf.urls import url
# from . import views
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken

urlpatterns = [
    url(r'^login$', ObtainJSONWebToken.as_view(), name='obtain'),
    url(r'^token/verify$', VerifyJSONWebToken.as_view(), name='verify'),
]
