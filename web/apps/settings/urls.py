"""
Urls
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^change_password/$', views.AccountSettingView.as_view(), name='change_pwd'),
    url(r'^change_password/update/$', views.AccountSettingUpdateView.as_view(), name='change_pwd_update'),
    url(r'^additional_settings/$', views.AdditionalSettingListView.as_view(), name='additional_settings'),
    url(r'^additional_settings/create/$', views.AdditionalSettingCreateView.as_view(), name='additional_settings_create'),
    url(r'^additional_settings/edit/(?P<pk>\d+)$', views.AdditionalSettingEditListView.as_view(), name='additional_settings_edit'),
    url(r'^additional_settings/update/(?P<pk>\d+)$', views.AdditionalSettingUpdateView.as_view(), name='additional_settings_update'),
    url(r'^additional_settings/delete/(?P<pk>\d+)$', views.AdditionalSettingDeleteView.as_view(), name='additional_settings_delete'),
]
