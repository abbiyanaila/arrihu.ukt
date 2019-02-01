from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^get/(?P<username>[\w\-]+)$',
        views.ProfileObjectAPIView.as_view(), name='get'),
]
