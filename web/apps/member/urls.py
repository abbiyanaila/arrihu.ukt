"""
Urls
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.MemberListView.as_view(), name='view'),
    url(r'^add$', views.MemberAddView.as_view(), name='add'),
    url(r'^create$', views.MemberCreateView.as_view(), name='create'),
    url(r'^detail/(?P<pk>\d+)$', views.MemberDetailView.as_view(), name='detail'),
    url(r'^edit/(?P<pk>\d+)$', views.MemberEditView.as_view(), name='edit'),
    url(r'^update/(?P<pk>\d+)$', views.MemberUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)$', views.MemberDeleteView.as_view(), name='delete'),
    url(r'^passwd_change/(?P<pk>\d+)$', views.MemberPasswordChangeView.as_view(), name='passwd_change'),
]
