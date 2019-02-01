"""
Urls
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add$', views.LevellingInfoView.as_view(), name='view'),
    url(r'^create$', views.LevellingInfoCreateView.as_view(), name='create'),
    url(r'^levelling/(?P<lev_info_pk>\d+)$', views.LevellingListView.as_view(), name='lev_list'),
    url(r'^levelling/(?P<lev_info_pk>\d+)/add$', views.LevellingAddView.as_view(), name='lev_add'),
    url(r'^levelling/(?P<lev_info_pk>\d+)/create$', views.LevellingCreateView.as_view(), name='lev_create'),
    url(r'^levelling/(?P<lev_info_pk>\d+)/delete/(?P<pk>\d+)$', views.LevellingDeleteView.as_view(), name='lev_delete'),
    
    url(r'^weight$', views.ExamWeightView.as_view(), name='w_view'),
    url(r'^weight/create$', views.ExamWeightCreateView.as_view(), name='w_create'),
    url(r'^weight/edit/(?P<pk>\d+)$', views.ExamWeightEditView.as_view(), name='w_edit'),
    url(r'^weight/update/(?P<pk>\d+)$', views.ExamWeightUpdateView.as_view(), name='w_update'),
    url(r'^weight/delete/(?P<pk>\d+)$', views.ExamWeightDeleteView.as_view(), name='w_delete'),
]
