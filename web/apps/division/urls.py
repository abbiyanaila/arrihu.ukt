"""
Urls
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^division/$', views.DivisionView.as_view(), name='view'),
    url(r'^division/create$', views.DivisionCreateView.as_view(), name='create'),
    url(r'^division/update/(?P<pk>\d+)$', views.DivisionUpdateView.as_view(), name='update'),
    url(r'^division/delete/(?P<pk>\d+)$', views.DivisionDeleteView.as_view(), name='delete'),
    url(r'^division/create/(?P<div_pk>\d+)/level$',
        views.DivisionLevelCreateView.as_view(), name='l_create'),
    url(r'^division/update/(?P<div_pk>\d+)/level/(?P<pk>\d+)$',
        views.DivisionLevelUpdateView.as_view(), name='l_update'),
    url(r'^division/delete/(?P<div_pk>\d+)/level/(?P<pk>\d+)$',
        views.DivisionLevelDeleteView.as_view(), name='l_delete'),
]
