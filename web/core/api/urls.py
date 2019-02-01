from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list$', views.FCMDeviceListView.as_view(), name='list'),
    url(r'^create$', views.FCMDeviceCreateView.as_view(), name='create'),
]
