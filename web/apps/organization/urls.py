"""
Urls
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.OrganizationView.as_view(), name='view'),
    url(r'^create$', views.OrganizationCreateView.as_view(), name='create'),
    url(r'^edit/(?P<pk>\d+)$', views.OrganizationEditView.as_view(), name='edit'),
    url(r'^update/(?P<pk>\d+)$', views.OrganizationUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)$', views.OrganizationDeleteView.as_view(), name='delete'),
]
